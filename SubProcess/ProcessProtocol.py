# -*- coding: utf-8 -*-
'''
Created on 2012-09-24 15:00
@summary: Protocol class for server side compile processes
@author: Martin Predki
'''
from twisted.internet import protocol

class ProcessProtocol(protocol.ProcessProtocol):
    '''
    @summary: Protocol class for job processes
    '''

    def __init__(self, processName, processHandler):
        self.processName = processName
        self.processHandler = processHandler
        self.stdOut = []
        self.errOut = []

    def outReceived(self, data):
        self.stdOut.append(data)

    def errReceived(self, data):
        self.errOut.append(data)

    def processEnded(self, status):
        self.stdOutput.close()
        self.errOutput.close()

        if status.value.exitCode == 0:
            self.processHandler.processCompleted(self.processName)
        else:
            self.processHandler.processFailed(self.processName)

    def kill(self):
        self.transport.signalProcess('KILL')
