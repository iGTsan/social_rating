import sys, pika, json, concurrent.futures, multiprocessing
import random, requests
from utilities import *

threadPool = None
channel = None
connection_pool = None
innerQueue = None
apiServiceURL = None

def start_event(target, event):
    #print(event)
    connection = connection_pool.getconn()
    returnValue = target(event, connection)
    #print(returnValue)
    connection_pool.putconn(connection)
    for request in returnValue:
        print("inner Queue", request)
        innerQueue.put(request)

def gen_new(id):
    print("HELLO FROM GENNEW")
    sys.stdout.flush()


    id = str(id)
    if id[0] == '-':
        return 0
    else:
        id = str(id)
        tmp = {"id": "", "len": "", "time": "", "name": ""}
        tmp["id"], tmp["len"], tmp["time"] = id, str(random.randint(1, 10)), str(current_day())
        # pipes = pipeQueue.get()
        # sendQueue.put(("bot", "users.get", {"user_ids": str(id)}, "CallBack", pipes))
        # nm_tmp = pipes["end"].recv()
        # pipes["end"].send("banana")
        print("Sending request")
        sys.stdout.flush()
        data = ("bot", "users.get", {"user_ids": str(id)}, "CallBack")
        nm_tmp = requests.post(apiServiceURL, json=json.dumps(data))
        # print(nm_tmp)
        # print(nm_tmp.text)
        # print(nm_tmp.json())
        # print(nm_tmp.json()["data"][0])
        # print(nm_tmp.json()["data"][0]["first_name"])
        nm_tmp = nm_tmp.json()["data"]
        print("Got data", nm_tmp)
        sys.stdout.flush()

        name = nm_tmp[0]["first_name"] + " " + nm_tmp[0]["last_name"]
        tmp["name"] = str(name)
        if tmp["name"][-12:] == " | ВКонтакте":
            tmp["name"] = tmp["name"][:-12]

        print(tmp)
        sys.stdout.flush() 
        return tmp

def delta(event, connection):

    print("HELLO FROM DELTA")
    sys.stdout.flush()

    returnValue = []
    cursor = connection.cursor()
    string = str(event["message"]["peer_id"])
    id = str(event["message"]["from_id"])
    day = current_day()
    cursor.execute("SELECT * FROM basechel WHERE peerid=%s and id=%s", [int(string), int(id)])
    chel = cursor.fetchone()
    if chel != None:
        print("NE NONE")
        sys.stdout.flush()


        chel = list(chel)
        if day - (int(chel[gtime])) < 1:
            cursor.close()
            return [("bot", "messages.send", {"peer_id": event["message"]["peer_id"],
                                        "message": chel[gname] + ", ти сьогодні вже грав(",
                                        "random_id": 0}, "OneWay")]
        fin = int(chel[glen])
        ans = random.randint(-10, 10)
        if ans < 0:
            ans = random.randint(-10, 10)
        while ans == 0:
            ans = random.randint(-10, 10)
        #        print(ans, fin)
        if fin + ans <= 0:
            fin = 0
            returnValue = [("bot", "messages.send", {"peer_id": event["message"]["peer_id"],
                                        "message": chel[gname] + ", у тебе відвалилася соціальный рейтинг(",
                                        "random_id": 0}, "OneWay")]
        else:
            fin = fin + ans
            if ans > 0:
                returnValue = [("bot", "messages.send", {"peer_id": event["message"]["peer_id"],
                                            "message": chel[gname] + ", твій соціальный рейтинг виріс на " + str(
                                                ans) + " очков. Тепер його довжина " + str(fin) + " очков.",
                                            "random_id": 0}, "OneWay")]
            else:
                returnValue = [("bot", "messages.send", {"peer_id": event["message"]["peer_id"],
                                            "message": chel[gname] + ", твій соціальный рейтинг зменшився на " + str(
                                                -ans) + " очков. Тепер його довжина " + str(fin) + " очков.",
                                            "random_id": 0}, "OneWay")]
        chel[glen] = int(fin)
        chel[gtime] = int(current_day())
        cursor.execute("UPDATE basechel set len = %s, time = %s where globalid = %s",
                                (chel[glen], chel[gtime], chel[gglobalid]))
        connection.commit()

    if chel == None:
        print("NONE")
        sys.stdout.flush()

        new_chel = gen_new(id)
        if new_chel == 0:
            returnValue = [("bot", "messages.send", {"peer_id": event["message"]["peer_id"],
                                        "message": "Боти не можуть користуватися цим ботом!",
                                        "random_id": 0}, "OneWay")]
        else:
            returnValue = [("bot", "messages.send", {"peer_id": event["message"]["peer_id"],
                                        "message": new_chel["name"] + ", Вітаю в грі соціальный рейтинг, ти зіграв в перший раз і "
                                                                        "зараз твій соціальный рейтинг має довжину " + new_chel[
                                                        "len"] + " очков.",
                                        "random_id": 0}, "OneWay")]
            tchel = (
                int(string), int(id), int(new_chel["len"]), int(new_chel["time"]), str(new_chel["name"]), 0)
            cursor.execute("INSERT INTO basechel (peerid, id, len, time, name, delta) VALUES(%s, %s, %s, %s, %s, %s)", tchel)
            connection.commit()
    cursor.close()
    print(returnValue)
    sys.stdout.flush() 
    return returnValue

