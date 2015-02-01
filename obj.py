#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import re

import config

from config import logging
from myurllib import quote, unquote
from lib.utils import formatbytes


class Table(object):
    """sorted(iterable, [cmp=None], [key=None], [reverse=False])"""
    def __init__(self, netloc, *cachedirs):
        logging.debug(netloc)
        Loc.www = 'www.' if netloc.startswith('www.') else ''
        self.netloc = Netloc(quote(netloc.encode('utf-8'))\
                             .replace('%3F','?'))
        logging.debug(self.netloc)
        self.cacheloc = self.netloc.converted
        self.title = os.path.split(self.cacheloc)[0] + os.sep + '*.*'
        self.dirscount = 0
        self.filescount = 0
        self.sum_size = 0
        self.rows = []
        self.rows.append(('/' + self.cacheloc.parent.converted,
                          '[..]',
                          '[DIR]',
                          ''))
        self.listcache = self.cacheloc.listdir(*cachedirs)
        for cacheitem in self.listcache.keys():
            if cacheitem.isdir:
                netitem = cacheitem.converted.encode('utf-8')
                a_href = '/' + netitem.replace('?', '%3F')
                a_text = '[%s]' % unquote(
                    netitem.split('/')[-(1 + netitem.endswith('/'))])
                self.rows.append((a_href, a_text, '[DIR]', ''))
                self.dirscount += 1
            else:
                a_href = cacheitem.converted.url
                netfile = a_href.split('?', 1)[1] if '?' in a_href else \
                          a_href.split('/')[-1]
                a_text = unquote(netfile.encode('utf-8')) if netfile else \
                         'INDEX'
                fpath = cacheitem.getabspath(self.listcache[cacheitem][0])
                size = os.path.getsize(fpath)
                self.sum_size += size
                fsize = formatbytes(size, config.formatbytes)
                ftime = datetime.datetime.fromtimestamp(
                    os.path.getmtime(fpath))\
                    .strftime(config.formattime)
                self.rows.append((a_href, a_text, fsize, ftime))
                self.filescount += 1
        self.rows.sort()
        self.sum_fsize = formatbytes(self.sum_size, config.formatbytes)


class Loc(unicode):
    www = ''


class Netloc(Loc):
    """An object that represents a URL with the scheme part trimmed."""
#    def __new__(cls, arg):
#        """
#        Topic written by Guido on overriding the __new__ method:
#        http://www.python.org/download/releases/2.2.3/descrintro/#__new__
#        """
#        self = unicode.__new__(cls, arg)
#        if arg.startswith('www.'):
#            Loc.www = 'www.'
#        return self

    @property
    def converted(self):
        """Returns self converted into a Cacheloc instance."""
        c = self[len(self.www):]
        c = self.__class__.mutate(c)
        if '?' in c:
            path, query = c.split('?', 1)
            c = '^/'.join((path, query.replace('/','#%')\
                                      .replace('?','#^')))
        c = c.replace('!','#I')\
             .replace('*','#x')\
             .replace('|','#i')\
             .replace(':','!')\
             .replace('//','/~')\
             .replace('/',os.sep)
        if c.endswith(os.sep):
            c += '#_'
        c = Cacheloc(c)
        return c

    @property
    def url(self):
        return 'http://' + self

    @staticmethod
    def mutate(string, rules=config.url_to_cache):
        """Transform netloc"""
        for pattern, repl, multi in rules:
            result = pattern.search(string)
            if result is not None:
                assert len(result.groups()) < 10
                for i, group in enumerate(result.groups()):
                    if not group:
                        repl = repl.replace('\\' + str(i + 1), '')
                count = not multi
                string = pattern.sub(repl, string, count)
        return string


class Cacheloc(Loc):
    """An object that represents a relative path starting from the
    inside of a cache directory."""
    @property
    def converted(self):
        """Returns self converted into a Netloc instance"""
        n = self.replace(os.sep,'/')\
                .replace('^/','?')\
                .replace('#^','?')\
                .replace('#x','*')\
                .replace('#%','/')\
                .replace('/~','//')\
                .replace('!',':')\
                .replace('#i','|')\
                .replace('#I','!')\
                .replace('#_','')\
                .replace('#m','')
        n = Netloc(self.www + self.__class__.mutate(n))
        return n

    def getabspath(self, cachedir):
        return os.path.join(cachedir, self)
        
    #TODO: make it a @staticmethod
    def listdir(self, *cachedirs):
        """Returns a dict where each key is a Cacheloc object
        and it's value is a list of only those cache dirs
        where the key object is found.

        {cacheloc:[*cachedirs],
         .
         .
         .
        }
        """
        listcache = {}
        for cachedir in cachedirs:
            absfolder = os.path.join(cachedir, self.dirname)
            if os.path.exists(absfolder) and os.path.isdir(absfolder):
                for entry in os.listdir(absfolder):
                    if os.path.isdir(os.path.join(absfolder, entry)):
                        entry += os.sep
                    key = self.__class__(os.path.join(self.dirname, entry))
                    listcache[key] = listcache.get(key, []) + [cachedir]
        return listcache

    @property
    def dirname(self):
        return self.__class__(os.path.dirname(self))

    @property
    def parent(self):
        components = self.split(os.sep)
        return self.__class__(os.sep.join(components[:-2] + ['']))

    @property
    def islost(self):
        return self.converted.converted != self

    def regainlost(self, cachedir):
        # synonyms: restore recover repair
        # got to find proper place for this method
        # maybe it's in the Table class
        pass

    @property
    def isdir(self):
        return self.endswith(os.sep)

#    @staticmethod
#    def mutate(string):
#        """Transform cacheloc back into netloc"""
#        try:
#            dom_1, _, dom_2, dom_3, pth = string.split('/', 4)
#            assert _.startswith('#-')
#            dom = dom_1.split('.') + [dom_2] + dom_3.split('.')
#            dom.reverse()
#            dom = '.'.join(dom)
#            if dom.startswith('www.'):
#                dom = dom[4:]
#            string = '/'.join((dom, pth))
#        except:
#            pass
#            #return False
#        return string

    @staticmethod
    def mutate(string):
        """Transform cacheloc back into netloc"""
        try:
            dom_1, dom_2, pth = string.split('/', 2)
            assert dom_1.find('.') > 0
            dom = dom_1.split('.') + dom_2.split('.')
            dom.reverse()
            dom = '.'.join(dom)
            if dom.startswith('www.'):
                dom = dom[4:]
            string = '/'.join((dom, pth))
        except:
            pass
            #return False
        return string

