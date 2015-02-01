#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import config
from obj import Table


urls = ('/favicon.ico$', 'Favicon',
        '/([a-z\-]+\.css)$', 'Style',
        '(/(?:[^/]+\.\w{2,4}/.*)?)', 'Index',)

app = web.application(urls, globals())
render = web.template.render('templates')


class Favicon:
    def GET(self):
        web.header("Content-Type","image/x-icon")
        return open('static/favicon.gif', 'rb').read()


class Style:
    def GET(self, fname):
        web.header("Content-Type","text/css")
        return open('static/' + fname, 'r').read()


class Index:
    def GET(self, netloc):
        web.header("Content-Type","text/html; charset=utf-8")
        table = Table(netloc.lstrip('/'), *config.cache_dirs)
        return render.a(table)


if __name__ == '__main__':
    app.run()

