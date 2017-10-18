# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

from .response import _RESPONSE_STATUES
from .virserion import ctx


def error(code):
    status = '%d %s' % (code, _RESPONSE_STATUES[code])
    ctx.response.status = status
    template = '<html><body><h1>{}</h1></body></html>'
    return template.format(status)


def redirect(code, location):
    error(code)
    ctx.response.header('Location', location)
    return ''