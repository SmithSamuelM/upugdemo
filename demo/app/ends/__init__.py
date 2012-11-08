""" Rest endpoint package """

__all__ = ['erroring', 'viewing']

import bottle

import japn # need this so can reference japn.app later

_debug = False
slogger, flogger = japn.wooder.getLoggers(__name__) #name logger after module

#get app from japn package.
app = japn.app

#now import ends modules
import erroring
import viewing
