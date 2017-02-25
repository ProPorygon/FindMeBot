from bottle import route, request
import logging

@route('/', method='POST')
def defaut():
    data = request.body.read()
    message = data["text"]
    user = data["user_id"]
    url = data["attachments"].get("url")
    attachment_type = data["attachments"].get("type")
    print url
    print message
    print user
    print attachment_type
