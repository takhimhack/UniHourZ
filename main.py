import sys
import bottle
import json

import os
import requests

import server_code.FirebaseAPI.firebaseAPI as fire

from bs4 import BeautifulSoup
from server_code.parse_login.parse_login import parse_email
from server_code import client_validator
from server_code.FirebaseAPI.Registration import registerUser


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

    @bottle.route('/queue')
    def get_queue():
        qdata = [{'name': 'Pete', 'email': 'pete78@buffalo.edu'}, {'name': 'Charles', 'email': 'crt1@buffalo.edu'}, {'name': 'Kristen', 'email': 'kristenh@buffalo.edu'}]
        with open("landing.html") as file:
            htmlfile = file.read()
            soup = BeautifulSoup(htmlfile, 'html.parser')
            headtag = soup.find(id='queue')
            for i, student in enumerate(qdata):
                divtag = soup.new_tag('div')
                divtag['class'] = "row"
                divtag['style'] = "margin: 20px;"
                div2 = soup.new_tag('div')
                div2['class'] = 'col-md-6'
                h6 = soup.new_tag('h6')
                div2.append(h6)
                divtag.append(div2)
                h6.string = f"{i+1}. {student['name']}, {student['email']}"
                headtag.append(divtag)
        return str(soup)

    bottle.run(host="0.0.0.0", port=port)