def top_all(event, connection):
    returnValue = []
    cursor = connection.cursor()
    string = str(event["message"]["peer_id"])
    cursor.execute("SELECT * FROM basechel WHERE peerid=%s", (int(string),))
    chel = cursor.fetchall()
    pr = sorted(chel, key=lambda tmp: -int(tmp[glen]))
    ans = ""
    counter = 0
    tmp = 0
    flag = 1
    while flag:
        flag = 0
        while tmp < len(pr):
            counter = 0
            ans = ""
            for i in range(tmp, len(pr)):
                if counter > 4000:
                    flag = 1
                    break
                ans += str(tmp+1) + ". " + pr[i][gname] + " - " + str(pr[i][glen]) + " очков." + " \n"
                counter = len(ans)
                tmp += 1
            if ans != "":
                returnValue.append(("bot", "messages.send", {"peer_id": event["message"]["peer_id"],
                                            "message": ans,
                                            "random_id": 0}, "OneWay"))
        else:
            break
    cursor.close()
    return returnValue

def top(event, connection):
    returnValue = []
    #print("123125456t436743")
    cursor = connection.cursor()
    string = str(event["message"]["peer_id"])
    cursor.execute("SELECT * FROM basechel WHERE peerid=%s", (int(string),))
    chel = cursor.fetchall()
    pr = sorted(chel, key=lambda tmp: -int(tmp[glen]))
    ans = ""
    for i in range(min(10, len(pr))):
        ans += str(i+1) + ". " + pr[i][gname] + " - " + str(pr[i][glen]) + " очков." + " \n"
    cursor.close()
    if ans != "":
        returnValue = [("bot", "messages.send", {"peer_id": event["message"]["peer_id"],
                                "message": ans,
                                "random_id": 0}, "OneWay")]
    return returnValue

def rand_gachi_text():
    gachi = ["Гей, приятель, я думаю, ти помилився дверима, Шкіряний клуб знаходиться в двох кварталах звідси." + "\n ",
                "трахнути тебе♂" + "\n ",
                "Ох, та пішов ти, Шкіряний мужик. Може бути, нам з тобою варто залагодити це прямо тут, на рингу, якщо ти вважаєш себе таким крутим." + "\n ",
                "Ха! Так, правильно, хлопець. Пішли звідси! Чому б тобі не позбутися від цієї шкіряної гидоти%s Я зараз роздягнуся, і ми всі владнаємо прямо тут, на рингу. А ти що скажеш%s" + "\n"]
    tmp = str(random.choice(gachi))
    return tmp

def TechRab(event, connection):
    return [("bot", "messages.send", {"peer_id": event["message"]["peer_id"],
                                "message": "Тыкни попозже, ведутся техработы.",
                                "random_id": 0}, "OneWay")]

