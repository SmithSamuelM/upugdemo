""" Rest endpoints
    
"""
import sys
import os.path
import json
import cStringIO
import io

import bottle
import myapp

app = myapp.app #get app from myapp package.

@app.route('/backend/test') 
def testGet():
    return dict(result='success')

