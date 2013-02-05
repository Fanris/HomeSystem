# -*- coding: utf-8 -*-
'''
Created on 2013-02-03 11:30
@summary:
@author: Martin Predki
'''
from twisted.internet import reactor

import wiringpi

import logging

# Global Definitions
GPIO_MODE_OUTPUT = 0
GPIO_MODE_INPUT = 1

GPIO_RISING_FLANK = 0
GPIO_FALLING_FLANK = 1
GPIO_EVERY_FLANK = 2

class GPIOController(object):
    '''
    @summary: Class for GPIO usage
    '''
    def __init__(self):
        self.logger = logging.getLogger("HomeSystem")

        self.pinConfiguration = {}
        self.stop = True

        # Set GPIO Pins
        self.io = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)

    def setGPIOPin(self, pin, callback=None, mode=None, reactToFlank=GPIO_EVERY_FLANK):
        '''
        @summary: Sets the GPIO pin to Input Mode
        @param pin: The pin number
        @param mode:
        @result:
        '''
        if mode == 1:
            self.io.pinMode(pin, self.io.INPUT)
            self.pinConfiguration[pin] = { "mode": mode, "flank": reactToFlank,
                "callback": callback}
        elif mode == 0:
            self.io.pinMode(pin, self.io.OUTPUT)
            self.pinConfiguration[pin] = { "mode": mode, "flank": reactToFlank,
                "callback": callback}


    def getGPIOInput(self):
        '''
        @summary: Gets the current GPIO input
        @result: Returns a dictionary containing the pin number as key and
        the pin value as value
        '''
        returnDict = {}
        for pin in self.pinConfiguration.keys():
            if  self.pinConfiguration[pin].get("mode", None) == 1:
                returnDict[pin] = self.io.digitalRead(pin)

        return returnDict


    def startGPIOLoop(self):
        '''
        @summary: Starts the GPIO Loop Thread.
        @param callbackFunction: A callback Function which is called when a
        flank occurs that is configured for the pin. The function gets the
        pin number as a parameter
        @result:
        '''
        self.stop = False;
        self.logger.info("Starte GPIO Loop")
        reactor.callInThread(self.GPIOLoop)

    def stopGPIOLoop(self):
        '''
        @summary: Stops the GPIO InputLoop
        @result:
        '''
        self.stop = True


    def GPIOLoop(self):
        '''
        @summary: Frequently polls the status of the GPIO pins
        @result:
        '''
        self.loopIsRunning = True
        inp = self.getGPIOInput()

        while not self.stop:
            inpNew = self.getGPIOInput()

            for i in inpNew.keys():
                if inp[i] == inpNew[i]:
                    inp = inpNew
                    continue

                if inp[i] < inpNew[i] and \
                    self.pinConfiguration[i].get("flank", None) != GPIO_RISING_FLANK:
                    inp = inpNew
                    continue

                if inp[i] > inpNew[i] and \
                    self.pinConfiguration[i].get("flank", None) != GPIO_FALLING_FLANK:
                    inp = inpNew
                    continue

                self.logger.debug("Input {} hat sich aendert: {} -> {}".format(i, inp[i], inpNew[i]))
                func = self.pinConfiguration[i].get("callback", None)
                if func:
                    func(i)

            inp = inpNew
