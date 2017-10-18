# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)


_RESPONSE_STATUES = {
    # Redirection
    301: 'Moved Permanently',
    302: 'Found',
    304: 'Not Modified',

    # Client Error
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',

    # Server Error
    500: 'Internal Server Error'
}

class Response(object):

    def __init__(self):
        self._status = '200 OK'
        self._headers = {'CONTENT-TYPE': 'text/html; charset=utf-8'}

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        status = _RESPONSE_STATUES.get(value, '')
        self._status = '%d %s' % (value, status)

    @property
    def headers(self):
        """
        [(key1, value1), (key2, value2), ...]
        :return: list of tuples
        """
        L = [(k, v) for k, v in self._headers.iteritems()]
        if hasattr(self, '_cookies'):
            for v in self._cookies.itervalues():
                L.append(('Set-Cookie', v))
        return L

    def header(self, name, value=None):
        if value:
            self._headers[name] = value
        else:
            return self._headers[name]

    def set_cookie(self, name, value, max_age=None):
        if not hasattr(self, '_cookies'):
            self._cookies = {}
        L = ['%s=%s' % (name, value)]
        if isinstance(max_age, int):
            L.append('Max-Age=%d' % max_age)
        self._cookies = '; '.join(L)