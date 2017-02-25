from bottle import route, request
import logging
import json

@route('/', method='POST')
def defaut():
    json_message = request.body.read()
    data = json.loads(json_message)
    message = data["text"]
    user = data["user_id"]
    if len(data["attachments"]) > 0:
        url = data["attachments"][0]["url"]
        attachment_type = data["attachments"][0]["type"]

    if url:
        print url
    print message
    print user
    if attachment_type:
        print attachment_type
