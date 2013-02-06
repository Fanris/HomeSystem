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
import GPIO

# SubProcessHandler
from SubProcess import SubProcessController

# Scenes
import Scenes

# Delayed Caller
import DelayedCaller

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
        self.gpio = GPIO.GPIOController()
        self.setupGPIOPins()
        self.gpio.startGPIOLoop()

        # Setting up twisted
	try:
	    reactor.addSystemEventTrigger("before", "shutdown", self.stop)
            reactor.run()
	except KeyboardInterrupt:
	    self.logger.info("Stopping HomeSystem")
	    reactor.stop()

    def setupGPIOPins(self):
        '''
        @summary: Configures the GPIO Pins
        @result:
        '''
        self.gpio.setGPIOPin(0, 
            fallingFlank=self.reactToGPIOFallingFlank,
            risingFlank=self.reactToGPIORisingFlank,
            mode=GPIO.GPIO_MODE_INPUT)

        self.gpio.setGPIOPin(3, 
            fallingFlank=self.reactToGPIOFallingFlank,
            risingFlank=self.reactToGPIORisingFlank,
            mode=GPIO.GPIO_MODE_INPUT)

        self.gpio.setGPIOPin(4, 
            fallingFlank=self.reactToGPIOFallingFlank,
            risingFlank=self.reactToGPIORisingFlank,
            mode=GPIO.GPIO_MODE_INPUT)

        self.gpio.setGPIOPin(5, 
            fallingFlank=self.reactToGPIOFallingFlank,
            risingFlank=self.reactToGPIORisingFlank,
            mode=GPIO.GPIO_MODE_INPUT)

        self.gpio.setGPIOPin(6, 
            fallingFlank=self.reactToGPIOFallingFlank,
            risingFlank=self.reactToGPIORisingFlank,
            mode=GPIO.GPIO_MODE_INPUT)


    def reactToGPIOFallingFlank(self, pin):
        '''
        @summary: Is called when a GPIO-Pin changes its value
        @param pin: the pin which changed its value
        @result:
        '''
        self.logger.info("Pin {} geaendert".format(pin))
        if pin == 0:
            Scenes.Licht_Bad_Rollade()

        if pin == 3:
            Scenes.Licht_Wohnzimmer_Musik()

        if pin == 4:
            Scenes.Licht_Wohnzimmer_Fernsehr()

        DelayedCaller.StopDelayed("AllOff")

    def reactToGPIORisingFlank(self, pin):
        inp = self.gpio.getGPIOInput()
        for pin in inp.keys():
            if inp[pin] == 0:
                self.logger("{} ist 0. Tue nichts.".format(pin))
                return

        self.logger.info("Mach alles aus in 10")
        DelayedCaller.CallDelayed("AllOff", 300, function=Scenes.Alles_Aus)

    def messageReceived(self, data, host, port):
        '''
        @summary: parses the message.
        @param clientId: The client who send the message
        @param data: the data containing the command informations in json format
        @result:
        '''

        # Command Parser
        # ===================================
        self.logger.debug("Message received: {}".format(data))
        try:
            commandDict = json.loads(data)
        except ValueError:
            self.logger.warning("Kann Kommando nicht parsen: {}".format(data))
            return

        # Run command....
        self.logger.debug("Run command {}".format(commandDict.get("command", None)))
        if hasattr(self, commandDict.get("command", None)):
            getattr(self, commandDict.get("command", None))(commandDict)
        else:
            self.logger.warning("Command {} is not defined.".format(commandDict.get("command")))


    def voice(self, data):
        message = data.get("data", "")
        self.subProcessController.startProcess("espeak", "-v", "de", message)

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
