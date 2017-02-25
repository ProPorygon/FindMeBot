from bottle import route, request
import logging

@route('/', method='POST')
def defaut():
    data = request.body.read()
    print data
