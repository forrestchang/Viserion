# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)
import os
import re

TEMPLATE_DIR = ''


def render(path, data={}):
    path = os.path.join(TEMPLATE_DIR, path)
    with open(path) as f:
        page = f.read()
    if not data:
        return page
    dirname = os.path.dirname(path)
    inc = re.compile(r'\{%\sinclude\s*(\w+(\.\w+)*)\s*%\}')
    def include(m):
        name = m.group(1)
        path = os.path.join(dirname, name)
        with open(path) as f:
            return f.read()
    page = re.sub(inc, include, page)

    ass = re.compile(r'\{\{\s*(\w+)\s*}\}')
    def assign(m):
        var_name = m.group(1)
        return str(data.get(var_name, ''))

    page = re.sub(ass, assign, page)
    return page