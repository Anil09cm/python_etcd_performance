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
        return lock.is_acquired()
