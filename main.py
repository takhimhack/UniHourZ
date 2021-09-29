import sys
import bottle
import os


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

    @bottle.route('/')
    def rethtml():
        return bottle.static_file("index.html", ".")

    @bottle.route('/<filename>')
    def rethtml(filename):
        return bottle.static_file("filename", ".")

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