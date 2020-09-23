import random, requests, time, vk_api, os, json, threading, sqlite3
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

RUN = open('RUN.txt', 'r')
RUN_arr = RUN.readlines()
vk = vk_api.VkApi(token=RUN_arr[0][:-1])
vk._auth_token()
api = vk.get_api()
LP = VkBotLongPoll(vk, RUN_arr[1])
RUN.close()

def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True
    return key, remember_device

vk_admin = vk_api.VkApi('+79015992170', 'yAnEtorcH', auth_handler=auth_handler)
vk_admin.auth()
vk_admin.get_api()

connection = sqlite3.connect('base505.db')
cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS basechel (globalid INT PRIMARY KEY, peerid INT, id INT, len INT, time INT, name TEXT, delta INT)")
connection.commit()

gpeerid = 1
gid = 2
glen = 3
gtime = 4
gname = 5


def current_day():
    return int(((time.time() + 10800) / 86400))


def current_hour():
    return int(((time.time() + 10800) % 86400) / 3600)


def is_admin(peer_id):
    try:
        vk.method("messages.getConversationMembers", {"peer_id": peer_id})
    except Exception:
        return False
    return True


def gen_new(id):
    id = str(id)
    tmp = {"id": "", "len": "", "time": "", "name": ""}
    tmp["id"], tmp["len"], tmp["time"] = id, str(random.randint(1, 10)), str(current_day())
    nm_tmp = vk.method("users.get", {"user_ids": str(id)})
    name = nm_tmp[0]["first_name"] + " " + nm_tmp[0]["last_name"]
    tmp["name"] = str(name)
    if tmp["name"][-12:] == " | ВКонтакте":
        tmp["name"] = tmp["name"][:-12]
    return tmp


def delta(event):
    string = str(event.object["message"]["peer_id"])
    id = str(event.object["message"]["from_id"])
    if ban(event):
        day = 0
    else:
        day = current_day()
    cursor.execute("SELECT * FROM basechel WHERE peerid=? and id=?", (int(string), int(id)))
    chel = cursor.fetchone()
    if chel != None:
        chel = list(chel)
        if day - (int(chel[gtime])) < 1:
            vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                        "message": chel[gname] + ", ти сьогодні вже грав(",
                                        "random_id": 0})
            return
        fin = int(chel[glen])
        ans = random.randint(-10, 10)
        if ans < 0:
            ans = random.randint(-10, 10)
        while ans == 0:
            ans = random.randint(-10, 10)
        #        print(ans, fin)
        if fin + ans <= 0:
            fin = 0
            vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                        "message": chel[gname] + ", у тебе відвалилася піська(",
                                        "random_id": 0})
        else:
            fin = fin + ans
            if ans > 0:
                vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                            "message": chel[gname] + ", твій пісюн виріс на " + str(
                                                ans) + " см. Тепер його довжина " + str(fin) + " см.",
                                            "random_id": 0})
            else:
                vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                            "message": chel[gname] + ", твій пісюн зменшився на " + str(
                                                -ans) + " см. Тепер його довжина " + str(fin) + " см.",
                                            "random_id": 0})
        chel[glen] = int(fin)
        chel[gtime] = int(current_day())
        cursor.execute("REPLACE INTO basechel VALUES(?, ?, ?, ?, ?, ?, ?);", chel)
        connection.commit()

    if chel == None:
        new_chel = gen_new(id)
        vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                    "message": new_chel["name"] + ", Вітаю в грі писюн, ти зіграв в перший раз і "
                                                                  "зараз твій пісюн має довжину " + new_chel["len"],
                                    "random_id": 0})
        RUN = open("GLOBALID", 'r')
        globalid = int(RUN.read())
        RUN.close()
        tchel = (globalid, int(string), int(id), int(new_chel["len"]), int(new_chel["time"]), str(new_chel["name"]), 0)
        cursor.execute("INSERT OR REPLACE INTO basechel VALUES(?, ?, ?, ?, ?, ?, ?);", tchel)
        connection.commit()
        globalid += 1
        RUN = open("GLOBALID", 'w')
        RUN.write(str(globalid))
        RUN.close()


def top_all(event):
    string = str(event.object["message"]["peer_id"])
    cursor.execute("SELECT * FROM basechel WHERE peerid=?", (int(string),))
    chel = cursor.fetchall()
    pr = sorted(chel, key=lambda tmp: -int(tmp[glen]))
    ans = ""
    counter = 0
    tmp = 0
    for i in range(len(pr)):
        if counter > 4000:
            break
        ans += pr[i][gname] + " - " + str(pr[i][glen]) + " см." + " \n"
        tmp += 1
        counter = len(ans)
    vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                "message": ans,
                                "random_id": 0})
    if counter >= 4000:
        while tmp <= len(pr):
            counter = 0
            ans = ""
            for i in range(tmp, len(pr)):
                ans += pr[i][gname] + " - " + str(pr[i][glen]) + " см." + " \n"
                counter = len(ans)
                tmp += 1
            vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                        "message": ans,
                                        "random_id": 0})


