# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

from functools import update_wrapper


class CachedProperty:

    def __init__(self, func):
        update_wrapper(self, func)
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = instance.__dict__[self.func.__name__] = self.func(instance)
        return value


class DictProperty:

    def __init__(self, storage, read_only=False):
        self.storage = storage
        self.read_only = read_only

    def __call__(self, func):
        update_wrapper(self, func, updated=[])
        self.func = func
        self.name = func.__name__
        return self

    def __get__(self, instance, owner):
        if instance is None:
            return self
        storage = getattr(instance, self.storage)

        if self.name not in storage:
            storage[self.name] = self.func(instance)

        return storage[self.name]

    def __set__(self, instance, value):
        if self.read_only:
            raise AttributeError('read-only property.')
        getattr(instance, self.storage)[self.name] = value

    def __delete__(self, instance):
        if self.read_only:
            raise AttributeError('read-only property.')
        del getattr(instance, self.storage)[self.name]


class HeaderDict:

    def __init__(self):
        self.store = {}

    def __getattr__(self, item):
        return self.store.get(item, None)

    def __getitem__(self, item):
        return self.store.get(item, None)

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise ValueError('headers key must be string but get key: {}'.format(type(key)))
        self.store[key.title().replace('_', '-')] = str(value)

    def items(self):
        return self.store.items()
