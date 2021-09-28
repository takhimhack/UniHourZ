import bottle


@bottle.route('/')
def rethtml():
    return bottle.static_file("index.html", ".")





bottle.run(host="0.0.0.0", port=8000)