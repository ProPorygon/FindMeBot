from bottle import route, request, response
import logging
import json
import psycopg2
import os
from urlparse import urlparse
import requests
from PIL import Image
from io import BytesIO
from face import findURLs

url = urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

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
        uid = match_image(url)
        r = requests.post("https://api.groupme.com/v3/bots/post", data={'bot_id':os.environ['BOT_KEY'] 'text': str(uid)})

    if message.lower() == "this is me":
        save_image(user, url)

    print url
    print message
    print user
    print attachment_type

def match_image(url):
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT (id) FROM userimage")
    urls = ["https://findmechatbot.herokuapp.com/image/{}.jpg".format(i[0]) for i in cur]
    print urls
    indices, _ = findURLs(url, urls)
    uid = cur[indices[0]]
    return uid

@route('/image/<id>.jpg')
def get_image(id):
    con = db_connect()
    cur = con.cursor()

    cur.execute("SELECT (image) FROM userimage WHERE id = %s", (int(id),))
    result = cur.fetchone()
    img_io = BytesIO(result[0])
    bytes = img_io.read()
    response.set_header('Content-type', 'image/jpeg')
    return bytes

    con.close()

'''
Function to associate a user id with an image, storing both in postgres
'''
def save_image(user, url):
    con = db_connect()
    cur = con.cursor()

    response = requests.get(url)
    data = BytesIO(response.content)

    binary = psycopg2.Binary(response.content)
    cur.execute("INSERT INTO userimage(id, image) VALUES (%s, %s)", (user,binary))
    con.commit()

    print "success"
    con.close()

    return

def db_connect():
    con = psycopg2.connect(
        dbname = dbname,
        user = user,
        password = password,
        host = host,
        port = port
    )

    return con
