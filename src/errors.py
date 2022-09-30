
__all__ = (
    'DatabaseWrongCoding',
)

class DatabaseWrongCoding(Exception):
    def __init__(self) -> None:
        super().__init__("Encoder or decoder isn\'t equal type `Callable[[bytes], bytes]`")
