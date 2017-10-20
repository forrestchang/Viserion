# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)-7s %(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger('viserion')
