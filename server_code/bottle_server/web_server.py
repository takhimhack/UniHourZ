from os.path import isfile
import bottle
import json
import requests
import server_code.FirebaseAPI.firebaseAPI as fire

from server_code.parse_login.parse_login import parse_email
from server_code import client_validator
from server_code.FirebaseAPI.Registration import registerUser
import server_code.FirebaseAPI.firebase_queue as fire_q
from server_code.firebase_lock import *

app = bottle.Bottle()

@app.route('/')
def ret_html():
    return bottle.static_file("index.html", ".")

@app.route('/<filename>')
def ret_html_2(filename): 
    if filename.endswith(".html") and isfile(filename):
        return bottle.static_file(filename, ".") 
    else:
        bottle.abort(code=404, text="The requested file does not exist.")

@app.route('/instructor/<filename:path>')
def ret_instructor(filename):
    #note: upon logging into the app, we can redirect to this if the request was made with an instructor account.
    #abort with a 404 if the requested file doesn't exist
    if not isfile(f"./instructor/{filename}"):
        bottle.abort(code=404, text="The requested file does not exist.")

    #get the auth token from the cookie
    authToken = bottle.request.get_cookie("authToken")
    
    #If auth token none, we abort
    if authToken is None:
        bottle.abort(code=403, text="We're sorry, but you don't have the permissions to view this page.")
    
    #Get the account information from the authToken. Throws requests.HTTPError if failure.
    #Catch this error and abort.
    account_info = "" 
    try:
        account_info = fire.auth.get_account_info(authToken)
    
    except requests.HTTPError:
        bottle.abort(code=403, text="We're sorry, but you don't have the permissions to view this page.")
    
    # Now query the firebase database. Access users -> 0 -> localId. 
    # If this localId is not under instructors, we abort.
    localId = account_info['users'][0]['localId']

    if not fire_q.is_instructor(localId):
        bottle.abort(code=403, text="We're sorry, but you don't have the permissions to view this page.")
        
    else:
        return bottle.static_file(filename, "./instructor")

@app.route('/assets/<filename:path>')
def ret_assets(filename):
    return bottle.static_file(filename, "./assets")

@app.route('/getConfig')
def return_config():
    data = ""
    with open("server_configuration_files/config-decrypted.json", "r") as readFile:
        data = readFile.read()
    return data

@app.post('/userRegistration')
def validate_registration():
    response = bottle.request.body.read().decode()
    decoded_response = client_validator.sanitize_input(response)
    # check if registering
    if client_validator.contains(decoded_response, ['email', 'name', 'password', 'typeofUser', 'discordName']):
        valid_state = parse_email(decoded_response['email'], 'buffalo.edu')
        if valid_state != 'valid':
            return json.dumps({
                'valid': valid_state
            })
        valid_state = registerUser(decoded_response)
        return json.dumps({
            'valid': valid_state
        })
    else:
        return json.dumps({
            'valid': 'invalid!'
        })

@app.route('/queuedata')
def return_queue():
    auth_token = bottle.request.get_cookie("authToken")
    if auth_token is None:
        bottle.abort(code=403, text="We're sorry, but you don't have the permissions to view this page.")
    try:
        fire.auth.get_account_info(auth_token)
    except requests.HTTPError:
        bottle.abort(code=403, text="We're sorry, but you don't have the permissions to view this page.")
    cse220 = fire_q.access_queue('cse220')
    cse250 = fire_q.access_queue('cse250')
    cse331 = fire_q.access_queue('cse331')
    return json.dumps({
        'queues': {
            'CSE220': {'queue': cse220[0], 'length': cse220[1], 'instructor': cse220[2], 'location': cse220[3],
                        'eta': cse220[4], 'student': cse220[5], 'status': cse220[6]},
            'CSE250': {'queue': cse250[0], 'length': cse250[1], 'instructor': cse250[2], 'location': cse250[3],
                        'eta': cse250[4], 'student': cse250[5], 'status': cse250[6]},
            'CSE331': {'queue': cse331[0], 'length': cse331[1], 'instructor': cse331[2], 'location': cse331[3],
                        'eta': cse331[4], 'student': cse331[5], 'status': cse331[6]}
        },
        'valid': 'valid'
    })


@app.post('/dequeue')
def dequeue():
    response = bottle.request.body.read().decode()
    decoded_response = client_validator.sanitize_input(response)
    try:
        info = fire.auth.get_account_info(decoded_response['token'])
    except requests.HTTPError:
        return json.dumps({'valid': 'invalid'})
    if not fire_q.is_instructor(info['users'][0]['localId']):
        return bottle.abort(code=403, text="We're sorry, but you don't have the permissions to view this page.")
    try:
        next_student = fire_q.dequeue_student(decoded_response['class'])
    except fire_q.EmptyQueue:
        return json.dumps({'valid': 'invalid'})
    cse220 = fire_q.access_queue('cse220')
    cse250 = fire_q.access_queue('cse250')
    cse331 = fire_q.access_queue('cse331')
    return json.dumps({
        'queues': {
            'CSE220': {'queue': cse220[0], 'length': cse220[1], 'instructor': cse220[2], 'location': cse220[3],
                        'eta': cse220[4]},
            'CSE250': {'queue': cse250[0], 'length': cse250[1], 'instructor': cse250[2], 'location': cse250[3],
                        'eta': cse250[4]},
            'CSE331': {'queue': cse331[0], 'length': cse331[1], 'instructor': cse331[2], 'location': cse331[3],
                        'eta': cse331[4]}
        },
        'student': next_student,
        'valid': 'valid'
    })


@app.post('/settings')
def change_settings():
    response = bottle.request.body.read().decode()
    decoded_response = client_validator.sanitize_input(response)
    print(decoded_response)
    try:
        info = fire.auth.get_account_info(decoded_response['token'])
    except requests.HTTPError:
        return bottle.abort(403, "You don't have permission to view this page.")
    if fire_q.is_instructor(info['users'][0]['localId']):
        if decoded_response["edit"] == "true":
            fire_q.change_queue_settings(decoded_response)
        else:
            queue_info = fire_q.access_queue(decoded_response["class"])
            return json.dumps({'instructor': queue_info[2], 'location': queue_info[3], 'eta': queue_info[4], 'status': queue_info[6]})
        # return json.dumps({'valid': 'valid'})
    else:
        return bottle.abort(403, "You don't have permission to view this page.")


@app.route('/checkstatus')
def get_privilege():
    auth_token = bottle.request.get_cookie("authToken")
    if auth_token is None:
        bottle.abort(code=403, text="We're sorry, but you don't have the permissions to view this page.")
    try:
        info = fire.auth.get_account_info(auth_token)
        print(info)
    except requests.HTTPError:
        return bottle.abort(403, "You don't have permission to view this page.")
    if fire_q.is_instructor(info['users'][0]['localId']):
        return json.dumps({'valid': 'valid'})
    else:
        return json.dumps({'valid': 'invalid'})