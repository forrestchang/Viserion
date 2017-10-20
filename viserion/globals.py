# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

import threading
from functools import partial


class LocalStorage(dict):

    thread_context_map = {}

    @classmethod
    def load_context(cls, name):
        return getattr(cls.thread_context_map[str(threading.current_thread().ident)], name)

    @classmethod
    def push(cls, identify, ctx):
        cls.thread_context_map[str(identify)]= ctx


class LocalProxy:

    def __init__(self, func):
        self.__dict__['func'] = func

    def __getattr__(self, item):
        if not hasattr(self.func(), item):
            raise AttributeError
        return getattr(self.func(), item)

    def __setattr__(self, key, value):
        if not hasattr(self.func(), key):
            raise AttributeError
        setattr(self.func(), key, value)


request = LocalProxy(partial(LocalStorage.load_context, 'request'))
response = LocalProxy(partial(LocalStorage.load_context, 'response'))
