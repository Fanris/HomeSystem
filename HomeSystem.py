#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2012-11-24 14:09
@summary: Python UDP listener
@author: Martin Predki
'''

# Imports for Pyrowl
from pyrowl import Pyrowl

# Udp Listener
from UdpListener import UdpListener

# GPIO
from GPIO import GPIOController

# SubProcessHandler
from SubProcess import SubProcessController

# Twisted
from twisted.internet import reactor

import logging
import json


def main():
    HomeSystem()


class HomeSystem(object):
    '''
    @summary: Main class.
    '''

    def __init__(self):
        # Initialize Logger
        self.initializeLogger()

        # Setup pyrowl with API key
        self.logger.info("Initialisiere HomeSystem")
        self.p = Pyrowl("61d552cdbd5ed63e5590ea0ef0cd6665508f6406")
        self.ausf_programm = "espeak -v de "
        self.data = " \"Dies ist ein test\""

        # Setup SubProcessHandler
        self.logger.info("Initialisiere SubProcessHandler")
        self.subProcessController = SubProcessController()

        # Setup Udp Listener
        self.logger.info("Initialisiere Udp Listener")
        self.udpListener = UdpListener(2000, self)
        self.udpListener.startListener()

        # Setup GPIO
        self.logger.info("Initialisiere GPIO Controller")
        self.gpio = GPIOController()
        self.gpio.startGPIOLoop(self.reactToGPIOFlank)

        # Setting up twisted
	try:
	    reactor.addSystemEventTrigger("before", "shutdown", self.stop)
            reactor.run()
	except KeyboardInterrupt:
	    self.logger.info("Stopping HomeSystem")
	    reactor.stop()

    def reactToGPIOFlank(self, pin):
        '''
        @summary: Is called when a GPIO-Pin changes its value
        @param pin: the pin which changed its value
        @result:
        '''
        if pin == 0:
            self.logger.info("Licht Bad und Rollade")
            self.subProcessController.startProcess("wget",
                "http://192.168.191.10:80/rasp_4_toilette.ssi",
                "--http-user=admin",
                "--http-password=wago",
                "q")

        if pin == 3:
            self.logger.info("Licht Wohnzimmer und Musik")
            self.subProcessController.startProcess("wget",
                "http://192.168.191.10:80/rasp_3_licht_musik.ssi",
                "--http-user=admin",
                "--http-password=wago",
                "q")
            self.p.push("Raspi", 'Haus', 'Test', batch_mode=False)

        if pin == 4:
            self.logger.info("Licht Wohnzimmer und Fernseher")
            self.subProcessController.startProcess("wget",
                "http://192.168.191.10:80/rasp_2_fernseher.ssi",
                "--http-user=admin",
                "--http-password=wago",
                "q")

            self.subProcessController.startProcess("wget",
                "http://192.168.191.9/web/powerstate?newstate=4")

    def messageReceived(self, data, host, port):
        '''
        @summary: parses the message.
        @param clientId: The client who send the message
        @param data: the data containing the command informations in json format
        @result:
        '''

        # Command Parser
        # ===================================
        # self.logger.debug("Message received: {}".format(data))
        # commandDict = json.loads(data)

        # # Run command....
        # self.logger.debug("Run command {}".format(commandDict.get("command", None)))
        # if hasattr(self, commandDict.get("command", None)):
        #     getattr(self, commandDict.get("command", None))(commandDict)
        # else:
        #     self.logger.warning("Command {} is not defined.".format(commandDict.get("command")))

        self.voice(data)

    def voice(self, data):
        # message = data.get("data", "")
        self.subProcessController.startProcess("espeak", "v", "de", data)

    def stop(self):
	self.gpio.stopGPIOLoop()

    def initializeLogger(self, debug=False):
        '''
        @summary: Initializes the logger
        @param workingDir:
        @param args:
        @result:
        '''
        self.logger = logging.getLogger("HomeSystem")
        ch = logging.StreamHandler()

        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        # create formatter
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s]: %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        self.logger.addHandler(ch)

if __name__ == '__main__':
    main()
