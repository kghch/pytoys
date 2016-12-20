from web_copy import WSGIApplication
import urls_copy

class Index(object):
    def get(self):
        return ['<html> Index page </html>']


class Another(object):
    def get(self):
        return ['<html><p> Another</p> page </html>']

wsgi = WSGIApplication()
wsgi.add_module(urls_copy)
wsgi.run()

