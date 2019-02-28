#!/usr/bin/python3

import os
import sys
import time
import socket


__DIR__ = os.path.dirname(os.path.realpath(__file__))


try:
    import thread
except:
    import _thread as thread


from includes import logger
from includes import threading_control

from modules import writer

import config



class HoneyPot:

    def __init__(self):
        logger.dump('HoneyPot v1', 'debug')

        # configuration part
        
        # concurent users
        self.max_threads = config.c['max_threads']
        self.listen_port = config.c['listen_port']
        self.max_live_time = 0

        # this defines timeout
        self.max_thread_alive = config.c['max_thread_alive']

        # references
        self.ref_tc = threading_control.threading_control(self.max_live_time, max_threads=self.max_threads)
        self.ref_writer = writer.writer()

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

        
        self.log_file = config.c['log_file']
        self.report_file = config.c['report_file']
        self.report_file_raw = config.c['report_file_raw']



    #
    # Send system stats
    #
    def answer_stats(self, connection, addr, freq=True):

        logger.dump('Sending system stats to %s!' %(str(addr)), 'critical')
        connection.sendall(b'HTTP/1.1 200 OK\r\n')
        connection.sendall(b'Content-Type: text/plain; charset=utf-8\r\n')
        connection.sendall(b'Server: hpot\r\n')
        connection.sendall(b'Connection: close\r\n')

        #Content-Length: 14
        #Date: Sat, 13 Oct 2018 20:08:08 GMT

        if freq == True:
            is_existing = os.path.isfile(self.report_file)
        else:
            is_existing = os.path.isfile(self.report_file_raw)


        if is_existing == True:
            connection.sendall(b'\r\n')

            if freq == True:
                f = open(self.report_file, 'r')
            else:
                f = open(self.report_file_raw, 'r')

            content = f.read()
            content = content.encode('utf-8')

            header = b'** HONEYPOT STATS **\r\n'
            rows = content.count(b'\n')
            header += b'rows: %d\r\n' %(rows)
            total_threads = self.ref_tc.get_total_threads()
            header += b'connections: %d / %d\r\n' %(total_threads, self.max_threads)
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

            connection.close()

        except:
            pass


    #
    # Client connection
    #
    def client(self, connection, addr):
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
                data = connection.recv(4096)
                datas += data
                
                logger.dump('received {!r}'.format(data), 'debug')

                if not data:
                    print('no more data from', connection)
                    break

                
                # router
                if datas.find(b'dusan0802') != -1:
                    
                    if datas.find(b'freq') != -1:
                        self.answer_stats(connection, addr, freq=True)
                    else:
                        self.answer_stats(connection, addr, freq=False)


                    try:
                        connection.close()
                    except:
                        pass
                    
                    self.ref_tc.dec_threads()
                    return False

                else:
                    self.answer(connection, datas)
                    break

            except socket.timeout:
                logger.dump('socket timeout!', 'warning')

            except:
                logger.dump('client(%s): %s' %(str(addr), str(sys.exc_info())), 'error')

        try:
            connection.close()
        except:
            pass

        if datas != '':
            print(datas)
            self.ref_writer.write(self.log_file, datas)


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
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        host = '0.0.0.0'
        port = self.listen_port

        try:
            s.bind((host, port))
        except PermissionError:
            logger.dump('%s:%s error listening!' %(host, port), 'warning')
            port = '8080'
            port = int(port)
            s.bind((host, port))


        logger.dump('%s:%s started!' %(host, port), 'info')
        s.listen(self.max_threads)


        while True:
            self.ref_tc.wait_threads()

            connection, addr = s.accept()
            logger.dump("<- %s" %(str(addr)), 'good')
            thread.start_new_thread(self.client, (connection, addr))

        s.close()


if __name__ == '__main__':
    hpot = HoneyPot()
    hpot.run()