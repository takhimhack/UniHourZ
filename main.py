import sys
import bottle
import os
import requests
import fireapp


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

    @bottle.route('/')
    def rethtml():
        return bottle.template("index.html", errormessage="")

    # @bottle.route('/<filename>')
    # def rethtml(filename):
    #     return bottle.static_file(filename, ".")

    @bottle.post('/')
    def do_login():
        password = bottle.request.forms.get("password")
        email = bottle.request.forms.get("email")
        try:
            user = fireapp.auth.sign_in_with_email_and_password(email, password)
            return bottle.template("home.html", username=email)
        except requests.HTTPError as err:
            if err.strerror[err.strerror.find("message")+11:err.strerror.find("message")+26] == 'EMAIL_NOT_FOUND':
                return bottle.template("index.html", errormessage="Invalid email")
            elif err.strerror[err.strerror.find("message")+11:err.strerror.find("message")+27] == 'INVALID_PASSWORD':
                return bottle.template("index.html", errormessage="Invalid password")
            else:
                return bottle.template("index.html", errormessage="Error logging in")

    @bottle.route('/assets/bootstrap/css/<filename>')
    def return_bootstrap_css(filename):
        return bottle.static_file(filename, "./assets/bootstrap/css/")

    @bottle.route('/assets/bootstrap/js/<filename>')
    def return_bootstrap_js(filename):
        return bottle.static_file(filename, "./assets/bootstrap/js/")

    @bottle.route('/assets/css/<filename>')
    def return_css(filename):
        return bottle.static_file(filename, "./assets/css/")

    @bottle.route('/assets/fonts/<filename>')
    def return_fonts(filename):
        return bottle.static_file(filename, "./assets/fonts/")

    @bottle.route('/assets/img/<filename>')
    def return_img(filename):
        return bottle.static_file(filename, "./assets/img/")

    bottle.run(host="0.0.0.0", port=port)