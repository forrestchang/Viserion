# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)
import mimetypes
import os

from .virserion import ctx


def _static_file_generator(path):
    BLOCK_SIZE = 1024 * 8
    with open(path, 'rb') as f:
        block = f.read(BLOCK_SIZE)
        while block:
            yield block
            block = f.read(BLOCK_SIZE)


def static_file(path):
    ext = os.path.splitext(path)[1]
    ctx.response.header('CONTENT-TYPE', mimetypes.types_map.get(ext.lower(), 'application/octet-stream'))
    return _static_file_generator(path)
