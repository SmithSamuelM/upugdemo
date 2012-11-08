""" Rest endpoints
    
"""
import sys
import os.path

import json
import cStringIO
import io

pythonold = True if sys.version_info[1] < 7 else False
if pythonold:
    from  ordereddict import OrderedDict as Odict
else:
    from collections import OrderedDict as Odict

import eventlet
import bottle

import japn

_debug = False
logger, flogger = japn.wooder.getLoggers(__name__)

app = japn.app #get app from japn package.

@app.route('%s%s' % (japn.BASE_PATH, '/level3/callback')) # /japn/level3/callback
def test():
    return dict(result='success')

