
from easyjsondb import Database

db = Database('test.json')
db.setCoderType(Database.ENCODE_BASE64) # use base64

db['value'] = 100

db.save()
