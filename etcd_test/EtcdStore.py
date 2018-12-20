import grpc
import etcd3
import json

class EtcdStore(object):

    def __init__(self, host, port, kv_path):
        self._etcd = etcd3.client(host=host, port=port)
        self.host = host
        self.port = port
        self._kv_path = kv_path

    def make_path(self, key):
        return '{}/{}'.format(self._kv_path, key)

    def __getitem__(self, key):
        (value, meta) = self._etcd.get(self.make_path(key))
        if value is not None:
            return value
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
            self._etcd.put(self.make_path(key), value)

    def __delitem__(self, key):
        self._etcd.delete(self.make_path(key))

    def __acquire_lock__(self,key):
        lock=self._etcd.lock(self.make_path(key),ttl=10)
        print(lock.acquire())
        return lock

    def __release_lock__(self,lock):
        lock.release()

    def __isLockAcquired__(self,lock):
        #print(lock.is_acquired())
        return lock.is_acquired()

'''
obj=EtcdStore('localhost',2379,"/vEtcd")
obj.__setitem__('test',"What a message to test")
obj.__setitem__('test/path1',"path1 message")
#obj.__setitem__('test/path1/path2',"path2 message")
#val=obj.__getitem__('test')
lock=obj.__acquire_lock__('test')
val=obj.__getitem__('test')
print obj.__isLockAcquired__(lock)
print("Value of test is",val)
#val=obj.__getitem__('v/BNG10/ABC/RSYS1/ELECTRA/F6')
#print("Value of test is",val)
#lock=obj.__acquire_lock__('v/BNG1/ABC')
#print obj.__isLockAcquired__(lock)
#obj.__setitem__('test/path1/path2',"This is a new message")
lock1=obj.__acquire_lock__('v/BNG10/ABC/RSYS1/ELECTRA/F6')
print obj.__isLockAcquired__(lock)
#obj.__setitem__('test',"This is a message from 2nd lock")
#val=obj.__getitem__('test')
#print("Value of test is",val)
#val=obj.__getitem__('test/path1/path2')
#print("Value of test is",val)
#obj.__release_lock__(lock)
obj.__isLockAcquired__(lock)
#val=obj.__getitem__('test')
#print("Value of test is",val)
if obj.__isLockAcquired__(lock1):
    obj.__setitem__('test',"This is a new message")
    val=obj.__getitem__('test')
print("Value of test is",val)
#obj.__delitem__('test')
#val=obj.__getitem__('test')
#if val is None:
#    print("This value is None")
'''
