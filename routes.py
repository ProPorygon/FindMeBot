from bottle import route, request
import logging
import json
import psycopg2
import os
from urlparse import urlparse
import requests
from PIL import Image
from io import BytesIO

@route('/', method='POST')
def defaut():
    json_message = request.body.read()
    data = json.loads(json_message)
    message = data["text"]
    user = data["user_id"]
    url = ""
    attachment_type = ""
    if len(data["attachments"]) > 0:
        url = data["attachments"][0]["url"]
        attachment_type = data["attachments"][0]["type"]

    if message.lower() == "this is me":
        save_image(user, url)

    print url
    print message
    print user
    print attachment_type

'''
Function to associate a user name with an image
TODO: Determine how to store image
'''
def save_image(user, url):
    url = urlparse.urlparse(os.environ['DATABSE_URL'])
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    con = psycopg2.connect(
        dbname = dbname,
        user = user,
        password = password,
        host = host,
        port = port
    )

    curs = con.cursor()

    response = requests.get(url)
    data = BytesIO(response.content)

    binary = psycopg2.Binary(data)
    cur.execute("INSERT INTO userimages(id, image) VALUES (%s, %s)", user, (binary,))

    return
