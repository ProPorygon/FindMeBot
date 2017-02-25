import bottle
import os
from os import environ

# routes contains the HTTP handlers for our server and must be imported.
import routes

def wsgi_app():
    return bottle.default_app()

if __name__ == '__main__':
    HOST = "0.0.0.0"
    try:
        PORT = int(os.environ.get('PORT', '5000'))
    except ValueError:
        PORT = 5555

    # Starts a local test server.
    bottle.run(server='gunicorn', host=HOST, port=PORT)
