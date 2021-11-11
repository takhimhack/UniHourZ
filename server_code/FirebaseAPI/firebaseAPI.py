import os
import json
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
# config_user = {
#    "apiKey": os.environ.get('apiKey'),
#    "authDomain": os.environ.get('authDomain'),
#    "databaseURL": os.environ.get('databaseURL'),
#    "storageBucket": os.environ.get('storageBucket')
# }

config_server = {
   "apiKey": os.environ.get('apiKey'),
   "authDomain": os.environ.get('authDomain'),
   "databaseURL": os.environ.get('databaseURL'),
   "storageBucket": os.environ.get('storageBucket'),
   "serviceAccount": "service_account/service.json"
}
server_keys = {
  "type": os.environ.get("type"),
  "project_id": os.environ.get("project_id"),
  "private_key_id": os.environ.get("private_key_id"),
  "private_key": os.environ.get("private_key"),
  "client_email": os.environ.get("client_email"),
  "client_id": os.environ.get("client_id"),
  "auth_uri": os.environ.get("auth_uri"),
  "token_uri": os.environ.get("token_uri"),
  "auth_provider_x509_cert_url": os.environ.get("auth_provider_x509_cert_url"),
  "client_x509_cert_url": os.environ.get("client_x509_cert_url")
}

if not os.path.isdir("service_account"):
  os.mkdir("service_account")

if not os.path.isfile("service_account/service.json"):
  with open("service_account/service.json", "w") as file:
    json.dump(server_keys, file)

# firebase = Firebase(config_user)
firebase_server = Firebase(config_server)
# auth = firebase.auth()
# db = firebase.database()
auth = firebase_server.auth()
server_db = firebase_server.database()
