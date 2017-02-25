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
    """
    Handles incoming connections to the bot
    """
    json_message = request.body.read()
    data = json.loads(json_message)
    message = data["text"]
    user = data["user_id"]
    groupid = data["group_id"]
    url = ""
    attachment_type = ""

    if message.lower() == "this is me" and len(data["attachments"]) > 0 and data["attachments"][0]["type"] == "image":
        save_image(user, url)

    else if len(data["attachments"]) > 0 and data["attachments"][0]["type"] == "image":
        url = data["attachments"][0]["url"]
        attachment_type = data["attachments"][0]["type"]
        uid = match_image(url)
        nickname = get_name_from_uid(uid, groupid)
        attachments = [{"type": "mentions", "user_ids":[str(uid)], "loci": [[0, len(nickname)]]}]
        r = requests.post("https://api.groupme.com/v3/bots/post", data={'bot_id':os.environ['BOT_KEY'], 'text': nickname, 'attachments': attachments})


    print data
    print user
    print message

def get_name_from_uid(uid, groupid):
    """
    Returns a user nickname for a uid in a particular group
    """
    response = requests.get("https://api.groupme.com/v3/groups/{}?token={}".format(groupid,os.environ['GROUPME_KEY']))
    group_data = json.loads(response.text)
    for item in group_data['response']['members']:
        if item["user_id"] == str(uid):
            return item['nickname']
    return ""

def match_image(url):
    """
    Finds the matching uid for the image linked by the url
    """
    con = db_connect()
    cur = con.cursor()
    cur.execute("SELECT (id) FROM userimage")
    results = cur.fetchall()
    urls = ["https://findmechatbot.herokuapp.com/image/{}.jpg".format(i[0]) for i in results]
    indices, _ = findURLs(url, urls, os.environ['FACE_KEY'])
    uid = results[indices[0]]
    return uid[0]

@route('/image/<id>.jpg')
def get_image(id):
    """
    Loads an image from postgres to the url associated with the user's id
    """
    con = db_connect()
    cur = con.cursor()

    cur.execute("SELECT (image) FROM userimage WHERE id = %s", (int(id),))
    result = cur.fetchone()
    img_io = BytesIO(result[0])
    bytes = img_io.read()
    response.set_header('Content-type', 'image/jpeg')
    return bytes

    con.close()


def save_image(user, url):
    """
    Function to associate a user id with an image, storing both in postgres
    """
    con = db_connect()
    cur = con.cursor()

    response = requests.get(url)
    data = BytesIO(response.content)

    binary = psycopg2.Binary(response.content)
    cur.execute("INSERT INTO userimage(id, image) VALUES (%s, %s)", (user,binary))
    con.commit()

    con.close()

    return


def db_connect():
    """
    Initialize connection to database
    """
    con = psycopg2.connect(
        dbname = dbname,
        user = user,
        password = password,
        host = host,
        port = port
    )

    return con
