import logging
import random
from time import sleep
from KThread import *
from EtcdStore import EtcdStore
from klein import run, route

logging.basicConfig(level=logging.DEBUG, #filename='LOGS.txt',
     format='(%(threadName)-9s) %(asctime)s %(name)-12s \
     %(levelname)-8s %(message)s',)

class etcdUtils(object):

    def __init__(self, ip, port, kv_root):
        logging.info('EtcdUtils Init')
        self.kvs = None
        self.es = EtcdStore(ip, port, kv_root)
        self.updated_keys = []
        self.threads = []
    def update_kv(self):
        logging.info('Updating the KV pairs')
        with open('input_kv_pairs', 'r') as fh:
            self.kvs = fh.readlines()
        for i in self.kvs:
            x = i.strip().split('/')
            for index in range(1,len(x)+1):
                key = '/'.join(x[:index])
                val = "ID-"+str(random.randint(0, 10000))
                if key != '' or key != None:
                    if key not in self.updated_keys:
                        self.updated_keys.append(key)
                    self.es.__setitem__(key, val)

    def set_worker(self, sleep_time ):
        logging.info("Availble Keys in ETCD : {}".format(self.updated_keys))
        for i in range(100):
            random_key_index = random.randint(0, len(self.updated_keys)-1)
            #logging.debug("Random Key index generated --> {}".format(random_key_index))
            #logging.info("Aquiring the Lock!")
            lock = self.es.__acquire_lock__(self.updated_keys[random_key_index])
            if self.es.__isLockAcquired__(lock):
                logging.info("Lock acquired on the key -- \
                        {}".format(self.updated_keys[random_key_index]))
                newval = "ID-"+str(random.randint(0, 10000))
                self.es.__setitem__(self.updated_keys[random_key_index], newval)
                logging.infoG("Updated the key : {} \
                              with value : {}".format(
                              self.updated_keys[random_key_index], newval))
                logging.info("Worker Sleeping for - {}seconds".format(sleep_time))
                sleep(sleep_time)
                logging.info("Released the Lock!")
            else:
                logging.warn("not able to Lock the Resource --\
                        {}".format(self.updated_keys[random_key_index]))
            self.es.__release_lock__(lock)

    def get_worker_threads(self):
        logging.info("Get method - Worker threads")
        #return self.threads
    def  create_thread(self):
        logging.info("Creating threads")
        

if __name__ == '__main__':
    logging.info("starting Rest server")

        """
        etcdutils = etcdUtils('localhost', 2379, '/vEtcd')
        etcdutils.update_kv()
        th1 = KThread(name='Worker-1', target=etcdutils.set_worker, args=(5,))
        th2 = KThread(name='Worker-2', target=etcdutils.set_worker, args=(4,))
        th3 = KThread(name='Worker-3', target=etcdutils.set_worker, args=(3,))
        #th1.setDaemon(True)
        #th2.setDaemon(True)
        #th3.setDaemon(True)
        th1.start()
        th2.start()
        th3.start()
        logging.info("In main Thread!")
        sleep(30)
        logging.info("Killing thread 2")
        th2.kill()
        th1.join()
        #th2.join(:q)
        th3.join()
        logging.info("Done!")
        #update_kv()
        #test_kv_set()
        #test_kv_get()
        #test_thread_kill()
        """
