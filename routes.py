from bottle import route, request

@route('/', type='POST')
def defaut():
    data = request.body.read()
    print data
