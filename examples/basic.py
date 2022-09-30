
from easyjsondb import Database

db = Database('test.json', indent=4)

db['value'] = 100 # very easy

db.save() # save it
