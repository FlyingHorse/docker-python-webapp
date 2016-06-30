#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-27 17:46:50
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from model import User, Blog, Comment

from transwarp import db

db.create_engine(user='root', password='root', database='awesome')

u = User(name='Test2', email='test2@example.com', password='1234567890', image='about:blank')

#u.insert()

#print 'new user id:', u.id

u1 = User.find_first('where email=?', 'test1@example.com')
print 'find user\'s name:', u1.name

#u1.delete()

u2 = User.find_first('where email=?', 'test@example.com')
print 'find user:', u2
