# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)
import threading

import re

from viserion.context import Context
from viserion.descriptors import CachedProperty
from viserion.exception import HTTPError, RouteError
from viserion.globals import LocalStorage


class Viserion:

    def __init__(self):
        self.route_processors = []
        self.request_middlewares = []
        self.response_middlewares = []
        self.exception_handlers = {}
        self.identify = str(threading.current_thread().ident)

    def __call__(self, environ, start_response):
        ctx = Context(environ)
        LocalStorage.push(self.identify, ctx)
        matched = False
        override = False
        try:
            for pattern, method, func in self.processors:
                if pattern is None:
                    result = func()
                    if result is not None:
                        ctx.response.body = result
                        override = True
                        break
                else:
                    match = pattern.match(ctx.request.path)
                    if match:
                        matched = True
                        if ctx.request.method not in method:
                            raise HTTPError(405)
                        else:
                            ctx.response.body = func(**match.groupdict())

            if not matched and not override:
                raise HTTPError(404)

        except HTTPError as e:
            ctx.response.status = e.args[0]
            ctx.response.body = ctx.response.status_detail
            status_code = str(ctx.response.status)
            if status_code in self.exception_handlers:
                self.exception_handlers[str(status_code)]()
        finally:
            status = ctx.response.status_result
            header = ctx.response.headers_result
            body = ctx.response.body_result
            start_response(status, header)
            return [body.encode('utf-8')]

    def exception(self, status_code):
        def _decorator(func):
            self.exception_handlers[str(status_code)] = func
        return _decorator

    @CachedProperty
    def processors(self):
        processors = []
        processors.extend(self.request_middlewares)
        processors.extend(self.response_middlewares)
        processors.extend(self.route_processors)
        return processors

    def middleware(self, middleware_type):
        def _decorator(func):
            if middleware_type == 'response':
                self.response_middlewares.extend([(None, None, func)])
            else:
                self.request_middlewares.extend([(None, None, func)])
        return _decorator

    def route(self, path, methods=None):
        if methods is None:
            methods = ['GET']
        def _decorator(func):
            pattern = re.compile(
                re.sub(r':(?P<params>[a-z_]+)',
                       lambda m: '(?P<{}>[a-z0-9-]+)'.format(m.group('params')), path).rstrip('/') + '/$'
            )
            if pattern in map(lambda i: i[0], self.route_processors):
                raise RouteError('Route {} repeat defining'.format(path))
            self.route_processors.append((pattern, methods, func))
        return _decorator

    def get(self, path):
        return self.route(path, methods=['GET'])

    def post(self, path):
        return self.route(path, methods='POST')

    def put(self, path):
        return self.route(path, methods=['PUT'])

    def patch(self, path):
        return self.route(path, methods=['PATCH'])

    def delete(self, path):
        return self.route(path, methods=['DELETE'])

    def option(self, path):
        return self.route(path, methods=['OPTION'])

    def head(self, path):
        return self.route(path, methods=['HEAD'])

    def listen(self, port):
        from wsgiref.simple_server import make_server
        server = make_server('localhost', port, self)
        print('Serving on 127.0.0.1:{port}'.format(port=port))
        server.serve_forever()
