#!/usr/bin/python3
import os
import sys
import time

__DIR__ = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, __DIR__)
sys.path.insert(0, __DIR__ + '/../')

from modules import logger
from modules import threading_control
from modules import writer

import config


class prot_http:


    def __init__(self):
        self.preferences = {
            'ports': [
                80,
                443,
                8080,
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
        if datas.find(b'stats') != -1:
            self.answer_stats(connection, addr)
        else:
            self.answer(connection, datas)


    #
    # Send system stats
    #
    def answer_stats(self, connection, addr):
        logger.dump('Sending system stats to %s!' %(str(addr)), 'critical')
        connection.sendall(b'HTTP/1.1 200 OK\r\n')
        connection.sendall(b'Content-Type: text/plain; charset=utf-8\r\n')
        connection.sendall(b'Server: hpot\r\n')
        connection.sendall(b'Connection: close\r\n')

        #Content-Length: 14
        #Date: Sat, 13 Oct 2018 20:08:08 GMT

        is_existing = os.path.isfile(config.c['report_file'])
        if is_existing == True:
            connection.sendall(b'\r\n')

            stat = os.stat(config.c['report_file'])
            print(stat)

            dts_created = stat.st_ctime

            dts_created = time.localtime(dts_created)
            dts_created = time.strftime("%B %d, %Y %H:%M:%S %z (%Z)", dts_created)

            dts_modified = stat.st_mtime
            print(dts_modified)
            dts_modified = time.localtime(dts_modified)
            dts_modified = time.strftime("%B %d, %Y %H:%M:%S %z (%Z)", dts_modified)

            dts_created = dts_created.encode('utf-8')
            dts_modified = dts_modified.encode('utf-8')


            print(dts_modified)

            f = open(config.c['report_file'], 'r')

            content = f.read()
            content = content.encode('utf-8')

            header = b'** HONEYPOT STATS **\r\n'
            rows = content.count(b'\n')
            header += b'rows: %d\r\n' %(rows)
            header += b'created: %s\r\n' %(dts_created)
            header += b'modified: %s\r\n' %(dts_modified)

            header += b'\r\n'
            
            body = header + content

            connection.sendall(body)
            f.close()

            connection.sendall(b'\r\n\r\n')

        else:
            connection.sendall(b'\r\n')
            connection.sendall(b'no stats file\r\n\r\n')


    #
    # Send default answer
    #
    def answer(self, connection, datas):
        # default answer
        try:
            connection.sendall(b'HTTP/1.1 404 Not Found\r\n')
            connection.sendall(b'Server: Apache/2.4.29 (Ubuntu)\r\n')
            connection.sendall(b'Connection: close\r\n')
            connection.sendall(b'Content-Type: text/html; charset=iso-8859-1\r\n')
            connection.sendall(b'\r\n')
            connection.sendall(b':)')
            connection.sendall(b'\r\n')


            if self.preferences['wait_user_input'] == False:
                connection.close()

        except:
            pass