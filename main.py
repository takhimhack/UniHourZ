import sys
import bottle
import json

import os
import requests

import server_code.FirebaseAPI.firebaseAPI as fire


from server_code.parse_login.parse_login import parse_email
from server_code import client_validator
from server_code.FirebaseAPI.Registration import registerUser


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

    @bottle.route('/')
    def rethtml():
        return bottle.static_file("index.html", ".")

    @bottle.route('/<filename>')
    def rethtml(filename):
        return bottle.static_file(filename, ".")

    @bottle.route('/assets/bootstrap/css/<filename>')
    def return_bootstrap_css(filename):
        return bottle.static_file(filename, "./assets/bootstrap/css/")

    @bottle.route('/assets/bootstrap/js/<filename>')
    def return_bootstrap_js(filename):
        return bottle.static_file(filename, "./assets/bootstrap/js/")

    @bottle.route('/assets/css/<filename>')
    def return_css(filename):
        return bottle.static_file(filename, "./assets/css/")

    @bottle.route('/assets/frontendjs/<filename>')
    def return_client_js(filename):
        return bottle.static_file(filename, "./assets/frontendjs/")

    @bottle.route('/assets/fonts/<filename>')
    def return_fonts(filename):
        return bottle.static_file(filename, "./assets/fonts/")

    @bottle.route('/assets/img/<filename>')
    def return_img(filename):
        return bottle.static_file(filename, "./assets/img/")

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

    @bottle.post('/userLogin')
    def validate_login():
        response = bottle.request.body.read().decode()
        decoded_response = client_validator.sanitize_input(response)
        if client_validator.contains(decoded_response, ['email', 'password']):
            valid_state = parse_email(decoded_response['email'], 'buffalo.edu')
            if valid_state != 'valid':
                return json.dumps({'valid': 'invalid!', 'message': "Enter valid email address"})
            try:
                user = fire.auth.sign_in_with_email_and_password(decoded_response["email"], decoded_response["password"])
                return json.dumps({'valid': 'valid', 'user': decoded_response["email"]})
            except requests.HTTPError as err:
                if err.strerror[err.strerror.find("message") + 11:err.strerror.find("message") + 26] == 'EMAIL_NOT_FOUND':
                    return json.dumps({'valid': 'invalid!', 'message': "Account does not exist"})
                elif err.strerror[
                     err.strerror.find("message") + 11:err.strerror.find("message") + 27] == 'INVALID_PASSWORD':
                    return json.dumps({'valid': 'invalid!', 'message': "Invalid password"})
                else:
                    return json.dumps({'valid': 'invalid!', 'message': "Login error"})
        else:
            return json.dumps({'valid': 'invalid!', 'message': "Enter email and password"})

    bottle.run(host="0.0.0.0", port=port)
