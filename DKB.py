import random, vk_api, os, time, multiprocessing, concurrent.futures
import sys

import events, daily, vkApiService, utilities
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll


def AutificationMain(isProdigy):
    global LP
    if isProdigy:
        RUN = open('RUNProdigy.txt', 'r')
        RUN_arr = RUN.readlines()
        vk = vk_api.VkApi(token=RUN_arr[0][:-1])
        vk._auth_token()
        LP = VkBotLongPoll(vk, RUN_arr[1])
        RUN.close()
        return LP
    else:
        RUN = open('RUN.txt', 'r')
        RUN_arr = RUN.readlines()
        vk = vk_api.VkApi(token=RUN_arr[0][:-1])
        vk._auth_token()
        LP = VkBotLongPoll(vk, RUN_arr[1])
        RUN.close()
        return LP


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device


def eventManager(eventQueue, isProdigy, isLocal, sendQueue, pipeQueue, debug):
    print("eventManager")
    executor = events.Events(isProdigy, isLocal,sendQueue, pipeQueue)
    threadPool = concurrent.futures.ThreadPoolExecutor(max_workers=32)

    if debug:
        test_event = {'message': {'date': 1669403763, 'from_id': 231688699, 'id': 0, 'out': 0, 'attachments': [], 'conversation_message_id': 610, 'fwd_messages': [], 'important': False, 'is_hidden': False, 'peer_id': 2000000001, 'random_id': 0, 'text': '/топ'}, 'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link', 'callback', 'intent_subscribe', 'intent_unsubscribe'], 'keyboard': True, 'inline_keyboard': True, 'carousel': True, 'lang_id': 0}}
        threadPool.submit(executor.start_event, executor.delta, test_event)
        threadPool.submit(executor.start_event, executor.top, test_event)
        threadPool.submit(executor.start_event, executor.top_all, test_event)
        threadPool.submit(executor.start_event, executor.roll, test_event)
        threadPool.submit(executor.start_event, executor.summarry, test_event)
        threadPool.submit(executor.start_event, executor.sound, test_event)
        threadPool.submit(executor.start_event, executor.my_cock, test_event)
        threadPool.submit(executor.start_event, executor.remove_cock, test_event)

    while True:
        try:
            while True:

                event = eventQueue.get(True)

                #   if not(isLocal):
                #   print(os.getpid(), event)



                if debug and event["message"]["text"][0] == "/":
                    threadPool.submit(executor.start_event, executor.TechRab, event)
                    continue

                if event["message"]["text"].lower() == "/писюн":
                    threadPool.submit(executor.start_event, executor.delta, event)
                elif event["message"]["text"].lower() == "/топ":
                    threadPool.submit(executor.start_event, executor.top, event)
                elif event["message"]["text"].lower() == "/топ_все":
                    threadPool.submit(executor.start_event, executor.top_all, event)
                elif event["message"]["text"].lower() == "/ролл":
                    threadPool.submit(executor.start_event, executor.roll, event)
                elif event["message"]["text"].lower() == "/чат":
                    threadPool.submit(executor.start_event, executor.summarry, event)
                elif event["message"]["text"].lower() == "/микс":
                    threadPool.submit(executor.start_event, executor.sound, event)
                elif event["message"]["text"].lower() == "/мой_писюн":
                    threadPool.submit(executor.start_event, executor.my_cock, event)
                elif event["message"]["text"].lower() == "/кострация":
                    threadPool.submit(executor.start_event, executor.remove_cock, event)
                break
        except Exception as shit:
            print("eventManager", shit, event)


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


def dailyTasks(isProdigy, isLocal, sendQueue, pipeQueue, debug):
    print("dailyTasks")
    try:
        tasks = daily.Daily(isProdigy, isLocal, sendQueue, pipeQueue, debug)
        tasks.start()
    except Exception as shit:
        print("dailyTasks", shit)


if __name__ == "__main__":

    time.sleep(20)

    eventQueue = multiprocessing.Queue(maxsize=1000)
    sendQueue = multiprocessing.Queue(maxsize=1000)
    pipeQueue = multiprocessing.Queue(maxsize=100)
    for i in range(50):
        pipeST , pipeED = multiprocessing.Pipe()
        tmp = {"start" : pipeST, "end" : pipeED}
        pipeQueue.put(tmp)

    isProdigy = 1 #sys.argv[2] == "True"
    isLocal = 1
    debug = 1 #sys.argv[1] == "True"

    LP = AutificationMain(isProdigy)

    try:
        f = open('timing.txt', 'r')
    except Exception:
        f = open('timing.txt', 'w')
        f.write("100")
        f.close()
        f = open('timing.txt', 'r')
    TMP = int(f.readline())
    f.close()

    apiServiceProcess = multiprocessing.Process(target=apiService, args=(sendQueue, pipeQueue, isProdigy, debug,))
    eventManagerProcess = multiprocessing.Process(target=eventManager, args=(eventQueue, isProdigy, isLocal, sendQueue, pipeQueue, debug,))
    dailyTasksProcess = multiprocessing.Process(target=dailyTasks, args=(isProdigy, isLocal, sendQueue, pipeQueue, debug,))
    apiServiceProcess.start()
    eventManagerProcess.start()
    dailyTasksProcess.start()

    commands = ["/писюн", "/топ", "/топ_все", "/ролл", "/чат", "/микс", "/мой_писюн", "/кострация"]

    while True:
        print("Ready")
        try:
            for event in LP.listen():

                if event.type == VkBotEventType.MESSAGE_NEW:
                    text = event.object["message"]["text"].lower()
                    if event.object["message"]["peer_id"] != event.object["message"]["from_id"]:
                        if text in commands:
                            eventQueue.put(dict(event.object))

                    elif event.object["message"]["peer_id"] == event.object["message"]["from_id"]:
                        if text == "" or text[0] == "/" or text == "начать":
                            request = ("bot", "messages.send",
                                      {"peer_id": event.object["message"]["from_id"],
                                       "message": "Дружище, наш бот работает только в беседах. Здесь ты можешь задать вопрос разработчикам. Подпишись на нашу группу, чтобы не пропускать новости разработки и ежедневные топы бесед, а пока держи гайд: https://vk.com/@dickkraftbot-itak-prishlo-vremya-napisat-podrobnyi-gaid-na-bota",
                                       "random_id": random.randint(1, 2147483647)}, "OneWay")
                            sendQueue.put(request)
                        else:
                            continue
                elif event.type == "donut_subscription_create":
                    print("Мама, ноый донат)")
                elif event.type == "donut_subscription_expired":
                    print("Бля, минус дон(")

        except Exception as fuck:
            try:
                LP = AutificationMain(isProdigy)
                print("LP update")
            except Exception as shit:
                print("ну иди выключи компьютер")
            print(fuck)

        time.sleep(1)
