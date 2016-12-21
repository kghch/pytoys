from web_copy import get, view


@get('/')
def Index():
    u1 = {"name": "aaa", "sex": "F"}
    u2 = {"name": "bbb", "sex": "M"}
    users = []
    users.append(u1)
    users.append(u2)
    return dict(users=users)

@view('/another.html')
@get('/another')
def Another():
    names = []
    names.append('wanghan')
    names.append('kghch')
    names.append('kouganhen')

    return dict(names=names)

@view('/student.html')
@get('/student/<studentid>')
def Student(sid):
    str = 'This is student %s' % sid
    return dict(title='Student Page', str=str)