import requests, concurrent.futures, time, sys, pika, json, multiprocessing, re, os, random, datetime, threading, concurrent.futures, json
from utilities import *
from bs4 import BeautifulSoup

apiServiceURL = "http://vk_api_send:7331/api"
channel = None
connection = None

class Daily:
    def __init__(self, isProdigy, isLocal, debug):
        self.debug = debug
        self.isProdigy = isProdigy
        self.connection_pool = StartDB(isProdigy, isLocal)
        self.threads = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        self.run_arr = getRUN_arr(isProdigy)
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

    def start(self):
        while True:
            channel.basic_publish(exchange='', routing_key='heartbeat', body='heartbeat')
            time.sleep(5)
            try:
                f = open('timing.txt', 'r')
                TMP = int(f.readline())
                f.close()
                if current_hour() == 12 and TMP - current_day() < 0 or self.debug:
                    self.debug = 0
                    print("TOPS")
                    TMP = current_day()
                    f = open('timing.txt', 'w')
                    f.write(str(current_day()))
                    f.close()

                    connection_top_print = self.connection_pool.getconn()
                    connection_top_chel = self.connection_pool.getconn()
                    connection_remove_old = self.connection_pool.getconn()

                    pipes_top_print = multiprocessing.Pipe()
                    pipes_top_chel = self.pipeQueue.get()
                    pipes_remove_old = self.pipeQueue.get()

                    self.threads.submit(self.top_chel, connection_top_chel, pipes_top_chel)
                    self.threads.submit(self.top_print, connection_top_print, pipes_top_print)
                    self.threads.submit(self.remove_old, connection_remove_old, pipes_remove_old)
                    self.threads.submit(self.reload_audio)

                    if pipes_top_chel["end"].recv() and \
                            pipes_top_print["end"].recv() and \
                            pipes_remove_old["end"].recv():

                        self.connection_pool.putconn(connection_top_chel)
                        self.connection_pool.putconn(connection_top_print)
                        self.connection_pool.putconn(connection_remove_old)
                        self.pipeQueue.put(pipes_top_print)
                        self.pipeQueue.put(pipes_top_chel)
                        self.pipeQueue.put(connection_remove_old)
                        print("Done SUKA!!!")
            except Exception as shit:
                print(shit, "from DAILY")
                sys.stdout.flush()



    def reload_audio(self, pipes_remove_old):
        print("reload audio")
        ssyl = "https://vk.com/music/playlist/-193557157_1"
        html_doc = requests.get(ssyl).text
        soup = BeautifulSoup(html_doc, features="html.parser")
        arr_track = []
        for track in soup.find('div', 'AudioPlaylistRoot').find_all('div', 'audio_item'):
            tmp = str(track)[45:54]
            arr_track.append(str(tmp))
        f = open('tracks.txt', 'w')
        for i in range(len(arr_track) - 1):
            f.write(str(arr_track[i]))
            f.write(" \n")
        f.write(arr_track[-1])
        f.close()
        pipes_remove_old["start"].send("pepper")

    def is_admin(self, peer_id):
        data = ("is_admin_check", "messages.getConversationMembers", {"peer_id": peer_id}, "CallBack")
        check = requests.post(apiServiceURL, json=json.dumps(data)).json()["data"]
        return check

    def del_post(self, name):
        print("Deliting")
        f = open(name, 'r')
        tmp = f.readlines()
        tmp = tmp[0].split()
        tmp = tmp[1][:-1]
        f.close()

        event = ("admin", "wall.delete",
                        {"owner_id": "-" + self.run_arr[1], "post_id": tmp}, "OneWay")

        channel.basic_publish(exchange='', routing_key='sendQueue', body=json.dumps(event))

    def top_chel(self, connection, pipes_top_chel):
        print("top_chel")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM basechel ORDER BY len DESC")
        chel = cursor.fetchall()
        ans = []
        for i in chel:
            if self.is_admin(i[gpeerid]):
                besed_id = i[gpeerid]
                data = ("bot", "messages.getConversationsById", {"peer_ids": besed_id}, "CallBack")
                name = requests.post(apiServiceURL, json=json.dumps(data)).json()["data"]
                name = name["items"][0]["chat_settings"]["title"]
            else:
                name = "-"
            tmp = [i, name]

            ans.append(tmp)

            if len(ans) == 11:
                break
        s = "Лучшие челы сегодня:" + "\n" + "\n"
        for i in range(len(ans)):
            j = ans[i][0]
            s += str(str(i + 1) + ". " + j[gname] + " - " + str(j[glen]) + " см." + " (" + ans[i][1] + ")" + '\n')
        if self.isProdigy == False:
            self.del_post("Chels_ID.txt")
        data = ("admin", "wall.post", {
            "owner_id": "-" + self.run_arr[1],
            "message": s,
            "from_group": 1
        }, "CallBack")
        ID = requests.post(apiServiceURL, json=json.dumps(data)).json()["data"]
        if self.isProdigy == False:
            f = open('Chels_ID.txt', 'w')
            f.write(str(ID))
            f.close()
        pipes_top_chel["start"].send("pepper")


    def top_print(self, connection, pipes_top_print):
        print("top_print")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM basechel")
        chels = cursor.fetchall()
        tops = {}
        for chel in chels:
            peerid = chel[gpeerid]
            ln = chel[glen]
            nowlen = tops.get(peerid)
            if nowlen == None:
                tops.update({peerid: ln})
            else:
                tops.update({peerid: nowlen + ln})
        ans = [[i, j] for i, j in sorted(tops.items(), key=lambda item: -item[1])]
        tmp = []
        for i in range(len(ans)):
            peerid = ans[i][0]
            if self.is_admin(peerid):
                data = ("bot", "messages.getConversationsById", {"peer_ids": peerid}, "CallBack")
                name = requests.post(apiServiceURL, json=json.dumps(data)).json()["data"]
                name = name["items"][0]["chat_settings"]["title"]
                tmp.append([ans[i][1], name])
            if len(tmp) == 9:
                break
        tmpe = "Лучшие чаты сегодня:" + "\n" + "\n"

        for i in range(len(tmp)):
            tmpe += str(i + 1) + ". " + str(tmp[i][-1]) + ", довжина писюна вашого чату - " + str(tmp[i][0]) + " см." + "\n"
        if self.isProdigy == False:
            self.del_post("Chats_ID.txt")
        data = ("admin", "wall.post", {
            "owner_id": "-" + self.run_arr[1],
            "message": tmpe,
            "from_group": 1
        }, "CallBack")
        ID = requests.post(apiServiceURL, json=json.dumps(data)).json()["data"]
        if self.isProdigy == False:
            f = open('Chats_ID.txt', 'w')
            f.write(str(ID))
            f.close()
        pipes_top_print["start"].send("pepper")



    def remove_old(self, connection):
        print("remove old")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM basechel WHERE time<%s", (current_day() - 365))
        chel = cursor.fetchall()
        for i in chel:
            cursor.execute("DELETE FROM basechel WHERE peerid=%s and id=%s", (i[gpeerid], i[gid]))
        connection.commit()

if __name__ == '__main__':
    print("dailyTasks")
    sys.stdout.flush()
    isLocal = int(sys.argv[1])
    isProdigy = int(sys.argv[2])
    debug = int(sys.argv[3])
    try:
        tasks = Daily(isProdigy, isLocal, debug)
        tasks.start()
    except Exception as shit:
        print("dailyTasks", shit)