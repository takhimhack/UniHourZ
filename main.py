from server_code.bottle_server.web_server import *
from server_code.discord_bot.discord_bot import *
import threading as th
from os import environ

def startWebServer():
    app.run(host='0.0.0.0', port=environ.get("PORT") if environ.get("PORT") is not None else 5000)


if __name__ == "__main__":
    # Start the web server
    th.Thread(target=startWebServer).start()
    #Start Discord Bot
    bot.run(environ.get("TOKEN"))