from cryptography.fernet import Fernet
from os import environ, write

def decrypt():
    #load the config key
    configKey = Fernet(environ.get("configKey"))

    #load the server key
    serviceKey = Fernet(environ.get("serviceKey"))


    #read encrypted config file and write decrypted file.
    data = ""
    with open("server_configuration_files/config-encrypted.json", "rb") as readFile:
        data = configKey.decrypt(readFile.read())

    with open("server_configuration_files/config-decrypted.json", "wb") as writeFile:
        writeFile.write(data)

    #read encrypted service file and write decrypted file. 
    data = ""
    with open("server_configuration_files/service-encrypted.json", "rb") as readFile:
        data = serviceKey.decrypt(readFile.read())

    with open("server_configuration_files/service-decrypted.json", "wb") as writeFile:
        writeFile.write(data)