def roll(event, connection):
    cursor = connection.cursor()
    id = str(event["message"]["from_id"])
    string = str(event["message"]["peer_id"])
    arr = ['0 0 1', '0 0 2', '0 0 3', '0 0 4', '0 0 5', '0 0 6', '0 0 7', '0 0 8', '0 0 9', '0 1 0', '0 1 1', '0 1 2',
            '0 1 3', '0 1 4', '0 1 5', '0 1 6', '0 1 7', '0 1 8', '0 1 9', '0 2 0', '0 2 1', '0 2 2', '0 2 3', '0 2 4',
            '0 2 5', '0 2 6', '0 2 7', '0 2 8', '0 2 9', '0 3 0', '0 3 1', '0 3 2', '0 3 3', '0 3 4', '0 3 5', '0 3 6',
            '0 3 7', '0 3 8', '0 3 9', '0 4 0', '0 4 1', '0 4 2', '0 4 3', '0 4 4', '0 4 5', '0 4 6', '0 4 7', '0 4 8',
            '0 4 9', '0 5 0', '0 5 1', '0 5 2', '0 5 3', '0 5 4', '0 5 5', '0 5 6', '0 5 7', '0 5 8', '0 5 9', '0 6 0',
            '0 6 1', '0 6 2', '0 6 3', '0 6 4', '0 6 5', '0 6 6', '0 6 7', '0 6 8', '0 6 9', '0 7 0', '0 7 1', '0 7 2',
            '0 7 3', '0 7 4', '0 7 5', '0 7 6', '0 7 7', '0 7 8', '0 7 9', '0 8 0', '0 8 1', '0 8 2', '0 8 3', '0 8 4',
            '0 8 5', '0 8 6', '0 8 7', '0 8 8', '0 8 9', '0 9 0', '0 9 1', '0 9 2', '0 9 3', '0 9 4', '0 9 5', '0 9 6',
            '0 9 7', '0 9 8', '0 9 9', '1 0 0']
    chislo = arr[random.randint(0, 99)]
    cursor.execute("SELECT * FROM basechel WHERE peerid=%s and id=%s", (int(string), int(id)))
    chel = cursor.fetchone()
    cursor.close()
    if chel == None:
        return [("bot", "messages.send", {"peer_id": event["message"]["peer_id"],
                                    "message": "Гарний хлопець получает случайное число(1-100):  " + chislo,
                                    "random_id": 0}, "OneWay")]
    else:
        return [("bot", "messages.send", {"peer_id": event["message"]["peer_id"],
                                    "message": chel[gname] + " получает случайное число(1-100):  " + chislo,
                                    "random_id": 0}, "OneWay")]

def summarry(event, connection):
    cursor = connection.cursor()
    string = str(event["message"]["peer_id"])
    cursor.execute("SELECT * FROM basechel WHERE peerid=%s", (int(string),))
    chel = cursor.fetchall()
    summ = 0
    for i in chel:
        summ += int(i[glen])
    cursor.close()
    return [("bot", "messages.send", {"peer_id": event["message"]["peer_id"],
                                "message": "Довжина соціального рейтинга вашого чату " + str(
                                    summ) + " очков.",
                                "random_id": 0}, "OneWay")]

def sound(event, connection):
    print("HELLO FROM SOUND")
    sys.stdout.flush() 
    with open ('tracks.txt', 'r') as f:
        arr_track = f.readlines()
        string = str(event["message"]["peer_id"])
        return [("bot", "messages.send", {"peer_id": string,
                                        "message": rand_gachi_text(),
                                        "attachment": f"audio{-193557157}_{str(random.choice(arr_track))}",
                                        "random_id": random.randint(1, 2147483647)}, "OneWay")]

def my_rating(event, connection):
    cursor = connection.cursor()
    string = str(event["message"]["peer_id"])
    id = str(event["message"]["from_id"])
    cursor.execute("SELECT * FROM basechel WHERE peerid=%s and id=%s", (int(string), int(id)))
    chel = cursor.fetchone()
    if chel == None:
        cursor.close()
        return [("bot", "messages.send", {"peer_id": string,
                                    "message": "Пробач, брате, але в тебе ще немає соціального рейтинга",
                                    "random_id": 0}, "OneWay")]
    else:
        cursor.close()
        return [("bot", "messages.send", {"peer_id": string,
                                    "message": chel[gname] + ", довжина твого соціального рейтинга " + str(chel[glen]) + " очков.",
                                    "random_id": 0}, "OneWay")]

def remove_rating(event, connection):
    cursor = connection.cursor()
    string = str(event["message"]["peer_id"])
    id = str(event["message"]["from_id"])
    cursor.execute("SELECT * FROM basechel WHERE peerid=%s and id=%s", (int(string), int(id)))
    chel = cursor.fetchone()
    if chel == None:
        returnValue = [("bot", "messages.send", {"peer_id": string,
                                    "message": "Пробач, брате, але в тебе ще немає соціального рейтинга",
                                    "random_id": 0}, "OneWay")]
    else:
        cursor.execute("DELETE FROM basechel WHERE peerid=%s and id=%s", (int(string), int(id)))
        returnValue = [("bot", "messages.send", {"peer_id": string,
                                    "message": chel[gname] + ", вітаю, ти відрізав собі соціальный рейтинг. Назавжди!",
                                    "random_id": 0}, "OneWay")]
    connection.commit()
    cursor.close()
    return returnValue

