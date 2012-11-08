#!/usr/local/bin/python2.7

""" Runs bottle.py wsgi server

    Interface to Bottle application
    To get usage
    
    $ ./demoing.py -h
    

    Runs embedded wsgi server when run directly as __main__.
    The server is at http://localhost:port or http://127.0.0.1:port
    The default port is 8080
    The root path is http://localhost:port
    and routes below are relative to this root path so
    "/" is http://localhost:port/
     
"""
import sys
import os
import traceback
import argparse
import datetime

import eventlet

import bottle

#import japn
japn = eventlet.import_patched('japn')
#from japn.helps import configing

_debug = False
logger, flogger = japn.wooder.getLoggers(__name__)

if __name__ == "__main__":
    """Process command line args

        Example
        porting.py -d -p port
    """
    logging = eventlet.import_patched('logging')
    
    #map of strings to logging levels
    levels = dict(debug=logging.DEBUG, info=logging.INFO, warning=logging.WARNING,
                      error=logging.ERROR, critical=logging.CRITICAL)
    
    d = "Runs localhost wsgi service on given host address and port. "
    d += "\nDefault host:port is localhost:8082."
    p = argparse.ArgumentParser(description = d)
    p.add_argument('-d','--debug',
                    action = 'store_const',
                    const = True,
                    default = False,
                    help = "Debug mode.")
    p.add_argument('-l','--level',
                    action='store', 
                    default='warning',
                    choices=levels.keys(), 
                    help="Logging level.")        
    p.add_argument('-r','--reload',
                    action = 'store_const',
                    const = True,
                    default = False,
                    help = "Server reload mode if also in debug mode.")
    p.add_argument('-p','--port', 
                    action = 'store',
                    nargs='?', 
                    const='8082', 
                    default='8082',
                    help = "Wsgi server ip port.")
    p.add_argument('-a','--host', 
                    action = 'store',
                    nargs='?', 
                    const='localhost', 
                    default='localhost',
                    help = "Wsgi server ip host address.")
    p.add_argument('-S','--server', 
                    action = 'store',
                    nargs='?', 
                    const='paste', 
                    default='paste',
                    help = "Wsgi server type.")

    #create config file path name string
    #configfilepath = os.path.join(
        #os.path.dirname(os.path.abspath(__file__)), 'config.json')
    
    #configer = configing.Configage(dumpster=configfilepath)
    #configer.load()
     
    
    args = p.parse_args() 
    if args.debug:
        level = levels['debug']
        _debug =  True
        logger.error("Debug mode")        
    else:
        level = levels[args.level]
    
    logger.error("Log level = '%s'" % level)
    logger.setLevel(level) 
    
    logger.info("Starting wsgi server %s on %s:%s." % (args.server, args.host, args.port))

    if _debug:   #default server
        bottle.debug(True)
        bottle.run(app=japn.app,
                   host=args.host, port=args.port,
                   reloader=args.reload) 
    else:
        bottle.run(app=japn.app, server=args.server,
                   host=args.host, port=args.port)
        
    
    