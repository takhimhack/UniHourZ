import json
from firebase import Firebase

#load the config
config = json.load(open("server_configuration_files/config-decrypted.json", "r"))
config["serviceAccount"] = "server_configuration_files/service-decrypted.json"

firebase_server = Firebase(config)
auth = firebase_server.auth()
server_db = firebase_server.database()
