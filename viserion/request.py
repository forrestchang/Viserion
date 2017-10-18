# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)
import cgi
from urllib.parse import parse_qs


class Request(object):

    def __init__(self, environ):
        self._query_dict = {}
        query_dict = parse_qs(environ['QUERY_STRING'], keep_blank_values=True)
        for k, v in query_dict.iteritems():
            if len(v) == 1:
                self._query_dict = v[0]
            else:
                self._query_dict = v

        # post data
        self._post_data = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ, keep_blank_values=True)

        # cookie
        self._cookies = {}
        cookie_str = environ.get('HTTP_COOKIE')
        if cookie_str:
            cookie_dict = parse_qs(cookie_str, keep_blank_values=True)
            self._cookies = {k.strip(): v[0] for k, v in cookie_dict.iteritems()}

        # save the original environment
            self._environ = environ

    @property
    def method(self):
        return self._environ['REQUEST_METHOD']

    @property
    def path_info(self):
        return self._environ['PATH_INFO']

    def query(self, key):
        return self._query_dict.get(key, '')

    def post(self, key):
        return self._post_data.getvalue(key, '')

    def file(self, key):
        if key in self._post_data and self._post_data[key].filename:
            return self._post_data[key]
        return None

    def get_cookie(self, name):
        return self._cookies.get(name)
