# -*- coding: utf-8 -*-
import os
ONBAE=False

if 'SERVER_SOFTWARE' in os.environ:
	ONBAE=True
else:
	ONBAE=False

if ONBAE :
	from bae.core import const
	mydb={	'user':const.MYSQL_USER,
			'password':const.MYSQL_PASS,
			'host':const.MYSQL_HOST,
			'port':const.MYSQL_PORT,
			'dbname':"your dbname",
			'encode':"utf8"}
else:
	mydb={	'host':'localhost',
			'port':'3306',
			'dbname':'mydb',
			'user':'mydb',
			'password':'123456',
			'encode':'utf8'	}

DBURL='mysql://%s:%s@%s:%d/%s?charset=%s'%(mydb['user'],mydb['password'],mydb['host'],int(mydb['port']),mydb['dbname'],mydb['encode'])
SKIP=10;
SMASK='sd0qd@#S#$#FD#$%DFSFSDFDSFSF'
POSTKEY='1SDFSDF#$R#@SFDR#21sf'

