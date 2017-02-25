from bottle import route, request, response
import logging
import json
import psycopg2
import os
from urlparse import urlparse
import requests
from PIL import Image
from io import BytesIO

url = urlparse(os.environ['DATABASE_URL'])
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

@route('/image/<id>')
def get_image(id):
    cur = con.cursor()

    cur.execute("SELECT (image) FROM userimage WHERE id = %s", (int(id),))
    result = cur.fetchone()
    #image = Image.open(result)
    img_io = BytesIO(result)
    #image.save(img_io, 'JPEG', quality=70)
    #img_io.seek(0)
    bytes = img_io.read()
    response.set_header('Content-type', 'image/jpeg')
    return bytes


'''
Function to associate a user id with an image, storing both in postgres
'''
def save_image(user, url):
    cur = con.cursor()

    response = requests.get(url)
    data = BytesIO(response.content)

    binary = psycopg2.Binary(response.content)
    cur.execute("INSERT INTO userimage(id, image) VALUES (%s, %s)", (user,binary))
    con.commit()

    print "success"

    return
