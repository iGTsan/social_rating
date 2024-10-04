import vk_api, multiprocessing, time, sys, pika

isLocal = None
isProdigy = None
debug = None
API = None
threadPool = None
def Autification(isProdigy):
    if isProdigy:
        RUN = open('RUNProdigy.txt', 'r')
        RUN_arr = RUN.readlines()
        vk = vk_api.VkApi(token=RUN_arr[0][:-1])
        vk._auth_token()
        RUN.close()
        return vk
    else:
        RUN = open('RUN.txt', 'r')
        RUN_arr = RUN.readlines()
        vk = vk_api.VkApi(token=RUN_arr[0][:-1])
        vk._auth_token()
        RUN.close()
        return vk


def adminAuth():
    vk_admin = vk_api.VkApi('+79163447672',
                            token="vk1.a.lEFtR2sMDqZDSfZIJ6wGjr1Tr56tDt0QFUUgX248ET51rrBQw12gxFqXxLTanLOeCvAMg6P2ezUyCW3myZItZKcgO6KRaWq81sT1mpjPU9BEFU0BTdvtQ6VR9AeQ3CrzX84fXG9BOC0p3P0I6F0kJbdUfZhPNk33h2XG-DZUFvlYd-5j6ZBg06FBiSj5n8UO2scrm8XUdzdLUIppQlNHcA")
    vk_admin.get_api()
    return vk_admin


class ApiService:
    def __init__(self, sendQueue, pipeQueue, isProdigy):
        self.sendQueue = sendQueue
        self.pipeQueue = pipeQueue
        self.isProdigy = isProdigy
        self.vk = Autification(isProdigy)
        self.vk_admin = adminAuth()
        self.vk.RPS_DELAY = 0.051

    def safe_executer(self, event, admin, type):
        if type == "execute":
            func = self.execute
        elif type == "execute_cb":
            func = self.execute_cb
        elif type == "is_admin":
            func = self.is_admin

        flag = 10
        while flag:
            try:
                func(event, admin)
                flag = 0
            except Exception as cal:
                print(cal, "in safe executer", event)
                flag -= 1
                time.sleep(1)




    def execute(self, event, admin):
        if admin:
            self.vk_admin.method(event[1], event[2])
        else:
            self.vk.method(event[1], event[2])

    def execute_cb(self, event, admin):
        pipe = event[4]["start"]
        if admin:
            tmp = self.vk_admin.method(event[1], event[2])
        else:
            tmp = self.vk.method(event[1], event[2])
        pipe.send(tmp)
        pipe.recv()
        self.pipeQueue.put(event[4])

    def is_admin(self, event, admin):
        try:
            self.vk.method(event[1], event[2])
            pipe = event[4]["start"]
            pipe.send(True)
            pipe.recv()
            self.pipeQueue.put(event[4])
        except Exception:
            pipe = event[4]["start"]
            pipe.send(False)
            pipe.recv()
            self.pipeQueue.put(event[4])

def callback(ch, method, properties, body):
    request = json.loads(body)
    #print(" [x] Received %r" % data)
    #sys.stdout.flush()
    try:
        if debug and request[1] != "messages.send":
            print("sending", request)

        if request[0] == "bot":
            if request[3] == "OneWay":
                API.safe_executer(request, 0, "execute")
            else:
                threadPool.submit(API.safe_executer, request, 0, "execute_cb")
        elif request[0] == "admin":
            if request[3] == "OneWay":
                API.safe_executer(request, 1, "execute")
            else:
                threadPool.submit(API.safe_executer, request, 1, "execute_cb")
        else:
            threadPool.submit(API.safe_executer, request, 1, "is_admin")
    except Exception as shit:
        print("apiService", shit, request)
        sys.stdout.flush()

if __name__ == "__main__":
    
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            channel = connection.channel()
            break
        except Exception:
            print("Failed to connect to RabbitMQ")
            sys.stdout.flush()
            time.sleep(2)
            continue

    channel.queue_declare(queue='sendQueue')

    isLocal = int(sys.argv[1])
    isProdigy = int(sys.argv[2])
    debug = int(sys.argv[3])

    API = vkApiService.ApiService(sendQueue, pipeQueue, isProdigy)
    threadPool = concurrent.futures.ThreadPoolExecutor(max_workers=100)

    channel.basic_consume(queue='sendQueue',
                      auto_ack=True,
                      on_message_callback=callback)

    print("apiService STARTED!")
    sys.stdout.flush()

    channel.start_consuming()
