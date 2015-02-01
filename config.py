#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement

import os
import re
import logging

logging.basicConfig(level=logging.DEBUG)

from ConfigParser import ConfigParser

# edit the line below if needed
hc_home = r'd:\Progs\HC'

hc_ini_file = os.path.join(hc_home, 'HandyCache.ini')
hc_ini = ConfigParser()
hc_ini.readfp(open(hc_ini_file))

options = ['CacheDir_Text', 'CacheDir2_Text',
           'CacheDir02_Text', 'CacheDir22_Text',]

cache_dirs = []
for option in options:
    value = hc_ini.get('TMainForm', option)
    if value.lower() == 'cache':
        value = os.path.join(hc_home, value)
    cache_dirs.append(value)
logging.info('cache dirs are %s' % cache_dirs)

is_set2_active = hc_ini.getboolean('TMainForm', 'CacheDirSet2_Checked')

if is_set2_active:
    active_dirs = cache_dirs[2:]
    logging.info('cache dir set #2 is active')
else:
    active_dirs = cache_dirs[:2]
    logging.info('cache dir set #1 is active')
logging.info('active dirs are %s' % active_dirs)


formatbytes={'forcekb' : True,
             'largestonly' : True,
             'kiloname' : 'K',
             'meganame' : 'M',
             'bytename' : '',
             'nospace' : True}

# http://docs.python.org/lib/module-time.html
formattime = '%Y-%m-%d %H:%M'


def parselst(lst_file):
    """result: [[pattern, repl, multi], ...]"""
    rules = []
    with open(lst_file, 'r') as lst_file:
        lines = lst_file.readlines()[1:]
    for line in lines:
        line = line.split('#~#')
        if line[0] == 'True' and line[4] == 'True':
            rule = line[1:4]
            rule[0] = rule[0].replace('(?>', '(?:')
            try:
                rule[0] = re.compile(rule[0])
            except:
                logging.debug('"%s" has failed to compile' % rule[0])
            else:
                rule[2] = rule[2] == 'True'
                rules.append(rule)
    return rules

url_to_cache = parselst(os.path.join(hc_home, 'URLToCache.lst'))


