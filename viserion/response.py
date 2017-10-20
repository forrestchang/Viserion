# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)
import json

from viserion.descriptors import HeaderDict

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

class Response:

    def __init__(self):
        self.status = 200
        self.headers = HeaderDict()
        self.body = None

    def __repr__(self):
        return '<Response {}>'.format(self.status)

    @property
    def status_detail(self):
        return _RESPONSE_STATUES.get(str(self.status))

    @property
    def status_result(self):
        return str(self.status) + ' ' + self.status_detail

    @property
    def headers_result(self):
        """
        [(key1, value1), (key2, value2), ...]
        :return: list of tuples
        """
        return [(key, val) for key, val in self.headers.items()]

    @property
    def body_result(self):
        if self.body is None:
            self.headers['Content-Length'] = 0
            return ''
        if isinstance(self.body, int):
            self.headers['Content-Length'] = 'text/html'
            return str(self.body)
        if isinstance(self.body, str):
            self.headers['Content-Length'] = 'text/html'
            return self.body
        if isinstance(self.body, dict):
            self.headers['Content-Length'] = 'text/json'
            return json.dumps(self.body)
        if isinstance(self.body, bytes):
            self.headers['Content-Length'] = 'application/octet-stream'
            return self.body
        return str(self.body)
