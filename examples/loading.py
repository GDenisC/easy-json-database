
from easyjsondb import Database

db = Database('test.json', indent=4)
db.loadFile() # load test.json

db['value'] /= 2

db.save()
