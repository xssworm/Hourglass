# -*- coding: utf-8 -*-
from sqlalchemy import Column,create_engine,CHAR ,Integer,String,Date,Text,DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from setting import DBURL,SMASK
import sqlalchemy.pool as pool
import hashlib,time

BaseModel=declarative_base()

class Article(BaseModel):#文章类
	__tablename__='post'
	pid=Column(Integer,primary_key=True)
	title=Column(String(40),nullable=False)
	date=Column(Date,nullable=False)
	cid=Column(Integer,nullable=False)
	content=Column(Text,nullable=False)
	vis=Column(Integer,nullable=False)
	url=Column(CHAR(40),nullable=False,unique=True)
	category='default'
	tags=[];
	def __init__(self):
		self.vis=0

class Category(BaseModel):#category类
	__tablename__='category'
	cid=Column(Integer,primary_key=True)
	name=Column(String(40),nullable=False,unique=True)
	count=Column(Integer,nullable=False)
	def __init__(self,cat):
		self.name=cat
		self.count=1

class Tags(BaseModel):#标签类
	__tablename__='tags'
	tid=Column(Integer,primary_key=True)
	name=Column(String(40),nullable=False,unique=True)
	count=Column(Integer,nullable=False)
	def __init__(self,tag):
		self.name=tag
		self.count=1
	
class TagPost(BaseModel):#标签与文章关系类
	__tablename__='tagpost'
	rid=Column(Integer,primary_key=True)
	tid=Column(Integer,nullable=False)
	pid=Column(Integer,nullable=False)
	def __init__(self,pid,tid):
		self.pid=pid
		self.tid=tid

class User(BaseModel):#标签类
	__tablename__='user'
	uid=Column(Integer,primary_key=True)
	name=Column(String(40),nullable=False,unique=True)
	password=Column(String(80),nullable=False)
	date=Column(DateTime,nullable=False)
	def __init__(self):
		self.name='Fluyy'
		self.date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def getSession():#获取session
	engine = create_engine(DBURL,pool_size=5,pool_recycle=5)  
	Session = sessionmaker(bind=engine)
	return Session() 


def initDatabase():#数据库初始化
	try:
		Se=getSession()
		user=Se.query(User).filter(User.name=='Fluyy').first()
	except :
		engine = create_engine(DBURL,pool_size=20,pool_recycle=1800)
		BaseModel.metadata.create_all(engine)
		user=User()
		Se=getSession()
		user.password=hashlib.md5('admin'.join(SMASK)).hexdigest()
		Se.add(user)	
		Se.commit()
	finally:
		Se.close()

