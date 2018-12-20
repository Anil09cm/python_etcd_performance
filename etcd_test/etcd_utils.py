import logging
import random
from time import sleep
import json
import threading
from KThread import *
from EtcdStore import EtcdStore
from klein import run, route

logging.basicConfig(level=logging.DEBUG, filename='LOGS.txt',
     format='(%(threadName)-9s) %(asctime)s %(name)-12s \
     %(levelname)-8s %(message)s',)

last_thread = 0 #has the last thread name
etcd_util_obj = None

class etcdUtils(object):

    def __init__(self, ip, port, kv_root):
        #logging.info('EtcdUtils Init')
        self.kvs = None
        self.ip = ip
        self.port = port
        self.kv_root = kv_root
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
        #sleep(1)
    #@staticmethod
    def set_worker(self, sleep_time ):
        #self.update_kv()
        logging.info("Availble Keys in ETCD : {}".format(self.updated_keys))
        for i in range(100):
            #logging.debug("Random Key index generated --> {}".format(random_key_index))
            random_key_index = random.randint(0, len(self.updated_keys)-1)
            logging.debug("Random Key index generated --> {}".format(random_key_index))
            #logging.info("Aquiring the Lock!")
            lock = self.es.__acquire_lock__(self.updated_keys[random_key_index])
            if self.es.__isLockAcquired__(lock):
                logging.info("Lock acquired on the key -- \
                        {}".format(self.updated_keys[random_key_index]))
                newval = "ID-"+str(random.randint(0, 10000))
                self.es.__setitem__(self.updated_keys[random_key_index], newval)
                logging.info("Updated the key : {} \
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
        name_list = [ t.name for t in threading.enumerate()]
        logging.info( "THREADS : {}".format(repr(name_list)))
        return repr(name_list)

    def create_threads(self, data):
        logging.info("Creating threads")
        #create threads 
        global last_thread 
        start_id = last_thread
        for i in range(start_id, start_id +int(data['count'])):
            thread_name = 'worker-{}'.format(i)
            self.threads.append(KThread(name=thread_name, 
                      target=etcdUtils(self.ip, self.port, self.kv_root).set_worker, args=(random.randint(5, 15),)))
    
    def start_threads(self):
        #print "Threads = = = = ", self.threads
        for t in self.threads:
            t.start()
  
    def kill_thread(self, thread_name):
        for t in threading.enumerate():
            if t.name == thread_name:
                logging.info("Found the Thread - {} and Killing it".format(t.name))
                t.kill()
                break

@route('/v1/threads', methods=['GET'])
def get_running_threads(request):
    global etcd_util_obj
    return etcd_util_obj.get_worker_threads()


@route('/v1/create', methods=['POST'])
def create_threads(request):
    #response has the threads count
    global etcd_util_obj
    content = json.loads(request.content.read().decode('utf-8'))
    print "Here Content === ", content
    etcd_util_obj.create_threads(content)
    etcd_util_obj.start_threads()

@route('/v1/kill/<thread_name>', methods=['DELETE'])
def kill_thread_func(request, thread_name):
    global etcd_util_obj
    etcd_util_obj.kill_thread(thread_name)

def start_rest_server():
    run('localhost', 9898)

        

if __name__ == '__main__':
    
    logging.info("starting Rest server")
    global etcd_util_obj
    etcd_util_obj = etcdUtils('localhost', 2379, '/vEtcd')
    etcd_util_obj.update_kv()
    #create etcdutil object
    #make it global

    #start the rest server
    #write wrapper functions for route
    start_rest_server()
        

