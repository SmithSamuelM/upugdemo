""" Static files """
__all__ = []

from os import path

import bottle

import japn 

_debug = False

slogger, flogger = japn.wooder.getLoggers(__name__) #name logger after module

app = japn.app #get app from app package.

#@app.route('%s%s' % (japn.BASE_PATH, '/app/index.html')) # /japn/japn.html
#@app.route('%s%s' % (japn.BASE_PATH, '/app/japn.html')) # /japn/index.html
#@app.route('%s%s' % (japn.BASE_PATH, '/app/home')) # /japn/home
#catchall for page refreshes of any app url
@app.route('%s%s' % (japn.BASE_PATH, '/app/<path:path>')) # /japn/app/<path>
@app.route('%s%s' % (japn.BASE_PATH, '/app')) # /japn/app
def homeGet(path=''):
    return bottle.static_file('japn.html', root=japn.STATIC_FILES_PATH)

@app.route('%s%s' % (japn.BASE_PATH, '/favicon.ico')) # /japn/favicon.ico
def faviconGet():
    return bottle.static_file('favicon.ico', root=japn.STATIC_FILES_PATH)

@app.route('%s%s' % (japn.BASE_PATH, '/static/libs/<filepath:path>'))
def staticGet(filepath):
    return bottle.static_file(filepath, root=japn.STATIC_LIBS_PATH)

@app.route('%s%s' % ( japn.BASE_PATH, '/static/files/<filepath:path>'))
def staticGet(filepath):
    return bottle.static_file(filepath, root=japn.STATIC_FILES_PATH)

