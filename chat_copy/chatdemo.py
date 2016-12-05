import tornado.web
import tornado.gen
import tornado.ioloop
import tornado.httpserver
from tornado.concurrent import Future
import os
import uuid

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/new', MessageNewHandler),
            (r'/update', MessageUpdateHandler)
        ]

        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            debug=True
        )

        super(Application, self).__init__(handlers, **settings)

class MessageBuffer(object):
    def __init__(self):
        self.waiters = set()
        self.cache = []
        self.cachesize = 200

    def new_message(self, message):
        for future in self.waiters:
            future.set_result(message)
        self.waiters = set()

    def wait_for_messages(self, cursor):
        result_future = Future()

        self.waiters.add(result_future)
        return result_future

global_message_buffer = MessageBuffer()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('home.html', messages='empty')

class MessageNewHandler(tornado.web.RequestHandler):
    def post(self):
        message = {
            'mid': str(uuid.uuid4()),
            'body': self.request.body
        }
        message['html'] = self.render_string('message.html', message=message)
        self.write(message['html'])
        global_message_buffer.new_message(message)

class MessageUpdateHandler(tornado.web.RequestHandler):
    """
    因为js端，一直在进行/update，但是因为future是空，所以不会完成ajax。

    1. 每当一个连接建立，就会有一个/update（未完成），新建一个waiter，在等着future中被塞入消息；
    2. 每当/new 时，会往所有的future中塞消息（塞完消息顺便清空waiters，因为我完成了），然后这些在监听的，因为future中有消息了，所以/update请求完成；
    """
    @tornado.gen.coroutine
    def post(self):
        cursor = self.request.body
        self.future = global_message_buffer.wait_for_messages(cursor)
        message = yield self.future
        self.write(dict(message=message))

def main():
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(22222)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()

