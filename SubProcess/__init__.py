# -*- coding: utf-8 -*-
'''
Created on 2013-02-03 13:29
@summary:
@author: Martin
'''

from ProcessProtocol import ProcessProtocol

from twisted.internet import reactor

import logging
import os

class SubProcessController(object):
    '''
    @summary: A class to start sub processes via twisted.
    '''
    def __init__(self):
        self.logger = logging.getLogger("HomeSystem")

    def startProcess(self, executable, *params):
        '''
        @summary: Starts a new process
        @param executable: the executable to start
        @param *params: additional parameter
        @result:
        '''

        parameter = [executable]
        parameter.extend(params)
        self.logger.debug("Starte {}".format(executable))
        reactor.spawnProcess(ProcessProtocol(executable, self), executable=executable,
            args=parameter, env=os.environ)

    def processCompleted(self, processName):
        '''
        @summary: Is called when a process is completed without errors
        @param processName: the name of the process
        @result:
        '''
        self.logger.debug("{} ausgeführt".format(processName))

    def processFailed(self, processName):
        '''
        @summary: Is called when a process has ended with errors
        @param processName: the name of the process
        @result:
        '''
        self.logger.warning("{} fehlgeschlagen!".format(processName))

