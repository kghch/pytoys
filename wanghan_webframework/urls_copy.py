from web_copy import get, post, view, ctx


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
@post('/student')
def Student():

    i = ctx.request.input(name='Me', sex='M', noexist='hhh')
    print i.get('name')
    print i.get('sex')
    print i.get('noexist')
    str = 'This is student'
    return dict(title='Student Page', str=str)

