#!/usr/bin/python3
import os
import sys

__DIR__ = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, __DIR__)
sys.path.insert(0, __DIR__ + '/../')

from modules import logger
from modules import threading_control
from modules import writer

import config


class prot_smtp:


    def __init__(self):
        self.preferences = {
            'ports': [
                25,
                465,
                587,
            ],
            
            'response_on_connect': True,
            'wait_user_input': True,
        }

    #
    # Get ports associated
    #
    def get_preferences(self):
        return self.preferences


    #
    # Route
    #
    def route(self, datas, connection, addr):
        self.answer(connection, datas)


    #
    # Send default answer
    #
    def answer(self, connection, datas):
        # default answer
        try:
            connection.sendall(b'220 smtp.gmail.com ESMTP f6sm175797wrs.45 - gsmtp\r\n')
            connection.sendall(b'\r\n')

            if self.preferences['wait_user_input'] == False:
                connection.close()

        except:
            pass