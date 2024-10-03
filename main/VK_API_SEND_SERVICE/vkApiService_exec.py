def apiService(sendQueue, pipeQueue, isProdigy, debug):
    print("apiService")
    API = vkApiService.ApiService(sendQueue, pipeQueue, isProdigy)
    threadPool = concurrent.futures.ThreadPoolExecutor(max_workers=100)

    request = None

    while True:
        try:
            while True:
                request = sendQueue.get(True)

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
                break
        except Exception as shit:
            print("apiService", shit, request)
