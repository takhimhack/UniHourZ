import sys
import bottle
import json

from server_code.parse_login.parse_login import parse_email
from server_code import client_validator


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

    @bottle.post('/userLogin')
    def validate_login():
        response=bottle.request.body.read().decode()
        decoded_response = client_validator.sanitize_input(response)
        #check if registering
        if client_validator.contains(decoded_response, 
            ['email', 'name', 'password', 'loginType', 'typeofUser']):
            validState = parse_email(decoded_response['email'], 'buffalo.edu')
            if (validState != 'valid'):
                return json.dumps({
                    'valid': validState
                })
            #some firebase registration code, then return success
            return json.dumps({
                    'valid': validState
            })
        #this is for loggin in
        elif client_validator.contains(decoded_response, ['email', 'password']):
            validState = parse_email(decoded_response['email'], 'buffalo.edu')
            if (validState != 'valid'):
                return json.dumps({
                    'valid': validState
                })
            #some firebase login code, then return success
            return json.dumps({
                    'valid': validState
            })
        
        else:
            return json.dumps({
                    'valid': 'invalid!'
            })
        






            
    bottle.run(host="0.0.0.0", port=port)