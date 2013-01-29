""" Static files """
__all__ = []

from os import path
import bottle

import myapp 

app = myapp.app #get app from myapp package.

# Common JavaScript libraries .  ../../../libs/web 
STATIC_LIBS_PATH =  path.join(
                        path.join(
                            path.dirname(
                                path.dirname(
                                    path.dirname(
                                        path.dirname(path.abspath(__file__))))),
                        'libs'),
                    'web')

# Application specific Static files ./
STATIC_FILES_PATH = path.dirname(path.abspath(__file__))


#catch all for page refreshes of any app url
@app.route('/app/<path:path>') # /demo/app/<path>
@app.route('/app') # /demo/app
def appGet(path=''):
    return bottle.static_file('app.html', root=STATIC_FILES_PATH)

@app.route('/static/favicon.ico') 
def faviconGet():
    return bottle.static_file('favicon.ico', root=STATIC_FILES_PATH)

@app.route('/static/libs/<filepath:path>')
def staticFilesGet(filepath):
    return bottle.static_file(filepath, root=STATIC_LIBS_PATH)

@app.route('/static/files/<filepath:path>')
def staticLibsGet(filepath):
    return bottle.static_file(filepath, root=STATIC_FILES_PATH)

@app.route('/bootstrap') # /demo/app
def appGet(path=''):
    return bottle.static_file('bootstrap.html', root=STATIC_FILES_PATH)
