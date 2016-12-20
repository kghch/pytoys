from web_copy import get

#@view('index.html')
@get('/')
def Index():
    str = 'Index page'
    return str


@get('/another')
def Another():
    str = 'Another page'
    return str