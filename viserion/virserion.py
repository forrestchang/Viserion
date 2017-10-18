# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)
import os
import re
import threading

from .exceptions import error
from .request import Request
from .response import Response

ctx = threading.local()


class WebApplication(object):

    def __init__(self):
        self.routers = []

    def route(self, path):
        def _decorator(func):
            func.__route__ = path + '$'
            self.routers.append(func)
            return func
        return _decorator()

    def callback(self):
        path = ctx.request.path_info
        for func in self.routers:
            m = re.match(func.__route__, path)
            if m:
                args = m.groups()
                return func(*args)
        return error(404)

    def run(self, port='8888'):
        """ Python built-in server """
        def wsgi(env, start_response):
            ctx.request = Request(env)
            ctx.response = Response()
            try:
                r = self.callback()
                if isinstance(r, str):
                    r = r.encode('utf-8')
                if not r:
                    r = error(404)
            except Exception as e:
                r = error(505)

            start_response(ctx.response.status, ctx.response.headers)
            return r

        DOCUMENT_ROOT = os.getcwd()
        from wsgiref.simple_server import make_server
        server = make_server('', port, wsgi)
        print('Sering on port: %s' % port)
        server.serve_forever()


app = WebApplication()

def route(path):
    return app.route(path)


