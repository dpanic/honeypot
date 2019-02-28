#!/usr/bin/python3
import os
import sys
import time


try:
    import thread
except:
    import _thread as thread


from includes import logger


class writer:

    def __init__(self):
        self.queue = []
        self.max_queue_size = 1000
        self.mutex = thread.allocate_lock()

        thread.start_new_thread(self.looper, ())
       
       

    #
    # Writing thread
    #
    def looper(self):
        
        logger.dump('writer.looper() started!', 'info')

        while 1:


            self.mutex.acquire()
            total_in_queue = len(self.queue)
            self.mutex.release()

            if total_in_queue > 0:
                time.sleep(0.01)
            else:
                time.sleep(1.0)

            if total_in_queue > 0:

                self.mutex.acquire()
                obj = self.queue.pop()
                self.mutex.release()

                logger.dump('writer.looper(): writing to file %s -> %s' %(obj['file_loc'], obj['message']), 'info')

                try:
                    file_loc = os.path.abspath(obj['file_loc'])

                    self.outfile = open(file_loc, 'a')
                    self.outfile.write(obj['message'])
                    self.outfile.flush()
                except:
                    logger.dump('writer.looper(): %s' %(str(sys.exc_info())), 'warning')





    #
    # Add to queue
    #
    def write(self, file_loc=False, message=''):
        self.mutex.acquire()
        
        if len(self.queue) > self.max_queue_size:
            logger.dump('Queue is full! Dropping this one. Sorry.', 'warning')
            self.mutex.release()
            return False


        if file_loc == False:
            logger.dump('Log file output location is empty...Dropping this one.', 'warning')
            self.mutex.release()
            return False


        message = message.decode('utf8')

        if message in [ '', None, False ]:
            logger.dump('Message empty...Dropping this one.', 'warning')
            self.mutex.release()
            return False

        logger.dump('Message sent to queue.', 'info')

        obj = {
            'file_loc': file_loc,
            'message': message,
        }
        self.queue.append(obj)

        self.mutex.release()

        return True