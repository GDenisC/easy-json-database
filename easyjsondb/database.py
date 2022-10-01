
import json, base64, zlib

from typing import Callable

from .constants import DEFAULT_ENCODING
from .errors import DatabaseWrongCoding

__all__ = ('EncodeTypes', 'Database', 'decode_database', 'encode_database', )

class EncodeTypes:
    ENCODE_NONE: int = 0x00
    ENCODE_BASE64: int = 0x10
    ENCODE_BASE64_URLSAFE: int = 0x11
    ENCODE_ZLIB_MAX: int = 0x20
    
    @staticmethod
    def parseCoderType(encode: int) -> tuple[Callable, Callable]:
        if encode == Database.ENCODE_NONE:
            return (
                lambda bts: bts,
                lambda bts: bts
            )
        elif encode == Database.ENCODE_BASE64:
            return (
                base64.b64encode,
                base64.b64decode
            )
        elif encode == Database.ENCODE_BASE64_URLSAFE:
            return (
                base64.urlsafe_b64encode,
                base64.urlsafe_b64decode
            )
        elif encode == Database.ENCODE_ZLIB_MAX:
            return (
                lambda bts: zlib.compress(bts, level=9),
                lambda bts: zlib.decompress(bts, wbits=zlib.MAX_WBITS)
            )

class Database(dict, EncodeTypes):
    __slots__ = ('filename', '_encoder', '_decoder', 'indent', )

    filename: str
    _encoder: Callable[[bytes], bytes]
    _decoder: Callable[[bytes], bytes]
    indent: int | None

    def __init__(self, /, filename: str, indent: int = None) -> None:
        super().__init__()
        self.filename = filename
        self.indent = indent

        self._encoder = lambda bts: bts
        self._decoder = lambda bts: bts
    
    def loadFile(self, /, encoding: str = DEFAULT_ENCODING) -> None:
        with open(self.filename, 'rb') as fb:
            self.update(
                json.loads(
                    self._decoder(fb.read()).decode(encoding)
                )
            )

    def setCoderType(self, encode: int = EncodeTypes.ENCODE_NONE, /, encoder: Callable[[bytes], bytes] = None, decoder: Callable[[bytes], bytes] = None) -> None:
        if encoder and decoder:
            if not isinstance(encoder, Callable[[bytes], bytes]) and isinstance(decoder, Callable[[bytes], bytes]):
                raise DatabaseWrongCoding()
            
            self._encoder = encoder
            self._decoder = decoder
            return

        c = self.parseCoderType(encode)
        self._encoder: Callable[[bytes], bytes] = c[0]
        self._decoder: Callable[[bytes], bytes] = c[1]
    
    def save(self, /, ensure_ascii: bool = False, encoding: str = DEFAULT_ENCODING) -> None:
        with open(self.filename, 'wb') as fb:
            fb.write(
                self._encoder(
                    json.dumps(self.copy(), ensure_ascii=ensure_ascii, indent=self.indent).encode(encoding)
                )
            )
    
    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.save()

def decode_database(db: str, encode: int = EncodeTypes.ENCODE_NONE, /, encoding: str = DEFAULT_ENCODING, ensure_ascii: bool = False, indent: int = None) -> None:
    with open(db, 'rb') as fb:
        dat = json.loads(
                EncodeTypes.parseCoderType(encode)[1](fb.read()).decode(DEFAULT_ENCODING)
            )

    with open(db, 'w', encoding=encoding) as f:
        json.dump(dat, f, ensure_ascii=ensure_ascii, indent=indent) 

def encode_database(db: str, encode: int = EncodeTypes.ENCODE_NONE, /, encoding: str = DEFAULT_ENCODING, ensure_ascii: bool = False, indent: int = None) -> None:
    with open(db, 'r') as f:
        dat = json.load(f)

    with open(db, 'wb') as fb:
        fb.write(
            EncodeTypes.parseCoderType(encode)[0](
                json.dumps(dat, ensure_ascii=ensure_ascii, indent=indent).encode(encoding)
            )
        )