def top(event):
    string = str(event.object["message"]["peer_id"])
    cursor.execute("SELECT * FROM basechel WHERE peerid=?", (int(string),))
    chel = cursor.fetchall()
    pr = sorted(chel, key=lambda tmp: -int(tmp[glen]))
    ans = ""
    for i in range(min(10, len(pr))):
        ans += pr[i][gname] + " - " + str(pr[i][glen]) + " см." + " \n"
    vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                "message": ans,
                                "random_id": 0})


def rand_gachi_text():
    gachi = ["Гей, приятель, я думаю, ти помилився дверима, Шкіряний клуб знаходиться в двох кварталах звідси." + "\n ",
             "трахнути тебе♂" + "\n ",
             "Ох, та пішов ти, Шкіряний мужик. Може бути, нам з тобою варто залагодити це прямо тут, на рингу, якщо ти вважаєш себе таким крутим." + "\n ",
             "Ха! Так, правильно, хлопець. Пішли звідси! Чому б тобі не позбутися від цієї шкіряної гидоти? Я зараз роздягнуся, і ми всі владнаємо прямо тут, на рингу. А ти що скажеш?" + "\n"]
    tmp = str(random.choice(gachi))
    return tmp


def TechRab(event):
    vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                "message": "Тыкни попозже, ведутся техработы",
                                "random_id": 0})


def roll(event):
    id = str(event.object["message"]["from_id"])
    string = str(event.object["message"]["peer_id"])
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
    cursor.execute("SELECT * FROM basechel WHERE peerid=? and id=?", (int(string), int(id)))
    chel = cursor.fetchone()
    vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                "message": chel[gname] + " получает случайное число(1-100):  " + chislo,
                                "random_id": 0})


def summarry(event):
    string = str(event.object["message"]["peer_id"])
    cursor.execute("SELECT * FROM basechel WHERE peerid=?", (int(string),))
    chel = cursor.fetchall()
    summ = 0
    for i in chel:
        summ += int(i[glen])
    vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                "message": "Довжина писюна вашого чату " + str(
                                    summ) + " см.",
                                "random_id": 0})


def top_chel():
    cursor.execute("SELECT * FROM basechel ORDER BY len DESC")
    chel = cursor.fetchall()
    #print(chel)
    ans = []
    for i in chel:
        if is_admin(i[gpeerid]):
            besed_id = i[gpeerid]
            # print(vk.method("messages.getConversationsById", {"peer_ids": besed_id}))
            # print(vk.method("messages.getConversations"))
            name = vk.method("messages.getConversationsById", {"peer_ids": besed_id})["items"][0]["chat_settings"][
                "title"]
        else:
            name = "-"
        tmp = [i, name]
        #print(tmp)
        if tmp[0][gid] in [i[0][gid] for i in ans]:
            print("AAAAAAAAAA")
            print([i[0][gid] for i in ans])
            print("BBBBBBBBBBBB")
            num = [i[0][gid] for i in ans].index(tmp[0][gid])
            if ans[num][0][glen] < tmp[0][glen]:
                ans[num] = tmp
        else:
            ans.append(tmp)


        if len(ans) == 11:
            break
    #print(ans)
    s = "Лучшие челы сегодня:" + "\n" + "\n"
    for i in range(len(ans)):
        j = ans[i][0]
        s += str(str(i + 1) + ". " + j[gname] + " - " + str(j[glen]) + " см." + " (" + ans[i][1] + ")" + '\n')
    # vk.method("messages.send",
    #         {"peer_id": "310573776", "message": s,
    #         "random_id": random.randint(1, 2147483647)})
    # vk.method("messages.send",
    #         {"peer_id": "231688699", "message": s,
    #         "random_id": random.randint(1, 2147483647)})
    del_post("Chels_ID.txt")
    ID = vk_admin.method("wall.post", {
        "owner_id": "-" + RUN_arr[1],
        "message": s,
        "from_group": 1
    })
    f = open('Chels_ID.txt', 'w')
    f.write(str(ID))
    f.close()


