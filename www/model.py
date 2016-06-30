#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-25 14:55:17
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, TextField, FloatField
import time, uuid

class User(Model):
    """docstring for User"""
    __table__ = 'users'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(updatable=True, ddl='varchar(50)')
    password = StringField(ddl='varchar(20)')
    admin = BooleanField()
    name = StringField(ddl='varchar(20)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(updatable=False, default = time.time)

class Blog(Model):
    """docstring for Blog"""

    __table__ = 'blogs'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(updatable = False, ddl='varchar(50)')
    user_name = StringField(ddl = 'varchar(50)')
    user_image = StringField(ddl = 'varchar(500)')
    name = StringField(ddl = 'varchar(50)')
    summary = StringField(ddl = 'varchar(200)')
    content = TextField()
    created_at = FloatField(updatable = False, default = time.time)

class Comment(Model):
    """docstring for Comment"""
    __table__ = 'comments'
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    blog_id = StringField(updatable = False, ddl='varchar(50)')
    user_id = StringField(updatable = False, ddl='varchar(50)')
    user_name = StringField(ddl = 'varchar(50)')
    user_image = StringField(ddl = 'varchar(500)')
    content = TextField()
    created_at = FloatField(updatable = False, default = time.time)




