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


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

    @bottle.route('/')
    def ret_html():
        return bottle.static_file("index.html", ".")

    @bottle.route('/<filename>')
    def ret_html_2(filename):
        return bottle.static_file(filename, ".") if ".html" in filename else None

    @bottle.route('/instructor/<filename>')
    def ret_instructor(filename):
        #note: upon logging into the app, we can redirect to this if the request was made with an instructor account.
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

        if fire.server_db.child("Instructors").child(localId).get().val() is None:
            bottle.abort(code=403, text="We're sorry, but you don't have the permissions to view this page.")
            
        else:
            return bottle.static_file(filename, "./instructor")

    @bottle.route('/assets/<filename:path>')
    def ret_assets(filename):
        return bottle.static_file(filename, "./assets")

    @bottle.route('/getConfig')
    def return_config():
        data = ""
        with open("server_configuration_files/config-decrypted.json", "r") as readFile:
            data = readFile.read()
        return data
    
    @bottle.post('/userRegistration')
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

    @bottle.post('/queuedata')
    def return_queue():
        response = bottle.request.body.read().decode()
        decoded_response = client_validator.sanitize_input(response)
        try:
            fire.auth.get_account_info(decoded_response['token'])
        except requests.HTTPError:
            return json.dumps({'valid': 'invalid'})
        try:
            cse220 = fire_q.access_queue('cse220')
        except fire_q.QueueDoesNotExist:
            cse220 = ([], 0)
        try:
            cse250 = fire_q.access_queue('cse250')
        except fire_q.QueueDoesNotExist:
            cse250 = ([], 0)
        try:
            cse354 = fire_q.access_queue('cse354')
        except fire_q.QueueDoesNotExist:
            cse354 = ([], 0)
        return json.dumps({
            'queues': {
                'CSE220': {'queue': cse220[0], 'length': cse220[1]},
                'CSE250': {'queue': cse250[0], 'length': cse250[1]},
                'CSE354': {'queue': cse354[0], 'length': cse354[1]}
            },
            'valid': 'valid'
        })


    @bottle.post('/dequeue')
    def dequeue():
        response = bottle.request.body.read().decode()
        decoded_response = client_validator.sanitize_input(response)
        try:
            info = fire.auth.get_account_info(decoded_response['token'])
        except requests.HTTPError:
            return json.dumps({'valid': 'invalid'})
        if info["typeofUser"] != "Instructor":
            return json.dumps({'valid': 'invalid'})
        next_student = fire_q.dequeue_student(decoded_response['class'])
        try:
            cse220 = fire_q.access_queue('cse220')
        except fire_q.QueueDoesNotExist:
            cse220 = ([], 0)
        try:
            cse250 = fire_q.access_queue('cse250')
        except fire_q.QueueDoesNotExist:
            cse250 = ([], 0)
        try:
            cse354 = fire_q.access_queue('cse354')
        except fire_q.QueueDoesNotExist:
            cse354 = ([], 0)
        return json.dumps({
            'queues': {
                'CSE220': {'queue': cse220[0], 'length': cse220[1]},
                'CSE250': {'queue': cse250[0], 'length': cse250[1]},
                'CSE354': {'queue': cse354[0], 'length': cse354[1]}
            },
            'student': next_student,
            'valid': 'valid'
        })


    @bottle.post('/settings')
    def change_settings():
        response = bottle.request.body.read().decode()
        decoded_response = client_validator.sanitize_input(response)
        try:
            info = fire.auth.get_account_info(decoded_response['token'])
        except requests.HTTPError:
            return
        if info["typeofUser"] != "Instructor":
            return json.dumps({'valid': 'invalid'})
        fire_q.change_queue_settings(decoded_response)


    bottle.run(host="0.0.0.0", port=port)
