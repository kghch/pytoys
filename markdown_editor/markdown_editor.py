# -*- coding: utf-8 -*-
import tornado
import markdown
import os
import tornado.web
import tornado.httpserver
import torndb
import json
import re

MARKDOWN_EXT = ('codehilite', 'extra')

db = torndb.Connection(host='127.0.0.1:3306', database='docs', user='root', password='123456')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', HomeHandler),
            (r'/preview', PreviewHandler),
            (r'/create', CreateHandler),
            (r'/save', SaveHandler),
            (r'/showpreview/(\d+)', ShowPreviewHandler),
            (r'/mydocs', MydocsHandler),
            (r'/show/(\d+)', ShowByFidHandler)
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
        unicode_raw_text = unicode(raw_text, "utf-8")
        md = markdown.Markdown(extensions=MARKDOWN_EXT)
        html_text = md.reset().convert(unicode_raw_text)
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
        g = re.search(r"<h[1-6]>[^<]+</h[1-6]>", data['html'])
        if g:
            title = g.group(0)[4:-5]
        else:
            title = "untitled"

        if doc:
            fid = doc['fid']
            db.execute("UPDATE doc set raw=%s, html=%s, title=%s, updated=UTC_TIMESTAMP() WHERE fid=%s", data['raw'], data['html'], title, int(fid))
        else:
            fid = int(data['fid'])
            unicode_raw = unicode(data['raw'], "utf-8")
            db.execute("""INSERT INTO doc(fid, title, raw, html, created, updated) VALUES(%s, %s, %s, %s, UTC_TIMESTAMP(), UTC_TIMESTAMP())""", fid, title, unicode_raw, data['html'])
        self.write({"fid":str(fid), "title": title})

class ShowPreviewHandler(tornado.web.RequestHandler):
    def get(self, fid):
        doc = db.get("SELECT * FROM doc WHERE fid=%s", fid)
        if doc:
            self.render('preview.html', fid=fid, html=doc['html'], title=doc['title'])
        else:
            self.render("error.html", error="The page hasn't been developed yet.")

class MydocsHandler(tornado.web.RequestHandler):
    def get(self):
        docs = db.query("SELECT * FROM doc ORDER BY created DESC")
        for doc in docs:
            doc['updated'] = doc['updated'].strftime("%Y-%m-%d %H:%M:%S")
            doc['created'] = doc['created'].strftime("%Y-%m-%d %H:%M:%S")
        table_html = self.render_string("docs.html", docs=docs)
        self.write(table_html)

class ShowByFidHandler(tornado.web.RequestHandler):
    def get(self, fid):
        doc = db.get("SELECT * FROM doc WHERE fid=%s", fid)
        if doc:
            self.render('home.html', fid=fid, title=doc['title'], raw=doc['raw'], html=doc['html'])
        else:
            self.render("error.html", error="The page hasn't been developed yet.")


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(9876)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
