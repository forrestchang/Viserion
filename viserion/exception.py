# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)


class ViException(Exception):
    """Super class of all Viserion exceptions."""
    pass


class RouteError(ViException):
    pass


class HTTPError(ViException):
    pass


def abort(status_code):
    raise HTTPError(status_code)
