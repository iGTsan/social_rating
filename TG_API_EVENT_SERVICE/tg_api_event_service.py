import telebot, sys, pika, time, json, threading
import time
from prometheus_client import start_http_server, Histogram

REQUEST_TIME = Histogram('tg_request_processing_seconds', 'Time spent processing request')


# time.sleep(30)
def AutificationMain(isProdigy):
    if isProdigy:
        RUN = open("RUNProdigy.txt", "r")
        RUN_arr = RUN.readlines()
        token = RUN_arr[0][:-1]
        bot = telebot.TeleBot(token, num_threads=4)
        RUN.close()
        return bot
    else:
        RUN = open("RUN.txt", "r")
        RUN_arr = RUN.readlines()
        token = RUN_arr[0][:-1]
        bot = telebot.TeleBot(token, num_threads=4)
        RUN.close()
        return bot


# eventQueue = multiprocessing.Queue(maxsize=1000)
# sendQueue = multiprocessing.Queue(maxsize=1000)
# pipeQueue = multiprocessing.Queue(maxsize=100)
# for i in range(50):
#     pipeST , pipeED = multiprocessing.Pipe()
#     tmp = {"start" : pipeST, "end" : pipeED}
#     pipeQueue.put(tmp)
isLocal = int(sys.argv[1])
isProdigy = int(sys.argv[2])
debug = int(sys.argv[3])

bot = AutificationMain(isProdigy)

COMMANDS = [
    "/соціальный_рейтинг",
    "/топ",
    "/топ_все",
    "/ролл",
    "/чат",
    "/микс",
    "/мой_соціальный_рейтинг",
    "/маргинализация",
]

channel = 0


@bot.message_handler(func=lambda message: message.text in COMMANDS)
def send_welcome(message):
    if debug:
        print(message)

    global channel
    print(message)
    sys.stdout.flush()

    event = {
        "message": {
            "date": message.date,
            "from_id": message.from_user.id,
            "id": 0,
            "text": message.text,
            "peer_id": message.chat.id,
            "username": message.from_user.username,
        },
        "start_time": time.time(),
    }

    while True:
        try:
            channel.basic_publish(
                exchange="",
                routing_key="eventQueue",
                body=json.dumps(event),
            )
            break
        except Exception as exp:
            while True:
                try:
                    sys.stdout.flush()
                    connection = pika.BlockingConnection(
                        pika.ConnectionParameters(
                            "rabbitmq" if isProdigy == False else "rabbitmq_dev"
                        )
                    )
                    channel = connection.channel()
                    break
                except Exception:
                    print("Failed to connect to RabbitMQ")
                    sys.stdout.flush()
                    time.sleep(2)
                    continue
            channel.queue_declare(queue="eventQueue")
            channel.basic_publish(
                exchange="",
                routing_key="eventQueue",
                body=json.dumps(event),
            )
            time.sleep(0.5)


def async_handle_answer(bot):

    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    "rabbitmq" if isProdigy == False else "rabbitmq_dev"
                )
            )
            channel = connection.channel()
            break
        except Exception:
            print("Failed to connect to RabbitMQ")
            sys.stdout.flush()
            time.sleep(2)
            continue

    def callback(ch, method, properties, body):
        event = json.loads(body)
        bot.send_message(event[2]["peer_id"], event[2]["message"])
        request_time = time.time() - event[-1]["start_time"]
        request_time *= 1000
        sys.stdout.flush()
        print("Request processing time = " + str(request_time) + " seconds")
        sys.stdout.flush()
        REQUEST_TIME.observe(request_time)

    channel.basic_consume(
        queue="sendQueueTG", auto_ack=True, on_message_callback=callback
    )

    channel.start_consuming()


# for event in LP.listen():

#     if event.type == VkBotEventType.MESSAGE_NEW:
#         text = event.object["message"]["text"].lower()
#         if (
#             event.object["message"]["peer_id"]
#             != event.object["message"]["from_id"]
#         ):
#             if text in commands:
#                 channel.basic_publish(
#                     exchange="",
#                     routing_key="eventQueue",
#                     body=json.dumps(dict(event.object)),
#                 )
#                 # eventQueue.put(dict(event.object))

#         elif (
#             event.object["message"]["peer_id"]
#             == event.object["message"]["from_id"]
#         ):
#             if text == "" or text[0] == "/" or text == "начать":
#                 request = (
#                     "bot",
#                     "messages.send",
#                     {
#                         "peer_id": event.object["message"]["from_id"],
#                         "message": "Дружище, наш бот работает только в беседах. Здесь ты можешь задать вопрос разработчикам. Подпишись на нашу группу, чтобы не пропускать новости разработки и ежедневные топы бесед, а пока держи гайд: https://vk.com/@social_rating_kraftbot-itak-prishlo-vremya-napisat-podrobnyi-gaid-na-bota",
#                         "random_id": random.randint(1, 2147483647),
#                     },
#                     "OneWay",
#                 )
#                 channel.basic_publish(
#                     exchange="",
#                     routing_key="sendQueue",
#                     body=json.dumps(list(event.request)),
#                 )
#                 # sendQueue.put(request)
#             else:
#                 continue
#     elif event.type == "donut_subscription_create":
#         print("Мама, ноый донат)")
#     elif event.type == "donut_subscription_expired":
#         print("Блин, минус дон(")

if __name__ == "__main__":
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    "rabbitmq" if isProdigy == False else "rabbitmq_dev"
                )
            )
            channel = connection.channel()
            break
        except Exception:
            print("Failed to connect to RabbitMQ")
            sys.stdout.flush()
            time.sleep(2)
            continue

    channel.queue_declare(queue="eventQueue")
    channel.queue_declare(queue="sendQueueTG")
    12
    while True:
        try:
            start_http_server(8000)
            break
        except Exception:
            print("Failed to start Prometheus client")
            sys.stdout.flush()
            time.sleep(2)
            continue

    print("Ready")
    sys.stdout.flush()

    answer_handler_thread = threading.Thread(target=async_handle_answer, args=(bot,))
    answer_handler_thread.start()

    bot.infinity_polling(
        allowed_updates=["message"],
        long_polling_timeout=1,
    )
