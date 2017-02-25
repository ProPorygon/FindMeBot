from bottle import route, request
import logging
import json

@route('/', method='POST')
def defaut():
    json_message = request.body.read()
    data = json.loads(json_message)
    message = data["text"]
    user = data["user_id"]
    url = data["attachments"][0].get("url")
    attachment_type = data["attachments"][0].get("type")
    print url
    print message
    print user
    print attachment_type
