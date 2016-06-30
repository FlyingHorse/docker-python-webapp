#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-27 14:02:08
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import time, logging,hashlib

from transwarp.web import get, view, ctx, interceptor,post
from model import User, Blog, Comment

from apis import api, APIValueError, APIError, APIPermissionError, APINotFoundError

logging.basicConfig(level=logging.INFO)

@view('test_users.html')
@get('/')
def test_users():
    users = User.find_all()
    return dict(users = users)


@api
@post("/api/users")
def register_user():
    i = ctx.request.input(name='',email='', password='')
    name = i.name.strip()
    email = i.email.strip()
    password = i.password
    if not name:
        raise APIValueError('name')
    if not email or not email_valid(email):
        raise APIValueError('email')
    if not password or not password_valid(password):
        raise APIValueError('password')

    user = User.find_first('where email=?', email)
    if user:
        raise APIError('registered failed', 'email', 'Email is already in use')

    user = User(name = name, email = email, password = password, image = 'about:blank')
    user.insert()
    return user

def email_valid(email):
    return True

def password_valid(password):
    return True

_COOKIE_NAME = 'token'
_COOKIE_KEY = 'seed'

@api
@post('/api/authenticate')
def authenticate():
    i = ctx.request.input()
    email = i.email.strip()
    password = i.password
    user = User.find_first('where email = ?', email)

    if user is None:
        raise APIPermissionError('invalid email. please sign up first')
    elif user.password != password:
        raise APIPermissionError('password not correct')
    max_age = 604800
    cookie = make_signed_cookie(user.id, user.password, max_age)
    logging.info('cookie  %s:%s' % (_COOKIE_NAME, cookie))
    ctx.response.set_cookie(_COOKIE_NAME, cookie, max_age = max_age)
    user.password = '********'
    return user

def make_signed_cookie(id, password, max_age):
    expires = str(int(time.time() + max_age))
    L = [id, expires, hashlib.md5('%s-%s-%s-%s' % (id, password, expires, _COOKIE_KEY)).hexdigest()]
    return '-'.join(L)

@interceptor('/')
def user_interceptor(next):
    logging.info('user_interceptor')
    user = None
    cookie = ctx.request.cookies.get(_COOKIE_NAME)
    if cookie:
        logging.info('cookie %s' % cookie)
        user = parse_signed_cookie(cookie)
        logging.info('user in cookie: %s' % user)
    ctx.request.user = user
    return next()

def parse_signed_cookie(cookie_str):
    try:
        L = cookie_str.split('-')
        logging.info('cookie split len:%d, %s' % (len(L), L))
        if len(L) != 3:
            return None
        id, expires, md5 = L
        logging.info('id in cookie: %s' % id)
        if int(expires) < time.time():
            logging.info('expire')
            return None
        user = User.get(id)
        logging.info('user get by id: %s' % user)
        if user is None:
            return None
        if md5 != hashlib.md5('%s-%s-%s-%s' % (id, user.password, expires, _COOKIE_KEY)).hexdigest():
            return None
        return user
    except:
        return None

@api
@post('/api/blogs')
def api_create_blog():
    i = ctx.request.input(name='', summary='', content='')
    name = i.name.strip()
    summary = i.summary.strip()
    content = i.content.strip()

    user = ctx.request.user
    blog = Blog(user_id = user.id, user_name = user.name, name = name, summary = summary, content = content)
    blog.insert()
    return blog

@api
@get('api/blogs')
def api_get_blogs():
    blogs,page = _get_blogs_by_page()
    return dict(blogs = blogs, page=page)

def _get_blogs_by_page():
    total = Blog.count_all()
    page = Page(total, _get_page_index())
    blogs = Blog.find_by('order by created_at desc limit ?,?', page.offset, page.limit)
    return blogs, page

def _get_page_index():
    page_index = 1
    try:
        page_index = int(ctx.request.get('page', '1'))
    except ValueError:
        pass
    return page_index
