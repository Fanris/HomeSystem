# -*- coding: utf-8 -*-
'''
Created on 2013-02-04 20:26
@summary: Module to call Functions after a given time interval.
Uses the Twisted Package
@author: Martin Predki
'''

from twisted.internet import reactor

delayedFunctions = {}

def CallDelayed(id, delay, function, *args, **kw):
    '''
    @summary: Calls a Function after a given time
    @param id: The id is used to identify the function. With the id it is
    possible to abort the function or change the delay.
    @param delay: The delay.
    @param function: The function to call.
    @param *args: Arguments to pass to the function.
    @param **kw: keyword arguments to pass to the function.
    @result:
    '''

    delayedFunctions[id] = reactor.callLater(delay, function, *args, **kw)
    reactor.callLater(delay + 5, StopDelayed, id)

def StopDelayed(id):
    '''
    @summary: Stops the Function with the id.
    @param id: The Function id to stop
    @result:
    '''
    func = delayedFunctions.get(id, None)
    if func and func.active:
        func.cancel()

    del delayedFunctions[id]
