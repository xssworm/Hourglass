#_*_ coding:UTF-8 _*_
import tornado.web
class ArtList(tornado.web.UIModule):
	def render(self,article):
		text=text[0:110]+'...'
		article.content=markdown.markdown(text)
		return self.render_string("themes/artlist.html",article=article)

class Article(tornado.web.UIModule):
	def render(self,article):
		markdown.markdown(text,['codehilite'])
		article.content=markdown.markdown(text)
		return self.render_string("themes/artlist.html",article=article)
