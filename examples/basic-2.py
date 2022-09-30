
from easyjsondb import Database

with Database('test.json', indent=4) as db:
    #db.loadFile() if you want
    db['value'] = 200
    # auto db.save()
