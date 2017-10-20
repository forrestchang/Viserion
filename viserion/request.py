# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)
import cgi
from urllib.parse import parse_qs

import os


class File:

    def __init__(self, file, name, filename):
        self.file = file
        self.name = name
        self.filename = filename

    def _copy_file(self, fp, chunk_size=2**16):
        buffer = self.file.read(chunk_size)
        while buffer:
            fp.write(buffer)
            buffer = self.file.read(chunk_size)
        self.file.seek(self.file.tell())

    def save(self, destination, overwrite=False, chunk_size=2**16):
        if isinstance(destination, str):
            if os.path.isdir(destination):
                destination = os.path.join(destination, self.filename)
            if not overwrite and os.path.exists(destination):
                raise IOError('File exists.')
            with open(destination, 'wb') as fp:
                self._copy_file(fp, chunk_size)
        else:
            self._copy_file(destination, chunk_size)

    def __str__(self):
        return '<File {}>'.format(self.filename)

    def __repr__(self):
        return '<File {}>'.format(self.filename)