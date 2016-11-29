import tornado
import markdown
import os
import tornado.web
import tornado.httpserver

MARKDOWN_EXT = ('codehilite', 'extra')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', HomeHandler),
            (r'/preview', PreviewHandler)
        ]

        settings = dict(
            editor_title = "KGHCH markdown",
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies = False,
            debug = True
        )
        super(Application, self).__init__(handlers, **settings)

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('home.html', content='Hello world.')


class PreviewHandler(tornado.web.RequestHandler):
    def post(self):
        raw_text = self.request.body
        md = markdown.Markdown(extensions=MARKDOWN_EXT)
        html_text = md.reset().convert(raw_text)    
        self.write(html_text)

def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(9876)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
