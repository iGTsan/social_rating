import random, requests, time, vk_api, os, json, threading
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

RUN = open('RUN.txt', 'r')
RUN_arr = RUN.readlines()
vk = vk_api.VkApi(token=RUN_arr[0][:-1])
vk._auth_token()
vk.get_api()
LP = VkBotLongPoll(vk, RUN_arr[1])
RUN.close()
vk_admin = vk_api.VkApi('+79998776270', '27ezaguf')
vk_admin.auth()
vk_admin.get_api()


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
    try:
        with open(string + '.json', "r", encoding='utf-8') as read_file:
            pr = json.load(read_file)
    except Exception:
        pr = []
        with open(string + '.json', "w", encoding='utf-8') as write_file:
            json.dump(pr, write_file)
        with open(string + '.json', "r", encoding='utf-8') as read_file:
            pr = json.load(read_file)
    mark = True
    for i in range(len(pr)):
        if len(pr) == 0:
            break
        if pr[i]["id"] == id:
            if day - ((float(pr[i]["time"]))) < 1:
                vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                            "message": pr[i]["name"] + ", ти сьогодні вже грав(",
                                            "random_id": 0})
                return
            mark = False
            fin = int(pr[i]["len"])
            ans = random.randint(-10, 10)
            if ans < 0:
                ans = random.randint(-10, 10)
            while ans == 0:
                ans = random.randint(-10, 10)
            #        print(ans, fin)
            if fin + ans <= 0:
                fin = 0
                vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                            "message": pr[i]["name"] + ", у тебе відвалилася піська(",
                                            "random_id": 0})
            else:
                fin = fin + ans
                if ans > 0:
                    vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                                "message": pr[i]["name"] + ", твій пісюн виріс на " + str(
                                                    ans) + " см. Тепер його довжина " + str(fin) + " см.",
                                                "random_id": 0})
                else:
                    vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                                "message": pr[i]["name"] + ", твій пісюн зменшився на " + str(
                                                    -ans) + " см. Тепер його довжина " + str(fin) + " см.",
                                                "random_id": 0})
            pr[i]["len"] = str(fin)
            pr[i]["time"] = str(current_day())
            with open(string + ".json", "w", encoding='utf-8') as write_file:
                json.dump(pr, write_file)

    if mark:
        chel = gen_new(id)
        vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                    "message": chel["name"] + ", Вітаю в грі писюн, ти зіграв в перший раз і "
                                                              "зараз твій пісюн має довжину " + chel["len"],
                                    "random_id": 0})
        chel = json.dumps(chel)
        f = open(string + '.json', 'a+', encoding='utf-8')  # открываем с курсором на конце
        if len(pr) == 0:
            f.seek(f.truncate(f.tell() - 1))
            f.write(str(chel) + ']')
            f.close()
        else:
            f.seek(f.truncate(f.tell() - 1))  # обрезаем хвост и переходим в конец
            f.write("," + str(chel) + ']')
            f.close()


def top_all(event):
    string = str(event.object["message"]["peer_id"])
    with open(string + '.json', "r", encoding='utf-8') as read_file:
        pr = json.load(read_file)
    pr = sorted(pr, key=lambda tmp: -int(tmp["len"]))
    ans = ""
    counter = 0
    tmp = 0
    for i in range(len(pr)):
        if counter > 4000:
            break
        ans += pr[i]["name"] + " - " + pr[i]["len"] + " см." + " \n"
        tmp = i
        counter = len(ans)
    vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                "message": ans,
                                "random_id": 0})
    ans = ""
    if counter >= 4000:
        for i in range(tmp, len(pr)):
            ans += pr[i]["name"] + " - " + pr[i]["len"] + " см." + " \n"

        vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                "message": ans,
                                "random_id": 0})



def top(event):
    string = str(event.object["message"]["peer_id"])
    with open(string + '.json', "r", encoding='utf-8') as read_file:
        pr = json.load(read_file)
    pr = sorted(pr, key=lambda tmp: -int(tmp["len"]))
    ans = ""
    for i in range(min(10, len(pr))):
        ans += pr[i]["name"] + " - " + pr[i]["len"] + " см." + " \n"
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
    with open(string + ".json", "r", encoding='utf-8') as read_file:
        pr = json.load(read_file)
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
    for i in pr:
        if i["id"] == id:
            vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                        "message": i["name"] + " получает случайное число(1-100):  " + chislo,
                                        "random_id": 0})


def summarry(event):
    string = str(event.object["message"]["peer_id"])
    with open(string + '.json', "r", encoding='utf-8') as read_file:
        pr = json.load(read_file)
    summ = 0
    for i in pr:
        summ += int(i["len"])
    vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                "message": "Довжина писюна вашого чату " + str(
                                    summ) + " см.",
                                "random_id": 0})


