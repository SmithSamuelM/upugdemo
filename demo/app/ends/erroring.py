""" Error handling
    
"""
import json

import bottle

import japn

_debug = False
slogger, flogger = japn.wooder.getLoggers(__name__) #name logger after module

app = japn.app  #get app from japn package.


@app.error(400)
def error400(ex):
    bottle.response.set_header('content-type', 'application/json')
    return json.dumps(dict(error=ex.body))

@app.error(404)
def error404(ex):
    """ Use json 404 if request accepts json otherwise use html"""
    if 'application/json' not in bottle.request.get_header('Accept'):
        result = bottle.tonat(bottle.template(bottle.ERROR_PAGE_TEMPLATE, e=ex))
        bottle.response.set_header('content-type', 'text/html')
        return result
    
    result = dict(error=ex.body)
    bottle.response.set_header('content-type', 'application/json')    
    return json.dumps(result)


@app.error(405)
def error405(ex):
    bottle.response.set_header('content-type', 'application/json')
    #bottle.response.set_header('allow', 'POST')
    return json.dumps(dict(error=ex.body))

@app.error(409)
def error409(ex):
    bottle.response.set_header('content-type', 'application/json')
    return json.dumps(dict(error=ex.body))

