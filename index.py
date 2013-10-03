#-*- coding:utf-8 -*- 
from bae.core.wsgi import WSGIApplication
from weblog.runapp import app
application = WSGIApplication(app)