def top_chel():
    fils = os.listdir(path=str(os.getcwd()))
    ans = []
    nms= []
    for i in range(len(fils)):
        if fils[i][0].isdigit():
            if is_admin(fils[i][:-5]):
                besed_id = fils[i][:-5]
                name = vk.method("messages.getConversationsById", {"peer_ids": besed_id})["items"][0]["chat_settings"]["title"]
            else:
                name = "-"
            with open(fils[i], "r", encoding='utf-8') as read_file:
                pr = json.load(read_file)
            tmp = ans
            for j in pr:
                tmp.append([j, name])
            tmp = sorted(tmp, key=lambda x: -int(x[0]["len"]))
            ans = []
            for j in tmp:
                if len(ans) == 11:
                    break
                flag = True
                for k in ans:
                    #print(k)
                    #print(j)
                    if k[0]["id"] == j[0]["id"]:
                        flag = False
                if flag:
                    ans.append(j)

    s = "Лучшие челы сегодня:" + "\n" + "\n"
    for i in range(len(ans)):
        j = ans[i][0]
        s += str(str(i + 1) + ". " + j["name"] + " - " + str(j["len"]) + " см." + " (" + ans[i][1] + ")" + '\n')
    vk.method("messages.send",
              {"peer_id": "310573776", "message": s,
               "random_id": random.randint(1, 2147483647)})
    vk.method("messages.send",
              {"peer_id": "231688699", "message": s,
               "random_id": random.randint(1, 2147483647)})
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
    fils = os.listdir(path=str(os.getcwd()))
    ans = []
    tmp = []
    for i in range(len(fils)):
        if fils[i][0].isdigit():
            with open(fils[i], "r", encoding='utf-8') as read_file:
                pr = json.load(read_file)
            summ = 0
            for j in pr:
                summ += int(j["len"])
            ans.append(summ)
            tmp.append(fils[i])
    fils = tmp
    for i in range(len(tmp)):
        tmp[i] = [fils[i], ans[i]]
    tmp = sorted(tmp, key=lambda i: -i[1])
    for i in range(len(tmp)):
        tmp[i][0] = tmp[i][0][:-5]
    # print(tmp)
    ans = []

    # print(vk.method("messages.getConversations"))
    # vk.method("messages.send", {"chat_id": "2", "message": "пососи", "random_id": random.randint(1, 2147483647)})
    # vk.method("messages.editChat", {"chat_id": "2", "title": "1488 1488"})
    # print(vk.method("messages.getConversationMembers", {"peer_id": "2000000001"}))
    # print(vk.method("messages.getConversationMembers", {"peer_id": "2000000002"}))
    # print(vk.method("messages.getConversationsById", {"peer_ids": "2000000001, 2000000002"}))
    for i in range(len(tmp)):
        # print(tmp[i])
        if is_admin(tmp[i][0]):
            temp = tmp[i]
            # print(vk.method("messages.getConversationsById", {"peer_ids": tmp[i][0]}))
            # print(vk.method("messages.getConversationsById", {"peer_ids": tmp[i][0]})["items"][0]["chat_settings"]["title"])
            temp.append(
                vk.method("messages.getConversationsById", {"peer_ids": tmp[i][0]})["items"][0]["chat_settings"][
                    "title"])
            # print(vk.method("messages.getConversationsById", {"peer_ids": tmp[i][0]}))
            ans.append(temp)
        if len(ans) == 9:
            break
    tmpe = "Лучшие чаты сегодня:" + "\n" + "\n"
    # print(ans)

    for i in range(len(ans)):
        tmpe += str(i + 1) + ". " + str(ans[i][-1]) + ", довжина писюна вашого чату - " + str(ans[i][1]) + " см." + "\n"
    # print(tmpe)
    vk.method("messages.send",
              {"peer_id": "310573776", "message": tmpe,
               "random_id": random.randint(1, 2147483647)})
    vk.method("messages.send",
              {"peer_id": "231688699", "message": tmpe,
               "random_id": random.randint(1, 2147483647)})
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

if input("DEBUG? ") == str(1):
    #=top_print()
    #top_chel()
    # del_post("Chels_ID.txt")
    while True:
        print("Ready")
        try:
            for event in LP.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    print(event)
                    if event.object["message"]["peer_id"] != event.object["message"]["from_id"]:
                        if event.object["message"]["text"][0] == "/":
                            print(time.asctime(), event.object)
                            TechRab(event)
                    elif event.object["message"]["peer_id"] == event.object["message"]["from_id"]:
                        if event.object["message"]["text"][0] != "/" or event.object["message"]["text"][0] != "Начать":
                            print(time.asctime(), event.object)
                            vk.method("messages.send",
                                      {"peer_id": event.object["message"]["from_id"], "message": rand_gachi_text(),
                                       "random_id": random.randint(1, 2147483647)})
                        else:
                            print(time.asctime(), event.object)
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
        try:
            for event in LP.listen():
                if current_hour() == 12 and TMP - current_day() < 0:
                    TMP = current_day()
                    f = open('timing.txt', 'w')
                    f.write(str(current_day()))
                    f.close()
                    top_chel()
                    top_print()
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
                            print(time.asctime(), event.object)
                            print()
                            threading.Thread(target=delta, args=(event,)).start()
                            #delta(event)
                        elif event.object["message"]["text"].lower() == "/топ":
                            threading.Thread(target=top, args=(event,)).start()
                            #top(event)
                        elif event.object["message"]["text"].lower() == "/топ_все":
                            threading.Thread(target=top_all, args=(event,)).start()
                            #top_all(event)
                        elif event.object["message"]["text"].lower() == "/ролл":
                            threading.Thread(target=roll, args=(event,)).start()
                            #roll(event)
                        elif event.object["message"]["text"].lower() == "/чат":
                            threading.Thread(target=summarry, args=(event,)).start()
                            #summarry(event)
                    elif event.object["message"]["peer_id"] == event.object["message"]["from_id"]:
                        if event.object["message"]["text"][0] == "/" or event.object["message"]["text"].lower() == "начать":
                            print(time.asctime(), event.object)
                            vk.method("messages.send",
                                      {"peer_id": event.object["message"]["from_id"],
                                       "message": "Дружище, тот бот в ЛС посылает рандомные гачи фразы на украинском. Их пока мало, но можешь написать ещё в ЛС создателю группы, и он их добавит, или нет. Если ты хочешь померятся письками, то пригласи бота в любую беседу и напиши /писюн.",
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
#test