def top_print():
    cursor.execute("SELECT peerid FROM basechel")
    ids = list(set(cursor.fetchall()))
    for i in range(len(ids)):
        ids[i] = ids[i][0]
    ans = []
    for id in ids:
        sum = 0
        cursor.execute("SELECT * FROM basechel WHERE peerid=?", (id,))
        for i in cursor.fetchall():
            sum += int(i[glen])
        ans.append([id, sum])
    #print(ans)
    # print(vk.method("messages.getConversations"))
    # vk.method("messages.send", {"chat_id": "2", "message": "пососи", "random_id": random.randint(1, 2147483647)})
    # vk.method("messages.editChat", {"chat_id": "2", "title": "1488 1488"})
    # print(vk.method("messages.getConversationMembers", {"peer_id": "2000000001"}))
    # print(vk.method("messages.getConversationMembers", {"peer_id": "2000000002"}))
    # print(vk.method("messages.getConversationsById", {"peer_ids": "2000000001, 2000000002"}))
    tmp = []
    ans.sort(key= lambda x: -x[1])
    #print(ans)
    for i in range(len(ans)):
        #print(len(tmp), tmp)
        # print(tmp[i])
        peerid = ans[i][0]
        if is_admin(peerid):
            # print(vk.method("messages.getConversationsById", {"peer_ids": tmp[i][0]}))
            # print(vk.method("messages.getConversationsById", {"peer_ids": tmp[i][0]})["items"][0]["chat_settings"]["title"])
            name = vk.method("messages.getConversationsById", {"peer_ids": peerid})["items"][0]["chat_settings"][
                    "title"]
            # print(vk.method("messages.getConversationsById", {"peer_ids": tmp[i][0]}))
            tmp.append([ans[i][1], name])
        if len(tmp) == 9:
            break
    tmpe = "Лучшие чаты сегодня:" + "\n" + "\n"
    # print(ans)

    for i in range(len(tmp)):
        tmpe += str(i + 1) + ". " + str(tmp[i][-1]) + ", довжина писюна вашого чату - " + str(tmp[i][0]) + " см." + "\n"
    # print(tmpe)
    # vk.method("messages.send",
    #         {"peer_id": "310573776", "message": tmpe,
    #         "random_id": random.randint(1, 2147483647)})
    # vk.method("messages.send",
    #         {"peer_id": "231688699", "message": tmpe,
    #         "random_id": random.randint(1, 2147483647)})
    del_post("Chats_ID.txt")
    ID = vk_admin.method("wall.post", {
        "owner_id": "-" + RUN_arr[1],
        "message": tmpe,
        "from_group": 1
    })
    f = open('Chats_ID.txt', 'w')
    f.write(str(ID))
    f.close()


# for i in range(len(ans)):
#    print(ans[i])
#   ans["items"]
# vk.method("messages.send", {"peer_id": "2000000001",
#         "message": "пососи",
#        "random_id": 0})
def del_post(name):
    f = open(name, 'r')
    tmp = f.readlines()
    tmp = tmp[0].split()
    tmp = tmp[1][:-1]
    f.close()
    vk_admin.method("wall.delete",
                    {"owner_id": "-" + RUN_arr[1], "post_id": tmp})


def ban(event):
    if event.object["message"]["from_id"] == "603472198":
        return 18540
    else:
        return 0


def reload_audio():
    ssyl = "https://vk.com/music/playlist/-193557157_1"
    html_doc = requests.get(ssyl).text
    soup = BeautifulSoup(html_doc, features="html.parser")
    arr_track = []
    for track in soup.find('div', 'AudioPlaylistRoot').find_all('div', 'audio_item'):
        tmp = str(track)[45:54]
        # print(tmp)
        arr_track.append(str(tmp))
    f = open('tracks.txt', 'w')
    for i in range(len(arr_track) - 1):
        f.write(str(arr_track[i]))
        f.write(" \n")
    f.write(arr_track[-1])
    f.close()


def sound(event):
    f = open('tracks.txt', 'r')
    arr_track = f.readlines()
    string = str(event.object["message"]["peer_id"])
    api.messages.send(peer_id=string,
                      message=rand_gachi_text(),
                      attachment=f"audio{-193557157}_{str(random.choice(arr_track))}",
                      random_id=random.randint(1, 2147483647))
    f.close()


def my_cock(event):
    string = str(event.object["message"]["peer_id"])
    id = str(event.object["message"]["from_id"])
    cursor.execute("SELECT * FROM basechel WHERE peerid=? and id=?", (int(string), int(id)))
    chel = cursor.fetchone()
    vk.method("messages.send", {"peer_id": string,
                                "message": chel[gname] + ", довжина твого писюна " + str(chel[glen]) + " см.",
                                "random_id": 0})


