from web_copy import WSGIApplication, Jinja2TemplateEngine
import urls_copy
import os



wsgi = WSGIApplication()
wsgi.template_engine = Jinja2TemplateEngine(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
wsgi.add_module(urls_copy)
wsgi.run()

