# -*- coding: utf-8 -*-
'''
Created on 2013-02-04 19:55
@summary:
@author: Martin Predki
'''

# SubProcessHandler
from SubProcess import SubProcessController

# Imports for Pyrowl
from pyrowl import Pyrowl

import logging


logger = logging.getLogger("HomeSystem")
processController = SubProcessController()
p = Pyrowl("61d552cdbd5ed63e5590ea0ef0cd6665508f6406")

@staticmethod
def Licht_Bad_Rollade():
    logger.info("Licht Bad und Rollade")
    processController.startProcess("wget",
        "http://192.168.191.10:80/rasp_4_toilette.ssi",
        "--http-user=admin",
        "--http-password=wago",
        "-q")


@staticmethod
def Licht_Wohnzimmer_Musik():
    logger.info("Licht Wohnzimmer und Musik")
    processController.startProcess("wget",
        "http://192.168.191.10:80/rasp_3_licht_musik.ssi",
        "--http-user=admin",
        "--http-password=wago",
        "-q")
    p.push("Raspi", 'Haus', 'Test', batch_mode=False)


@staticmethod
def Licht_Wohnzimmer_Fernsehr():
    logger.info("Licht Wohnzimmer und Fernseher")
    processController.startProcess("wget",
        "http://192.168.191.10:80/rasp_2_fernseher.ssi",
        "--http-user=admin",
        "--http-password=wago",
        "-q")

    processController.startProcess("wget",
        "http://192.168.191.9/web/powerstate?newstate=4")
