import json
import html

from bottle import html_escape

def sanitize_input(jsonStr):
    actualDict = json.loads(jsonStr)
    for key in actualDict:
        actualDict[key] = html_escape(actualDict[key])
    return actualDict

def contains(clientData, listOfKeys):
    for key in listOfKeys:
        if key not in clientData or (key != 'discordName' and clientData[key] == "") or \
                (key == 'discordName' and clientData[key] == "" and clientData['typeofUser'] != "Instructor"):
            return False
    
    return True
