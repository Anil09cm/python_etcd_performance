import logging
import random
from KThread import *
from time import sleep

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class test():
    def __init__(self):
        logging.debug("Test Init")
        self.lock = threading.Lock()
 
    def func(self, operation):
        logging.debug("Aquiring the Lock")
        self.lock.acquire()
        try:
            if operation == 'read':
                with open('file_1', 'r') as f:
                    logging.info('Data - {}'.format(f.readlines()))

            if operation == 'write':
                with open('file_1', 'a') as f:
                    f.writelines(str(random.random()))
        except Exception as e:
            logging.debug('Execption - {}'.format(e))
        self.lock.release()
        logging.debug("Lock Released")

def reader(obj):
    for i in range(30):
        logging.debug('Starting Read operation')
        obj.func('read')
        logging.debug('Sleeping for 1 sec in Reader thread')
        sleep(1)

def writer(obj):
    for i in range(30):
        logging.debug('Starting write operation')
        obj.func('read')
        logging.debug('Sleeping for 1 sec in writer thread')
        sleep(1)



obj = test()
th1 = KThread(target=reader, args=(obj,))
th2 = KThread(target=writer, args=(obj,))

"""
A.start()
for i in xrange(10000):
    pass
A.kill()
"""
th1.start()
th2.start()

logging.debug('Waiting for worker threads')
main_thread = threading.currentThread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()


print 'End of main program'
