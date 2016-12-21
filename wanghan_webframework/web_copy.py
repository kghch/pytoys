from wsgiref.simple_server import make_server
import logging
import re
import types
import functools

logging.getLogger().setLevel('INFO')

_RESPONSE_STATUSES = {
    404: 'Not Found',
    405: 'Method Not Allowed'
}

class HTTPError(Exception):
    def __init__(self, code):
        super(HTTPError, self).__init__()
        self.status = '%d %s' %(code, _RESPONSE_STATUSES[code])

    def __str__(self):
        return self.status

    __repr__ = __str__

class Template(object):
    def __init__(self, template_name, **kwargs):
        self.template_name = template_name
        self.model = dict(**kwargs)


class Jinja2TemplateEngine(object):
    def __init__(self, tempate_dir, **kwargs):
        from jinja2 import Environment, FileSystemLoader
        kwargs['autoescape'] = True
        self._env = Environment(loader=FileSystemLoader(tempate_dir), **kwargs)

    def __call__(self, path, data):
        return self._env.get_template(path).render(**data).encode('utf-8')


def view(path):
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            r = func(*args, **kwargs)
            if isinstance(r, dict):
                return Template(path, **r)
            raise ValueError('Expect return a dict when using @view() decorator.')
        return _wrapper
    return _decorator


def get(path):
    def _decorator(func):
        func.web_route = path
        func.web_method = 'GET'
        return func
    return _decorator

def post(path):
    def _decorator(func):
        func.web_route = path
        func.web_method = 'POST'
        return func
    return _decorator

class Request(object):
    def __init__(self, env):
        self.path_info = env['PATH_INFO']
        self.request_method = env['REQUEST_METHOD']


class Route(object):
    def __init__(self, fn):
        self.path = fn.web_route
        self.method = fn.web_method
        self.handler = fn


def convert_regex(path):
    # /another, /school/teacher/<coursename>, /student/<int:studentid>(useless...)
    reg = '^'
    p = path.find('<')
    if p != -1:
        reg += path[:p] + '(?P'
        q = path.find('>')
        colon = path.find(":")
        if colon != -1:
            t = path[p+1:colon]
            if t == 'int':
                reg += path[p] + path[colon+1:q+1] + '\d+)'
            else:
                print "type not supported"
        else:
            reg += path[p:q+1] + '[^/]+)'
    else:
        reg +=  path
    reg += '$'
    return reg

class WSGIApplication(object):
    def __init__(self):
        self._get_dynamic = []
        self._template_engine = None

    @property
    def template_engine(self):
        return self._template_engine

    @template_engine.setter
    def template_engine(self, engine):
        self._template_engine = engine

    def add_module(self, module):
        if type(module) != types.ModuleType:
            logging.warning("%s is not a module" % module)
            return

        for attr in dir(module):
            fn = getattr(module, attr)
            if callable(fn) and hasattr(fn, 'web_route') and hasattr(fn, 'web_method'):
                self.add_url(fn)

    def add_url(self, fn):
        route = Route(fn)
        self._get_dynamic.append(route)

    def run(self, host='127.0.0.1', port=9888):
        logging.info("Listening on %s:%s" % (host, port))
        server = make_server(host, port, self.get_application())
        server.serve_forever()

    def get_application(self):

        def fn_route(request):
            for func in self._get_dynamic:
                reg_path = convert_regex(func.path)
                m = re.match(reg_path, request.path_info)
                if m:
                    if request.request_method == func.method:
                        left = reg_path.find('<')
                        if left != -1:
                            left += 1
                            right = reg_path.find('>')
                            arg = m.group(reg_path[left:right])
                        else:
                            arg = None
                    else:
                        raise HTTPError(405)
                    if arg:
                        return func.handler(arg)
                    else:
                        return func.handler()
            raise HTTPError(404)


        def wsgi(env, start_response):
            request = Request(env)

            try:
                r = fn_route(request)
                r = self._template_engine(r.template_name, r.model)

                start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
                return r
            except HTTPError, e:
                start_response(e.status, [('Content-Type', 'text/html; charset=utf-8')])
                return [e.status]

        return wsgi


