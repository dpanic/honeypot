#!/usr/bin/python3
import gc
import sys
import time

try:
    import thread
except:
    import _thread as thread


class threading_control():
    
    def __init__(self, max_work=30, max_threads=50):
        self.total_threads = 0

        self.mutex = thread.allocate_lock()

        self.max_work = max_work
        self.max_threads = max_threads
        self.start = time.time()

    #
    # Get total running threads
    #
    def get_total_threads(self):
        return self.total_threads


    #
    # helper method for checking if maximum allowed runtime has exceeded
    #
    def can_work(self):
        x = time.time() - self.start
        if x >= self.max_work: 
            return False
        return True


    #
    # helper method for checking if maximum allowable threads started
    #
    def wait_threads(self):
        while self.total_threads >= self.max_threads:
            time.sleep(0.1)

    #
    # Increment number of running threads
    #
    def inc_threads(self):
        self.mutex.acquire()

        self.total_threads += 1

        self.mutex.release()

    #
    # Decrement number of running threads
    #
    def dec_threads(self):
        self.mutex.acquire()

        self.total_threads -= 1

        self.mutex.release()