if input("DEBUG? ") == str(1):
    # reload_audio()
    #top_chel()
    #top_print()
    # del_post("Chels_ID.txt")
    while True:
        print("Ready")
        try:
            for event in LP.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    print(event)
                    if event.object["message"]["peer_id"] != event.object["message"]["from_id"]:
                        if event.object["message"]["text"][0] == "/":
                            # print(time.asctime(), event.object)
                            TechRab(event)
                    elif event.object["message"]["peer_id"] == event.object["message"]["from_id"]:
                        if event.object["message"]["text"][0] != "/" or event.object["message"]["text"][0] != "Начать":
                            # print(time.asctime(), event.object)
                            vk.method("messages.send",
                                      {"peer_id": event.object["message"]["from_id"], "message": rand_gachi_text(),
                                       "random_id": random.randint(1, 2147483647)})
                        else:
                            # print(time.asctime(), event.object)
                            vk.method("messages.send",
                                      {"peer_id": event.object["message"]["from_id"],
                                       "message": "Дружище, тот бот в ЛС посылает рандомные гачи фразы на украинском. Их пока мало, но можешь написать ещё в ЛС создателю группы, и он их добавит, или нет. Если ты хочешь померятся письками, то пригласи бота в любую беседу и напиши /писюн.",
                                       "random_id": random.randint(1, 2147483647)})
        except Exception as fuck:
            print(fuck)
        time.sleep(1)
else:
    try:
        f = open('timing.txt', 'r')
    except Exception:
        f = open('timing.txt', 'w')
        f.write("10000000000000000000")
        f.close()
        f = open('timing.txt', 'r')
    TMP = int(f.readline())
    f.close()
    while True:
        print("Ready")
        dick_thread = 0
        try:
            for event in LP.listen():
                if current_hour() == 12 and TMP - current_day() < 0:
                    TMP = current_day()
                    f = open('timing.txt', 'w')
                    f.write(str(current_day()))
                    f.close()
                    top_chel()
                    top_print()
                    reload_audio()
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if event.object["message"]["peer_id"] != event.object["message"]["from_id"]:
                        """if event.object["message"]["text"][0] == "/":
                            peer_id = str(event.object["message"]["peer_id"])
                            try:
                                vk.method("messages.getConversationMembers", {"peer_id": peer_id})
                            except Exception:
                                vk.method("messages.send",
                                          {"peer_id": peer_id,
                                           "message": "Для корректной работы бота необходимо сделать администратором беседы!",
                                           "random_id": random.randint(1, 2147483647)})
                                print(time.asctime(), event.object)
                                continue"""
                        if event.object["message"]["text"].lower() == "/писюн":
                            #print(time.asctime(), event.object)
                            #print()
                            """if dick_thread != 0:
                                dick_thread.join()

                            dick_thread = threading.Thread(target=delta, args=(event,))
                            dick_thread.start()"""
                            delta(event)
                        elif event.object["message"]["text"].lower() == "/топ":
                            # threading.Thread(target=top, args=(event,)).start()
                            top(event)
                        elif event.object["message"]["text"].lower() == "/топ_все":
                            # threading.Thread(target=top_all, args=(event,)).start()
                            top_all(event)
                        elif event.object["message"]["text"].lower() == "/ролл":
                            # threading.Thread(target=roll, args=(event,)).start()
                            roll(event)
                        elif event.object["message"]["text"].lower() == "/чат":
                            # threading.Thread(target=summarry, args=(event,)).start()
                            summarry(event)
                        elif event.object["message"]["text"].lower() == "/микс":
                            # threading.Thread(target=sound, args=(event,)).start()
                            sound(event)
                        elif event.object["message"]["text"].lower() == "/мой_писюн":
                            # threading.Thread(target=my_cock, args=(event,)).start()
                            my_cock(event)
                    elif event.object["message"]["peer_id"] == event.object["message"]["from_id"]:
                        if event.object["message"]["text"][0] == "/" or event.object["message"][
                            "text"].lower() == "начать":
                            print(time.asctime(), event.object)
                            vk.method("messages.send",
                                      {"peer_id": event.object["message"]["from_id"],
                                       "message": "Дружище, наш бот работает только в беседах. Здесь ты можешь задать вопрос разработчикам. Подпишись на нашу группу, чтобы не пропускать новости разработки и ежедневные топы бесед, а пока держи гайд: https://vk.com/@dickkraftbot-itak-prishlo-vremya-napisat-podrobnyi-gaid-na-bota",
                                       "random_id": random.randint(1, 2147483647)})
                        else:
                            continue
                            print(time.asctime(), event.object)
                            vk.method("messages.send",
                                      {"peer_id": event.object["message"]["from_id"], "message": rand_gachi_text(),
                                       "random_id": random.randint(1, 2147483647)})



        except Exception as fuck:
            print(fuck)
        time.sleep(1)
