
import tornado
import tornado.web
import tornado.httpserver
import os
from tornado.concurrent import Future

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', HomeHandler),
            (r'/new', MessageNewHandler),
            (r'/update', MessageUpdateHanlder)
        ]

        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies = False,
            debug = True
        )
        super(Application, self).__init__(handlers, **settings)

class MessageBufferClass(object):
    def __init__(self):
        self.waiters = set()
        self.cache = []

    def add_message(self, message):
        for waiter in self.waiters:
            waiter.set_result(message)
        self.waiters = set()

    def wait_for_messages(self):
        waiter = Future()

        self.waiters.add(waiter)
        return waiter

MessageBuffer = MessageBufferClass()

class MessageNewHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.request.body
        # write new message to MessageBuffer
        MessageBuffer.add_message(text)
        self.write({'text': text})

class MessageUpdateHanlder(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def post(self):
        self.future = MessageBuffer.wait_for_messages()
        messages = yield self.future
        message_html = self.render_string("message.html", messages=messages)
        self.write(message_html)


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html", messages="nothing")


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8888)
    tornado.ioloop.IOLoop.current().start()
