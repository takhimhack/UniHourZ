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

    @bottle.route('/assets/<filename:path>')
    def ret_assets(filename):
        return bottle.static_file(filename, "./assets")

    @bottle.route('/instructor/<filename:path>')
    def ret_assets(filename):
        return bottle.static_file(filename, "./instructor")

    @bottle.route('/student/<filename:path>')
    def ret_assets(filename):
        return bottle.static_file(filename, "./student")

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

    @bottle.route('/queuedata')
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


    @bottle.post('/dequeue')
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


    @bottle.post('/settings')
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


    @bottle.route('/checkstatus')
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


    bottle.run(host="0.0.0.0", port=port)
