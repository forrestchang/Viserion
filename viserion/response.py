# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)


_RESPONSE_STATUES = {
    "100": "Continue",
    "101": "Switching Protocols",
    "102": "Processing",
    "200": "OK",
    "201": "Created",
    "202": "Accepted",
    "203": "Non-Authoritative Information",
    "204": "No Content",
    "205": "Reset Content",
    "206": "Partial Content",
    "207": "Multi-Status",
    "300": "Multiple Choices",
    "301": "Moved Permanently",
    "302": "Found",
    "303": "See Other",
    "304": "Not Modified",
    "305": "Use Proxy",
    "306": "Switch Proxy",
    "307": "Temporary Redirect",
    "400": "Bad Request",
    "401": "Unauthorized",
    "403": "Forbidden",
    "404": "Not Found",
    "405": "Method Not Allowed",
    "406": "Not Acceptable",
    "407": "Proxy Authentication Required",
    "408": "Request Timeout",
    "409": "Conflict",
    "410": "Gone",
    "411": "Length Required",
    "412": "Precondition Failed",
    "413": "Request Entity Too Large",
    "414": "Request-URI Too Long",
    "415": "Method Not Allowed",
    "416": "Requested Range Not Satisfiable",
    "417": "Expectation Failed",
    "418": "I'm a teapot",
    "421": "There are too many connections from your internet address",
    "422": "Unprocessable Entity",
    "423": "Locked",
    "424": "Failed Dependency",
    "425": "Unordered Collection",
    "426": "Upgrade Required",
    "449": "Retry With",
    "451": "Unavailable For Legal Reasons",
    "500": "Internal Server Error",
    "501": "Not Implemented",
    "502": "Bad Gateway",
    "503": "Service Unavailable",
    "504": "Gateway Timeout",
    "505": "HTTP Version Not Supported",
    "506": "Variant Also Negotiates",
    "507": "Insufficient Storage",
    "509": "Bandwidth Limit Exceeded",
    "510": "Not Extended",
    "550": "Permission denied"
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