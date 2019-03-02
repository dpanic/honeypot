#!/usr/bin/python3

import sys
import time


class bcolors:
    HEADER = '\033[1m\033[37m'
    OKBLUE = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def dump(msg, msg_type):
    try:
        msg = str(msg)
    except:
        pass
    
    try:
        msg = msg.decode('utf8', errors='ignore')
    except:
        pass

    try:

        dts = time.localtime(time.time())
        dts = time.strftime('%d.%m.%Y %H:%M:%S', dts)

        if msg_type == "critical": 
            print('[ ' + dts + ' ] ' + bcolors.FAIL + msg + bcolors.ENDC)

        if msg_type == "warning": 
            print('[ ' + dts + ' ] ' + bcolors.WARNING + msg + bcolors.ENDC)

        if msg_type == "error":
            print('[ ' + dts + ' ] ' + bcolors.FAIL + msg + bcolors.ENDC)

        if msg_type == "info":
            print('[ ' + dts + ' ] ' + bcolors.OKBLUE + msg + bcolors.ENDC)

        if msg_type == "good":
            print('[ ' + dts + ' ] ' + bcolors.OKGREEN + msg + bcolors.ENDC)

        if msg_type == "debug":
            print('[ ' + dts + ' ] ' + bcolors.HEADER + msg + bcolors.ENDC)
    except:
        try:
            print(sys.exc_info())
        except:
            pass