from bottle import route, request
import logging

@route('/', type='POST')
def defaut():
    data = request.body.read()
    logging.info(data)
