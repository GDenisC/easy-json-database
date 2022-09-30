
"""
o no test.json encoded and i can't use it with other encoding!

FIX:
"""

from easyjsondb import Database, decode_database, encode_database

# test.json encoding: db.ENCODE_BASE64

decode_database('test.json', Database.ENCODE_BASE64)
"""
Database.ENCODE_BASE64 -> Database.ENCODE_NONE
"""

encode_database('test.json', Database.ENCODE_ZLIB_MAX)
"""
Database.ENCODE_NONE -> Database.ENCODE_ZLIB_MAX
"""

db = Database('test.json', indent=4)
db.setCoderType(db.ENCODE_ZLIB_MAX)
db.loadFile() # works!

db['value'] /= 2

db.save()
