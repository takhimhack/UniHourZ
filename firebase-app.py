import os
from firebase import Firebase

config = {
   "apiKey": os.environ.get('apikey'),
   "authDomain": os.environ.get('authDomain'),
   "databaseURL": os.environ.get('databaseURL'),
   "storageBucket": os.environ.get('storageBucket')
}

firebase = Firebase(config)

sample_entry = {
    "123456": {
        "name" : "FirstName LastName",
        "students" : ['studenta', 'studentb', 'studentc']
    },
    "234567" : {
        "name" : "FromServer ToDB",
        "students" : ['studente', 'studentb', 'studentf'] 
    }
}


db = firebase.database()

