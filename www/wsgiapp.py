#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-27 14:05:31
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import logging; logging.basicConfig(level=logging.INFO)
import os

from transwarp import db
from transwarp.web import WSGIApplication, Jinja2TemplateEngine
from config import configs

db.create_engine(**configs.db)

wsgi = WSGIApplication(os.path.dirname(os.path.abspath(__file__)))

template_engine = Jinja2TemplateEngine(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
wsgi.template_engine = template_engine

import urls
wsgi.add_interceptor(urls.user_interceptor)

wsgi.add_module(urls)

if __name__ == '__main__':
    wsgi.run(9000)