def callback(ch, method, properties, body):
    event = json.loads(body)
    #print(" [x] Received %r" % data)
    #sys.stdout.flush()
    try: 
        if debug and event["message"]["text"][0] == "/":
            threadPool.submit(start_event, TechRab, event)

        elif event["message"]["text"].lower() == "/соціальный_рейтинг":
            threadPool.submit(start_event, delta, event)
        elif event["message"]["text"].lower() == "/топ":
            threadPool.submit(start_event, top, event)
        elif event["message"]["text"].lower() == "/топ_все":
            threadPool.submit(start_event, top_all, event)
        elif event["message"]["text"].lower() == "/ролл":
            threadPool.submit(start_event, roll, event)
        elif event["message"]["text"].lower() == "/чат":
            threadPool.submit(start_event, summarry, event)
        elif event["message"]["text"].lower() == "/микс":
            threadPool.submit(start_event, sound, event)
        elif event["message"]["text"].lower() == "/мой_соціальный_рейтинг":
            threadPool.submit(start_event, my_rating, event)
        elif event["message"]["text"].lower() == "/маргинализация":
            threadPool.submit(start_event, remove_rating, event)
    except Exception as excpt:
        print(excpt)
        sys.stdout.flush()

def innerQueueManager(innerQueue, isProdigy):
    while True:
        try:
            while True:
                try:
                    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq' if isProdigy == False else 'rabbitmq_dev'))
                    channel = connection.channel()
                    break
                except Exception:
                    print("Failed to connect to RabbitMQ")
                    sys.stdout.flush()
                    time.sleep(2)
                    continue

            channel.queue_declare(queue='sendQueue')

            while True:
                event = innerQueue.get()
                print("innerQueueManager", event)
                sys.stdout.flush()
                channel.basic_publish(exchange='', routing_key='sendQueue', body=json.dumps(event))
                
        except Exception as excpt:
            print("innerQueueManager", excpt)
            sys.stdout.flush()

if __name__ == "__main__":

    isLocal = int(sys.argv[1])
    isProdigy = int(sys.argv[2])
    debug = int(sys.argv[3])

    apiServiceURL = "http://vk_api_send_dev:7331/api" if isProdigy else "http://vk_api_send:7331/api"

    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq' if isProdigy == False else 'rabbitmq_dev'))
            channel = connection.channel()
            break
        except Exception:
            print("Failed to connect to RabbitMQ")
            sys.stdout.flush()
            time.sleep(2)
            continue

    channel.queue_declare(queue='eventQueue')


    threadPool = concurrent.futures.ThreadPoolExecutor(max_workers=32)
    connection_pool = StartDB(isProdigy, isLocal)
    innerQueue = multiprocessing.Queue(maxsize=1000)

    innerQueueProcess = multiprocessing.Process(target=innerQueueManager, args=(innerQueue, isProdigy,))
    innerQueueProcess.start()

#def eventManager(eventQueue, isProdigy, isLocal, sendQueue, pipeQueue, debug):

    if debug:
        test_event = {'message': {'date': 1669403763, 'from_id': 231688699, 'id': 0, 'out': 0, 'attachments': [], 'conversation_message_id': 610, 'fwd_messages': [], 'important': False, 'is_hidden': False, 'peer_id': 2000000001, 'random_id': 0, 'text': '/топ'}, 'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link', 'callback', 'intent_subscribe', 'intent_unsubscribe'], 'keyboard': True, 'inline_keyboard': True, 'carousel': True, 'lang_id': 0}}
        threadPool.submit(start_event, delta, test_event)
        threadPool.submit(start_event, top, test_event)
        threadPool.submit(start_event, top_all, test_event)
        threadPool.submit(start_event, roll, test_event)
        threadPool.submit(start_event, summarry, test_event)
        threadPool.submit(start_event, sound, test_event)
        threadPool.submit(start_event, my_rating, test_event)
        threadPool.submit(start_event, remove_rating, test_event)

    channel.basic_consume(queue='eventQueue',
                      auto_ack=True,
                      on_message_callback=callback)

    print("EventManager STARTED!")
    sys.stdout.flush()

    channel.start_consuming()