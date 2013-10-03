#! /home/fluyy/VirtualEnv/py2/bin/python
#-*- coding: UTF-8 -*-
import tornado.wsgi,tornado.web,tornado.escape
import os,time,datetime
from orebase import Article, initDatabase
from setting import ONBAE
from sqlcore import *
import uimodules
class IndexHandler(tornado.web.RequestHandler):
	def get(self,pid):
		try:
			pid=int(pid)
		except:
			pid=0;
		article=show_all(pid)
		category=getcategory()
		tags=gettags()
		title='Fluyy'
		return self.render('index.html',article=article,category=category,tags=tags,title=title,markdown=Toindex)

class ArticleHandler(tornado.web.RequestHandler):
	def get(self,uname,cater=None):
		if cater is not None:
			uname=uname[0:4]+'-'+uname[4:6]+'-'+uname[6:8]+uname[8:]
		#self.write(uname)
		post=show_article('post/'+uname)
		#self.write(post)
		category=getcategory()
		if post is None:
			raise tornado.web.HTTPError(404)
		return self.render('post.html',article=post,category=category,markdown=Topost)
	
class TagsHandler(tornado.web.RequestHandler):
	def get(self,uname):
		uname=tornado.escape.url_unescape(uname)
		article=show_bytags(uname)
		if article is None:
			raise tornado.web.HTTPError(404)
		category=getcategory()

		title='Tags'
		return self.render('index.html',article=article,category=category,tags=None,title=title,markdown=Toindex)

class CategoryHandler(tornado.web.RequestHandler):
	def get(self,uname):
		uname=tornado.escape.url_unescape(uname)
		article=show_bycategory(uname)
		if article is None:
			raise tornado.web.HTTPError(404)
		category=getcategory()
		tags=gettags()
		title='Category'
		return self.render('index.html',article=article,category=category,tags=tags,title=title,markdown=Toindex)

class FeedHandler(tornado.web.RequestHandler):
	def get(self):
		article=show_all(0,True)
		category=getcategory()
		tags=gettags()
		lasttime=getChangeTime()
		self.set_header("Content-Type", "application/xml; charset=utf-8")
		return self.render('atom.xml',article=article,lasttime=lasttime,markdown=Topost)


class PublishHandler(tornado.web.RequestHandler):
	def post(self):
		key1=self.get_argument("checkkey")
		key2=self.get_argument("password")
		if check(key1,key2)==True:
			article=Article()
			article.title=self.get_argument("title")
			article.content=self.get_argument("content")
			article.tags=self.get_argument("tags").replace("[","").replace("]","").split(',')
			t=time.strptime(self.get_argument("date"),"%Y-%m-%d")
			article.date=datetime.date(*t[0:3])
			article.category=self.get_argument("category")
			article.url='post/'+self.get_argument("filename")
			insert(article)
		else:
			raise tornado.web.HTTPError(500)


class ChangePassHandler(tornado.web.RequestHandler):
	def post(self):
		newkey=self.get_argument("new")
		key1=self.get_argument("checkkey")
		key2=self.get_argument("old")
		if check(key1,key2)==True:
			cpassword(newkey)
		else:
			raise tornado.web.HTTPError(500)

class InitHandler(tornado.web.RequestHandler):
	def get(self):
		initDatabase()

settings ={
	"static_path" : os.path.join(os.path.dirname(__file__), "static"),
	"template_path" : os.path.join(os.path.dirname(__file__), "templates"),
	"gzip" : True,
	#"debug" : True,
    "debug" : False,
#	"ui_modules":uimodules,
}


url=[(r'/post/(?P<cater>[a-zA-Z]+)/(?P<uname>[a-zA-Z0-9-_]+)/*',ArticleHandler),
		(r'/post/(?P<uname>[a-zA-Z0-9-_]+)/*',ArticleHandler),
		(r'/tags/(?P<uname>[a-zA-Z0-9-_%]+)/*',TagsHandler),
		(r'/category/(?P<uname>[a-zA-Z0-9-_%]+)/*',CategoryHandler),
		(r'/publish$',PublishHandler),
		(r'/(?P<pid>[0-9]*)$',IndexHandler),
		(r'/',IndexHandler),
		(r'/atom.xml$',FeedHandler),
		(r'/update$',ChangePassHandler),
		(r'/init$',InitHandler),]

if ONBAE:
	app=tornado.wsgi.WSGIApplication(url,**settings)
else: #local
	import tornado.ioloop
	import tornado.httpserver
	app=tornado.web.Application(url,**settings)
	if __name__=='__main__':    
		http_server=tornado.httpserver.HTTPServer(app)
		http_server.listen(8888)
		tornado.ioloop.IOLoop.instance().start() 
