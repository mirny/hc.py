#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib

quote = urllib.quote

def unquote(s):
    s = urllib.unquote_plus(s)
    try:
        s = s.decode('utf-8')
    except UnicodeDecodeError:
        import locale
        _, sys_encoding = locale.getdefaultlocale()
        s = s.decode(sys_encoding)
    return s

