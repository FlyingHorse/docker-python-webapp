#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-28 13:42:45
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import json
import logging
import functools

from transwarp.web import ctx

class APIError(StandardError):
    """docstring for APIError"""
    def __init__(self, error, data='', message = ''):
        super(APIError, self).__init__(message)
        self.error = error
        self.data = data
        self.message = message

class APIValueError(APIError):
    """docstring for APIValueError"""
    def __init__(self, field, message = ''):
        super(APIValueError, self).__init__('value:invalid', field, message)

class APINotFoundError(APIError):
    def __init__(self,field,message = ''):
        super(APINotFoundError, self).__init__('value:not found', field, message)

class APIPermissionError(APIError):
    def __init__(self,message= ''):
        super(APIPermissionError, self).__init__('permission denied', 'permission', message)


def api(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        try:
            r = json.dumps(func(*args, **kw))
        except APIError, e:
            r = json.dumps(dict(error = e.error, data = e.data, message = e.message))
        except Exception, e:
            logging.exception(e)
            r = json.dumps(dict(error = 'internaleror', data = e.__class__.__name__, message = e.message))
        ctx.response.content_type = 'application/json'
        return r
    return _wrapper


class Page(object):
    """docstring for Page"""
    def __init__(self, item_count, page_index=1, page_size=10):
        self.item_count = item_count
        self.page_size = page_size
        self.page_count = item_count // page_size + (1 if item_count % page_size > 0 else 0)
        if item_count == 0 or page_index < 1 or page_index > self.page_count:
            self.offset = 0
            self.limit = 0
            self.page_index = 1
        else:
            self.page_index = page_index
            self.offset = self.page_size * (page_index - 1)
            self.limit = self.page_size
        self.has_next = self.page_index < self.page_count
        self.has_previous = self.page_index > 1

