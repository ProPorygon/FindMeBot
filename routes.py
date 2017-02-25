from bottle import route, request
import logging
import json

@route('/', method='POST')
def defaut():
    json_message = request.body.read()
    data = json.loads(json_message)
    message = data["text"]
    user = data["user_id"]
    url = data["attachments"].get("url")
    attachment_type = data["attachments"].get("type")
    print url
    print message
    print user
    print attachment_type
