""" Static files """
__all__ = []

from os import path
import bottle

import myapp 

app = myapp.app #get app from myapp package.

#catchall for page refreshes of any app url
@app.route('%s%s' % (myapp.BASE_PATH, '/app/<path:path>')) # /demo/app/<path>
@app.route('%s%s' % (myapp.BASE_PATH, '/app')) # /demo/app
def homeGet(path=''):
    return bottle.static_file('app.html', root=japn.STATIC_FILES_PATH)

@app.route('%s%s' % (myapp.BASE_PATH, '/favicon.ico')) # /demo/favicon.ico
def faviconGet():
    return bottle.static_file('favicon.ico', root=japn.STATIC_FILES_PATH)

@app.route('%s%s' % (myapp.BASE_PATH, '/static/libs/<filepath:path>'))
def staticGet(filepath):
    return bottle.static_file(filepath, root=japn.STATIC_LIBS_PATH)

@app.route('%s%s' % ( myapp.BASE_PATH, '/static/files/<filepath:path>'))
def staticGet(filepath):
    return bottle.static_file(filepath, root=japn.STATIC_FILES_PATH)

