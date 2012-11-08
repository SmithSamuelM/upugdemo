""" Initialize web application package """

from os import path
import bottle

BASE_PATH = '/demo' # application base, proxy forwards anything starting with this

# Common JavaScript libraries .  ../../libs/web 
STATIC_LIBS_PATH =  path.join(
                        path.join(
                            path.dirname(
                                path.dirname(
                                    path.dirname(path.abspath(__file__)))),
                        'libs'),
                    'web')

# Application specific Static files ./files 
STATIC_FILES_PATH = path.join(
                        path.dirname(path.abspath(__file__)),
                    'files')


app = bottle.default_app() #create app

@app.route('%s%s' % (BASE_PATH, '/test')) # http://localhost:8080/demo/test
def testGet():
    """ Test endpoint"""
    bottle.response.set_header('content-type', 'text/plain')
    content =  "Web app is located at %s" % path.dirname(path.abspath(__file__))
    return content

# import ends before files so ends routes take precedence
import ends # dynamic rest endpoint package
import files #static file package    

