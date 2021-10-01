import os
from firebase import Firebase

config = {
   "apiKey": os.environ.get('apikey'),
   "authDomain": os.environ.get('authDomain'),
   "databaseURL": os.environ.get('databaseURL'),
   "storageBucket": os.environ.get('storageBucket')
}

firebase = Firebase(config)



