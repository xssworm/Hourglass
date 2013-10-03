# -*- coding: utf-8 -*-
from orebase import *
import hashlib
import markdown
from setting import SMASK,POSTKEY,SKIP
from sqlalchemy import desc,and_,exists
se=getSession()
#查询单篇文章

def show_article(url):
	article=se.query(Article).filter(Article.url==url).first()
	article.vis=article.vis+1
	se.commit()
	article=se.query(Article).filter(Article.url==url).first()
	se.close()
	return article

#查询所有文章
def show_all(sid,Rss=False):
	if Rss==True:
		article=se.query(Article).order_by(desc('date')).all()
	else:
		article=se.query(Article).order_by(desc('date')).limit(SKIP).offset(sid*SKIP).all()
	se.close()
	return article

#通过标签查找文章
def show_bytags(tag):
	article=se.query(Article).filter(and_(Article.pid==TagPost.pid,TagPost.tid==Tags.tid,Tags.name==tag))
	article=article.order_by(desc('date')).all()
	se.close()
	return article

#通过分类查找文章
def show_bycategory(category):
	article=se.query(Article).filter(and_(Article.cid==Category.cid,Category.name==category))
	article=article.order_by(desc('date')).all()
	se.close()
	return article
	
#获取所有分类
def getcategory():
	category=se.query(Category).all()
	se.close()
	return category

#获取所有标签
def gettags():
	tags=se.query(Tags).all()
	se.close()
	return tags
	
#获取文章，标签关系
def gettagpost():
	tp=se.query(TagPost).all()
	se.close()
	return tp

#添加一个分类信息,返回分类的cid
def addcategory(category):
	cate=se.query(Category).filter(Category.name==category).first()#cid是一个元组
	if cate is None:
		cate=Category(category)
		se.add(cate)
	else:
		cate.count=cate.count+1
	se.commit()
	cid=cate.cid
	return cid

#添加一个标签
#pid为文章的id号,默认为None,表示不添加文章和标签的关系
def addtags(tags,pid=None):
	for tt in tags:
		tid=se.query(Tags).filter(Tags.name==tt).first()
		if tid is None:
			tag=Tags(tt)
			se.add(tag)
			se.commit()
			tid=tag.tid
		else:
			tid.count=tid.count+1
			se.commit()
			tid=tid.tid
		if pid is not None:#关联文章ID是否存在
			tp=TagPost(pid,tid)
			se.add(tp)

#删除一个标签
#如果指定文章的pid,则删除该文章和标签的关系,否则删除所有
def deltags(tags,pid=None):
	for tt in tags:
		if pid is None:
			se.delete(TagPost).filter(and_(tt==Tags.name,Tags.tid==TagPost.tid)).all()
			se.delete(Tags).filter(Tags.name==tt).first()
		else:
			tags=se.query(Tags).filter(Tags.name==tt).first()
			tags.count=tags.count-1
			tr=se.query(TagPost).filter(and_(tt==Tags.name,Tags.tid==TagPost.tid,TagPost.pid==pid)).first()
			if tr is not None:
				se.delete(tr)
	se.commit()


def insert(art):
	myart=se.query(Article).filter(Article.url==art.url).first()#查询文章的信息
	if myart is None:
		art.cid=addcategory(art.category)
		se.add(art)
		se.commit()
		pid=art.pid
		addtags(art.tags,pid)
	else:
		if(cmp(art.category,myart.category)!=0):
			myart.cid=addcategory(art.category)#获取标签ID
			category=se.query(Category).filter(Category.cid==myart.cid).first()
			category.count=category.count-1

		myart.title=art.title
		myart.content=art.content
		pid=myart.pid
		oldtags=se.query(Tags.name).filter(and_(TagPost.pid==pid,TagPost.tid==Tags.tid)).all()
		for oldt in oldtags:
			myart.tags.append(oldt.name)
			for newt in art.tags:
				if newt==oldt.name:
					art.tags.remove(newt)
					myart.tags.remove(oldt.name)
		addtags(art.tags,myart.pid)
		deltags(myart.tags,myart.pid)
	user=se.query(User).filter(User.name=="Fluyy").first()
	tt=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	user.date=tt;
	se.commit()
	se.close()

def getChangeTime():
	user=se.query(User.date).filter(User.name=="Fluyy").first()
	se.close()
	return user.date 

#Security check
def check(key1,key2):
	#print key1
	#print key2
	#print hashlib.md5(key2.join(SMASK)).hexdigest()
	if POSTKEY!=key1:
		return False
	mypass=se.query(User).first()
	mypass=mypass.password
	se.close()
	if mypass==hashlib.md5(key2.join(SMASK)).hexdigest():
		return True
	return False

#update password
def cpassword(newkey):
	#print newkey
	user=se.query(User).filter(User.name=='Fluyy').first()
	user.password=hashlib.md5(newkey.join(SMASK)).hexdigest()
	se.commit()
	se.close()

def Topost(text):
	return markdown.markdown(text,['codehilite'])

def Toindex(text):
	text=text[0:110]+'    ...'
	return markdown.markdown(text)
