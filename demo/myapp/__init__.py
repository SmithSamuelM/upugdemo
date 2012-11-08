""" Initialize web application package """

from os import path
import bottle

BASE_PATH = '/demo' # application base, proxy forwards anything starting with this

app = bottle.default_app() #create app

@app.route('/test') # http://localhost:8080/test
def testGet():
    """ Test endpoint"""
    bottle.response.set_header('content-type', 'text/plain')
    content =  "Web app is located at %s" % path.dirname(path.abspath(__file__))
    return content

# import ends before files so ends routes take precedence
import ends # dynamic rest endpoint package
import files #static file package    

app.mount(BASE_PATH, app) #remount app to be behind BASE_PATH for proxy
# http://localhost:8080/demo/test