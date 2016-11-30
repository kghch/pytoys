import tornado
import markdown
import os
import tornado.web
import tornado.httpserver
import torndb
import json

MARKDOWN_EXT = ('codehilite', 'extra')

db = torndb.Connection(host='127.0.0.1:3306', database='docs', user='root', password='123456')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', HomeHandler),
            (r'/preview', PreviewHandler),
            (r'/create', CreateHandler),
            (r'/save', SaveHandler),
            (r'/show/preview', ShowPreviewHandler)
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
        latest = db.get("SELECT * FROM doc ORDER BY updated DESC LIMIT 1")
        if latest:
            self.render('home.html', fid=latest['fid'], title=latest['title'], raw=latest['raw'], html=latest['html'])
        else:
            self.render('home.html', fid='0', title='untitled', raw='', html='')


class PreviewHandler(tornado.web.RequestHandler):
    def post(self):
        raw_text = self.request.body
        md = markdown.Markdown(extensions=MARKDOWN_EXT)
        html_text = md.reset().convert(raw_text)
        self.write(html_text)

class CreateHandler(tornado.web.RequestHandler):
    def get(self):
        doc = db.get("SELECT * FROM doc ORDER BY fid DESC LIMIT 1")
        if doc:
            doc_id = doc['fid'] + 1
        else:
            doc_id = 1
        self.write({'fid':str(doc_id), 'title': 'untitled'})
        
class SaveHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        doc = db.get("SELECT * FROM doc WHERE fid=%s", int(data['fid']))
        if doc:
            fid = doc['fid']
            db.execute("UPDATE doc set raw=%s, html=%s, updated=UTC_TIMESTAMP()", data['raw'], data['html'])
        else:
            fid = int(data['fid'])
            db.execute("""INSERT INTO doc(fid, title, raw, html, created, updated) VALUES(%s, %s, %s, %s, UTC_TIMESTAMP(), UTC_TIMESTAMP())""", fid, data['title'], data['raw'], data['html'])
        self.write(str(fid))

class ShowPreviewHandler(tornado.web.RequestHandler):
    def get(self):
        fid = self.get_argument('fid')
        doc = db.get("SELECT * FROM doc WHERE fid=%s", int(fid))
        self.render('preview.html', html=doc['html'], title=doc['title'])


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(9876)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
