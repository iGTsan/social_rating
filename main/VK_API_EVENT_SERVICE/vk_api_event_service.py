import random, vk_api, os, time, sys, pika, json
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

def pika_auth():
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

    channel.queue_declare(queue='eventQueue')
    channel.queue_declare(queue='sendQueue')

if __name__ == "__main__":

    # time.sleep(30)

    # eventQueue = multiprocessing.Queue(maxsize=1000)
    # sendQueue = multiprocessing.Queue(maxsize=1000)
    # pipeQueue = multiprocessing.Queue(maxsize=100)
    # for i in range(50):
    #     pipeST , pipeED = multiprocessing.Pipe()
    #     tmp = {"start" : pipeST, "end" : pipeED}
    #     pipeQueue.put(tmp)

    pika_auth()

    isLocal = int(sys.argv[1])
    isProdigy = int(sys.argv[2])
    debug = int(sys.argv[3])

    LP = AutificationMain(isProdigy)

    # try:
    #     f = open('timing.txt', 'r')
    # except Exception:
    #     f = open('timing.txt', 'w')
    #     f.write("100")
    #     f.close()
    #     f = open('timing.txt', 'r')
    # TMP = int(f.readline())
    # f.close()

    # apiServiceProcess = multiprocessing.Process(target=apiService, args=(sendQueue, pipeQueue, isProdigy, debug,))
    # eventManagerProcess = multiprocessing.Process(target=eventManager, args=(eventQueue, isProdigy, isLocal, sendQueue, pipeQueue, debug,))
    # dailyTasksProcess = multiprocessing.Process(target=dailyTasks, args=(isProdigy, isLocal, sendQueue, pipeQueue, debug,))
    # apiServiceProcess.start()
    # eventManagerProcess.start()
    # dailyTasksProcess.start()

    commands = ["/писюн", "/топ", "/топ_все", "/ролл", "/чат", "/микс", "/мой_писюн", "/кострация"]

    while True:
        print("Ready")
        sys.stdout.flush()
        try:
            for event in LP.listen():

                if event.type == VkBotEventType.MESSAGE_NEW:
                    text = event.object["message"]["text"].lower()
                    if event.object["message"]["peer_id"] != event.object["message"]["from_id"]:
                        if text in commands:
                            channel.basic_publish(exchange='', routing_key='eventQueue', body=json.dumps(dict(event.object)))
                            #eventQueue.put(dict(event.object))

                    elif event.object["message"]["peer_id"] == event.object["message"]["from_id"]:
                        if text == "" or text[0] == "/" or text == "начать":
                            request = ("bot", "messages.send",
                                      {"peer_id": event.object["message"]["from_id"],
                                       "message": "Дружище, наш бот работает только в беседах. Здесь ты можешь задать вопрос разработчикам. Подпишись на нашу группу, чтобы не пропускать новости разработки и ежедневные топы бесед, а пока держи гайд: https://vk.com/@dickkraftbot-itak-prishlo-vremya-napisat-podrobnyi-gaid-na-bota",
                                       "random_id": random.randint(1, 2147483647)}, "OneWay")
                            channel.basic_publish(exchange='', routing_key='sendQueue', body=json.dumps(list(event.request)))
                            #sendQueue.put(request)
                        else:
                            continue
                elif event.type == "donut_subscription_create":
                    print("Мама, ноый донат)")
                elif event.type == "donut_subscription_expired":
                    print("Бля, минус дон(")

        except Exception as fuck:
            try:
                LP = AutificationMain(isProdigy)
                pika_auth()
                print("LP update")
            except Exception as shit:
                print("ну иди выключи компьютер")
            print(fuck)

        time.sleep(1)
