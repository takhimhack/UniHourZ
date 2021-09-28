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



@bottle.route('/<filename>')
def route_dependencies(filename):
    return bottle.static_file(filename, ".")






bottle.run(host="0.0.0.0", port=8000)