import bottle
import os


file_name_dict = {
    "bootstrap.min.css": "assets/bootstrap/css/bootstrap.min.css",
    "bootstrap.min.js": "assets/bootstrap/js/bootstrap.min.js",
    "styles.css": "assets/css/Login-Form-Dark.css",

}

@bottle.route('/')
def rethtml():
    return bottle.static_file("index.html", ".")



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
def return_fonts(filename):
    return bottle.static_file(filename, "./assets/img/")

bottle.run(host="0.0.0.0", port=8000)