from wsgiref.simple_server import make_server
import logging
import re
import types

logging.getLogger().setLevel('INFO')


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


class WSGIApplication(object):
    def __init__(self):
        self._get_dynamic = []

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
        def wsgi(env, start_response):
            request = Request(env)

            start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

            res = ''

            for func in self._get_dynamic:
                if re.match(func.path + "$", request.path_info):
                    if request.request_method == func.method:
                        print func.handler.__name__
                        res += func.handler()
                    else:
                        # TODO: raise 405 Error here
                        logging.error("Method not allowed, 405 Error")
                    break

            return [res]

        return wsgi


