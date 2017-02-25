from bottle import route

@route('/')
def defaut():
    return "Hello World"
