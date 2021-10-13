import sys
import bottle
import os
import json

from server_code.parse_login.parse_login import parse_login


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
    def validateLogin():
        response=bottle.request.body.read().decode()
        decoded_response = bottle.html_escape(response)
        decoded_response=json.loads(response)
        if "email" not in decoded_response or "name" not in decoded_response or "password" not in decoded_response:
            return json.dumps({
            "valid" : 0
            })
        isvalid = parse_login(r"^([^@+]+)+?(\w+)?@([^@]+)", decoded_response['email'], "buffalo.edu")
        # return 0 as a JSON object if email is not valid else 1.
        return json.dumps({
            "valid" : 1 if isvalid else 0
        })
            
    bottle.run(host="0.0.0.0", port=port)