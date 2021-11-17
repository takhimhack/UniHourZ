import sys
import bottle
import json
import requests
#This module decrypts the server files. DO NOT GET RID OF THIS!
from decryptor import decrypt; decrypt()
import server_code.FirebaseAPI.firebaseAPI as fire

from server_code.parse_login.parse_login import parse_email
from server_code import client_validator
from server_code.FirebaseAPI.Registration import registerUser
import server_code.FirebaseAPI.firebase_queue as fire_q
from server_code.firebase_lock import *

app = bottle.Bottle()
port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

@app.route('/')
def ret_html():
    return bottle.static_file("index.html", ".")

@app.route('/<filename>')
def ret_html_2(filename):
    return bottle.static_file(filename, ".") if ".html" in filename else None

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
    if client_validator.contains(decoded_response, ['email', 'name', 'password', 'typeofUser']):
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

@app.post('/queuedata')
def return_queue():
    response = bottle.request.body.read().decode()
    decoded_response = client_validator.sanitize_input(response)
    try:
        fire.auth.get_account_info(decoded_response['token'])
    except requests.HTTPError:
        return json.dumps({'valid': 'invalid'})
    try:
        fireBaseLock.acquire()
        cse220 = fire_q.access_queue('cse220')
        fireBaseLock.release()
    except fire_q.QueueDoesNotExist:
        fireBaseLock.release()
        cse220 = ([], 0)
    try:
        fireBaseLock.acquire()
        cse250 = fire_q.access_queue('cse250')
        fireBaseLock.release()
    except fire_q.QueueDoesNotExist:
        fireBaseLock.release()
        cse250 = ([], 0)
    try:
        fireBaseLock.acquire()
        cse354 = fire_q.access_queue('cse354')
        fireBaseLock.release()
    except fire_q.QueueDoesNotExist:
        fireBaseLock.release()
        cse354 = ([], 0)
    return json.dumps({
        'queues': {
            'CSE220': {'queue': cse220[0], 'length': cse220[1]},
            'CSE250': {'queue': cse250[0], 'length': cse250[1]},
            'CSE354': {'queue': cse354[0], 'length': cse354[1]}
        },
        'valid': 'valid'
    })