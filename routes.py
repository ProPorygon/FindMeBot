from bottle import route, request
import logging

@route('/', method='POST')
def defaut():
    data = request.body.read()
    url = data["url"]
    message = data["text"]
    user = data["user_id"]
    print url
    print message
    print user
