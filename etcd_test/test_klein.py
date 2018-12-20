import json
from klein import run, route
from random import randint


class MyTest(object):
    _instance = None
    def __init__(self, ip, port):
        self.threads = []
        self.ip = ip
        self.port = port
  
    def get_threads(self, request):
        print "Threads :  {} ".format(self.threads)
    
    def create_threads(self, request):
        self.threads.append(randint(1, 100))
    
    def start_server(self):
        print "Running the Server"
        run(self.ip, self.port)


@route('/v1/threads', methods=['GET']) 
def get_all_threads(request, obj):
    obj.get_threads()

@route('/v1/create', methods=['POST'])
def create_threads(request, obj):
    content = json.loads(request.content.read().decode('utf-8'))
    print "Content : {}".format(content)
    obj.create_threads()

if __name__ == '__main__':
    
    obj = MyTest('localhost', 9999)
    obj.start_server()

