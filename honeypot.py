#!/usr/bin/python3

import os
import sys
import time
import socket


__DIR__ = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, __DIR__ + '/protocols/')


try:
    import thread
except:
    import _thread as thread


from modules import logger
from modules import threading_control
from modules import writer

import config



class HoneyPot:

    def __init__(self):
        logger.dump('HoneyPot v1', 'debug')

        # configuration part
        self.max_threads = config.c['max_threads']
        self.max_live_time = 0

        # this defines timeout
        self.max_thread_alive = config.c['max_thread_alive']

        # references
        self.ref_tc = threading_control.threading_control(self.max_live_time, max_threads=self.max_threads)
        self.ref_writer = writer.writer()


        self.ref_protocols = {}
        self.load_protocols()

        thread.start_new_thread(self.stats, ())

        # init 
        dirs = [
            __DIR__ + '/data/',
        ]

        for directory in dirs:
            try:
                directory = os.path.abspath(directory)
                os.mkdir(directory)
                logger.dump('mkdir %s' %(directory), 'debug')
            except:
                pass

        

    #
    # Load protocols
    #
    def load_protocols(self):
        res = os.listdir(__DIR__ + '/protocols/')

        for file in res:
            if file.endswith('.py') == True:

                module_name = file.replace('.py', '')
                logger.dump('Loaded protocol [%s]' %(module_name), 'good')

                try:
                    # loading module
                    mod = __import__(module_name) 

                    # getting class
                    klass = getattr(mod, module_name) 
                    instance = klass()
                    ports = instance.get_ports()

                    for port in ports:
                        self.ref_protocols[port] = klass()
                except:
                    logger.dump('load_protocols(): %s > %s' %(module_name, str(sys.exc_info())), 'critical')





    #
    # Client connection
    #
    def client(self, port, connection, addr):
        self.ref_tc.inc_threads()

        datas = b''
        ts_start = time.time()
        while True:
            diff = time.time() - ts_start

            if diff >= self.max_thread_alive:
                logger.dump('Thread timeouted in %s sec. Closing.' %(diff), 'warning')
                break

            try:
                connection.settimeout(5.0)
                data = connection.recv(4 * 1024)
                datas += data
                
                logger.dump('received {!r}'.format(data), 'debug')

                if not data:
                    print('no more data from', connection)
                    break

                break

            except socket.timeout:
                logger.dump('socket timeout!', 'warning')

            except:
                logger.dump('client(%s): %s' %(str(addr), str(sys.exc_info())), 'error')


        # router
        try:
            self.ref_protocols[port].route(datas, connection, addr)
        except:
            print(str(sys.exc_info()))
            logger.dump('no port %s handler! implement protocol!' %(port), 'critical')


        try:
            connection.close()
        except:
            pass


        if datas != '':
            print(datas)
            self.ref_writer.write(config.c['log_file'], datas)


        self.ref_tc.dec_threads()
        logger.dump('Closing socket', 'info')


    #
    # Stats
    #
    def stats(self):
        while 1:
            total_threads = self.ref_tc.get_total_threads()

            if total_threads > 0:
                logger.dump('CONNECTIONS: %s' % (total_threads), 'warning')
            
            time.sleep(5)




    #
    # Main thread
    #
    def run(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        host = '0.0.0.0'

        try:
            s.bind((host, port))
        except PermissionError:
            logger.dump('%s:%s error listening!' %(host, port), 'warning')
            try:
                s.close()
            except:
                pass
            return False


        logger.dump('%s:%s started!' %(host, port), 'info')
        s.listen(self.max_threads)


        while True:
            self.ref_tc.wait_threads()

            connection, addr = s.accept()
            logger.dump("<- %s" %(str(addr)), 'good')
            thread.start_new_thread(self.client, (port, connection, addr))

        s.close()

    #
    # Long run
    #
    def long_run(self):
        while 1:
            time.sleep(60)




if __name__ == '__main__':

    hpot = HoneyPot()
    for port in config.c['listen_ports']:
        thread.start_new_thread(hpot.run, (port,))


    hpot.long_run()