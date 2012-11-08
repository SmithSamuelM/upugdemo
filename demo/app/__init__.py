""" Initialize web application package """

import sys
import os
from os import path
import bottle

BASE_PATH = '/demo' # application base, proxy forwards anything starting with this

# Common JavaScript libraries ../libs/js    /japn/static/libs/js
STATIC_LIBS_PATH =  path.join(
                        path.join(
                            path.dirname(
                                path.dirname(
                                    path.dirname(path.abspath(__file__)))),
                        'libs'),
                    'web')

# Application specific Static files ./files  /japn/static
STATIC_FILES_PATH = path.join(
                        path.dirname(path.abspath(__file__)),
                    'files')


app = bottle.default_app() #create jofa app

@app.route('%s%s' % (BASE_PATH, '/test')) # http://localhost:8082/japn/test
def testGet():
    """ Test that we are getting proxied ok to the prefix"""
    bottle.response.set_header('content-type', 'text/plain')
    content =  "Web app is located at %s" % \
        os.path.dirname(os.path.abspath(__file__))
    return content

# import ends before files so ends routes take precedence
import ends # dynamic rest endpoint package i
import files #static file package    

