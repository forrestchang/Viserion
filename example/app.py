# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

from viserion.application import Viserion as Vi
from viserion.globals import request, response


app = Vi()


@app.route('/', methods=['GET', 'POST'])
def hello():
    return 'Hello World'


@app.route('/environ/')
def environ():
    return str(request.environ)


def main():
    app.listen(8888)


if __name__ == '__main__':
    main()
