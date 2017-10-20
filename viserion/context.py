# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

from .request import Request
from .response import Response


class Context:

    def __init__(self, environ):
        self.request= Request(environ)
        self.response = Response()
