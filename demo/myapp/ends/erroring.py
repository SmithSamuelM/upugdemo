""" Error handling
    
    Bottle 'error' methods do not automatically detect json when returning a dict
    so must manually jsonify
"""
import json
import bottle
import myapp

app = myapp.app  #get app from japn package.

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
    
    bottle.response.set_header('content-type', 'application/json')    
    return json.dumps(dict(error=ex.body))


@app.error(405)
def error405(ex):
    bottle.response.set_header('content-type', 'application/json')
    return json.dumps(dict(error=ex.body))

@app.error(409)
def error409(ex):
    bottle.response.set_header('content-type', 'application/json')
    return json.dumps(dict(error=ex.body))

