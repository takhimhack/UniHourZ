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
        if key not in clientData or clientData[key] == "":
            return False
    
    return True
