import os
from firebase import Firebase
'''
Might need to edit firebase database rules to get this to work...
{
  "rules": {
    ".read": "auth.uid != null",
    ".write": "auth.uid != null"
  }
} 
should be the ruleset for the firebase database!
'''
config = {
   "apiKey": os.environ.get('apiKey'),
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

auth = firebase.auth()
db = firebase.database()

