# -*- coding: utf-8 -*-
'''
Created on 2012-11-30 13:35
@summary:
@author: Maritn Predki
'''

from twisted.internet import reactor

from UdpProtocol import UdpProtocol

import logging

class UdpListener(object):
    '''
    @summary: UDP Server class
    '''

    def __init__(self, port, receiver):
        '''
        @summary: Initializes the udp server
        @param port: The port on which the server should listen
        @result:
        '''
        self.logger = logging.getLogger("Haus")
        self.port = port
        self.protocol = UdpProtocol(self)
        self.receiver = receiver

    def startListener(self):
        '''
        @summary: Starts the server
        @result:
        '''
        self.logger.info("Starting Udp Listener.")
        reactor.listenMulticast(self.port, self.protocol, listenMultiple=True)
        return True

    def stopServer(self):
        '''
        @summary: Stops the Udp server.
        @result:
        '''
        pass

    def sendMessage(self, message, host, port):
        '''
        @summary: Sends a message
        @param message: the message to send
        @param host: the ip of the receiver
        @param port: the port of the receiver
        @result:
        '''
        # creating command
        self.protocol.sendMEssage(message)

    def messageReceived(self, message, senderIp, senderPort):
        '''
        @summary: Checks if the received command is used for the networkManager or
        pass it to the messageReceiver
        @param client: the origin of the command
        @param command: the command
        @result:
        '''
        self.logger.debug("Broadcast received: {}".format(message))
        self.receiver.messageReceived(senderIp, senderPort, message)

