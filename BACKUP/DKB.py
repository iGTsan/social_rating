import random, requests, time, vk_api, os, json
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

vk = vk_api.VkApi(token="98aa138c77d7378f8db9e91450bf7f97d9919eb21c153a2f304322a24680e1ce66562bf159c338381fe31")
vk._auth_token()
vk.get_api()
LP = VkBotLongPoll(vk, 193557157)


def name(id, event):
    string = str(event.object["message"]["peer_id"])
    try:
        nm = open('name' + string + '.txt', 'r', encoding='utf-8')
    except Exception:
        nm = open('name' + string + '.txt', 'w', encoding='utf-8')
        nm.close()
        nm = open('name' + string + '.txt', 'r', encoding='utf-8')
    # print("это имена")
    tmp = list(nm.readlines())
    # print(tmp)
    for i in tmp:
        if str(list(i.split(","))[0]) == str(id):
            # print(list(i.split(","))[0], id)
            return list(i.split(","))[1][:-2]
    sss = "https://vk.com/id" + str(id)
    html_doc = requests.get(sss).text
    soup = BeautifulSoup(html_doc, features="html.parser")
    xxx = soup.find('title')
    tmp.append(str(id) + "," + str(xxx.get_text()) + " \n")
    nm.close()
    nm = open('name' + string + '.txt', 'w', encoding='utf-8')
    for i in tmp:
        nm.write(i)
    return str(xxx.get_text())


def delta(event):
    string = str(event.object["message"]["peer_id"])
    id = str(event.object["message"]["from_id"])
    try:
        pr = open(string + '.txt', 'r', encoding='utf-8')
    except Exception:
        pr = open(string + '.txt', 'w', encoding='utf-8')
        pr.close()
        pr = open(string + '.txt', 'r', encoding='utf-8')
    tmp = list(pr.readlines())
    # print(tmp)
    pr.close()
    pr = open(string + '.txt', 'w', encoding='utf-8')
    mark = True
    for i in range(len(tmp)):
        if tmp[i] == [' \n']:
            break
        line = tmp[i]
        if list(line.split())[0] == id:
            # print(line, ((int(list(line.split())[2]))/86400))
            if int((time.time() + 10800)/ 86400) - ((int(list(line.split())[2]))) < 1:
                vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                            "message": name(id, event) + ", ти сьогодні вже грав(",
                                            "random_id": 0})
                for j in tmp:
                    xxx = j.split()
                    # print(xxx)
                    pr.write(xxx[0] + " " + xxx[1] + " " + xxx[2] + " \n")
                pr.close()
                return
            mark = False
            #        print(id)
            fin = int(list(line.split())[1])
            ans = random.randint(-10, 10)
            if ans < 0:
                ans = random.randint(-10, 10)
            while ans == 0:
                ans = random.randint(-10, 10)
            #        print(ans, fin)
            if fin + ans <= 0:
                fin = 0
                vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                            "message": name(id, event) + ", у тебе відвалилася піська(",
                                            "random_id": 0})
            else:
                fin = fin + ans
                if ans > 0:
                    vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                                "message": name(id, event) + ", твій пісюн виріс на " + str(
                                                    ans) + " см. Тепер його довжина " + str(fin) + " см.",
                                                "random_id": 0})
                else:
                    vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                                "message": name(id, event) + ", твій пісюн зменшився на " + str(
                                                    -ans) + " см. Тепер його довжина " + str(fin) + " см.",
                                                "random_id": 0})
            tmp[i] = id + " " + str(fin) + " " + str(int((time.time() + 10800)/ 86400))

    if mark:
        ans = random.randint(0, 10)
        tmp.append(id + " " + str(ans) + " " + str(int((time.time() + 10800)/ 86400)))
        vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                    "message": name(id, event) + ", Вітаю в грі писюн, ти зіграв в перший раз і "
                                                                 "зараз твій пісюн має довжину " + str(ans),
                                    "random_id": 0})
    # print(str(tmp) + "??")
    for j in tmp:
        xxx = j.split()
        # print(xxx)
        pr.write(xxx[0] + " " + xxx[1] + " " + xxx[2] + " \n")
    pr.close()


# print(tmp)
# print("NEXT_ONE")

def kluch(arr):
    return int(arr[1])


def top_all(event, flag = False):
    if flag:
        string = event
    else:
        string = str(event.object["message"]["peer_id"])
    pr = open(string + '.txt', 'r', encoding='utf-8')
    tmp = list(pr.readlines())
    pr.close()
    arr = [list(tmp[i].split()) for i in range(len(tmp))]
    arr = sorted(arr, key=kluch)
    # print(arr)
    nm = open('name' + string + '.txt', 'r', encoding='utf-8')
    nms = list(nm.readlines())
    nmss = []
    for i in arr:
        for j in nms:
            if i[0] == str(list(j.split(","))[0]):
                nmss.append([i[1], str(list(j.split(","))[1])])
    nmss.reverse()
    ans = ""
    for i in range(len(tmp)):
        ans += str(nmss[i][1][:-2]) + " - " + str(nmss[i][0]) + " см." + " \n"
    if flag == False:
        vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                    "message": ans,
                                    "random_id": 0})
    if flag:
        vk.method("messages.send", {"peer_id": "231688699",
                                    "message": ans,
                                    "random_id": 0})
        return ans


def top(event):
    string = str(event.object["message"]["peer_id"])
    pr = open(string + '.txt', 'r', encoding='utf-8')
    tmp = list(pr.readlines())
    pr.close()
    arr = [list(tmp[i].split()) for i in range(len(tmp))]
    arr = sorted(arr, key=kluch)
    # print(arr)
    nm = open('name' + string + '.txt', 'r', encoding='utf-8')
    nms = list(nm.readlines())
    nmss = []
    for i in arr:
        for j in nms:
            if i[0] == str(list(j.split(","))[0]):
                nmss.append([i[1], str(list(j.split(","))[1])])
    nmss.reverse()
    ans = ""
    for i in range(min(len(tmp), 10)):
        ans += str(nmss[i][1][:-2]) + " - " + str(nmss[i][0]) + " см." + " \n"
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
    arr = ['0 0 1', '0 0 2', '0 0 3', '0 0 4', '0 0 5', '0 0 6', '0 0 7', '0 0 8', '0 0 9', '0 1 0', '0 1 1', '0 1 2', '0 1 3', '0 1 4', '0 1 5', '0 1 6', '0 1 7', '0 1 8', '0 1 9', '0 2 0', '0 2 1', '0 2 2', '0 2 3', '0 2 4', '0 2 5', '0 2 6', '0 2 7', '0 2 8', '0 2 9', '0 3 0', '0 3 1', '0 3 2', '0 3 3', '0 3 4', '0 3 5', '0 3 6', '0 3 7', '0 3 8', '0 3 9', '0 4 0', '0 4 1', '0 4 2', '0 4 3', '0 4 4', '0 4 5', '0 4 6', '0 4 7', '0 4 8', '0 4 9', '0 5 0', '0 5 1', '0 5 2', '0 5 3', '0 5 4', '0 5 5', '0 5 6', '0 5 7', '0 5 8', '0 5 9', '0 6 0', '0 6 1', '0 6 2', '0 6 3', '0 6 4', '0 6 5', '0 6 6', '0 6 7', '0 6 8', '0 6 9', '0 7 0', '0 7 1', '0 7 2', '0 7 3', '0 7 4', '0 7 5', '0 7 6', '0 7 7', '0 7 8', '0 7 9', '0 8 0', '0 8 1', '0 8 2', '0 8 3', '0 8 4', '0 8 5', '0 8 6', '0 8 7', '0 8 8', '0 8 9', '0 9 0', '0 9 1', '0 9 2', '0 9 3', '0 9 4', '0 9 5', '0 9 6', '0 9 7', '0 9 8', '0 9 9', '1 0 0']
    chislo = arr[random.randint(0, 99)]
    vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                "message": name(id, event) + " получает случайное число(1-100):  " + chislo,
                                "random_id": 0})

def summarry(event):
    string = str(event.object["message"]["peer_id"])
    pr = open(string + '.txt', 'r', encoding='utf-8')
    tmp = list(pr.readlines())
    pr.close()
    arr = [list(tmp[i].split()) for i in range(len(tmp))]
    summ = 0
    for i in arr:
        summ += int(i[1])
    vk.method("messages.send", {"peer_id": event.object["message"]["peer_id"],
                                "message": "Довжина писюна вашого чату " + str(
                                    summ) + " см.",
                                "random_id": 0})

def top_print():
    fils = os.listdir(path=str(os.getcwd()))
    arra = []
    for i in range(len(fils)):
        if fils[i][0].isdigit():
             arra.append(int(fils[i][:-4]))
    arra.sort()
    ans = []
    for i in arra:
        string = str(i)
        pr = open(string + '.txt', 'r', encoding='utf-8')
        tmp = list(pr.readlines())
        pr.close()
        arr = [list(tmp[i].split()) for i in range(len(tmp))]
        summ = 0
        for i in arr:
            summ += int(i[1])
        ans.append(summ)
    #print(ans)
    #print(arra)
    id = ans.index(max(ans))
    text = top_all(str(arra[id]), True)
    vk.method("messages.send", {"peer_id": "231688699",
                                "message": max(ans),
                                "random_id": 0})

if input("DEBUG? ") == str(1):
    TMP = time.time()
    while True:
        #top_print()
        print("Ready")
        try:
            for event in LP.listen():
                if time.time() - TMP > 86400:
                    top_print()
                    TMP = time.time()
                if event.type == VkBotEventType.MESSAGE_NEW:
                    print(event)
                    if event.object["message"]["peer_id"] != event.object["message"]["from_id"]:
                        if event.object["message"]["text"] == "/писюн":
                            print(time.asctime(), event.object)
                            TechRab(event)
                        elif event.object["message"]["text"] == "/топ":
                            TechRab(event)
                        elif event.object["message"]["text"] == "/топ_все":
                            TechRab(event)
                        elif event.object["message"]["text"] == "/ролл":
                            TechRab(event)
                        elif event.object["message"]["text"] == "/чат":
                            TechRab(event)
                    elif event.object["message"]["peer_id"] == event.object["message"]["from_id"]:
                        if event.object["message"]["text"][0] != "/":
                            print(time.asctime(), event.object)
                            vk.method("messages.send",
                                      {"peer_id": event.object["message"]["from_id"], "message": rand_gachi_text(),
                                       "random_id": random.randint(1, 2147483647)})
                        else:
                            print(time.asctime(), event.object)
                            vk.method("messages.send",
                                      {"peer_id": event.object["message"]["from_id"], "message": "Дружище, тот бот в ЛС посылает рандомные гачи фразы на украинском. Их пока мало, но можешь написать ещё в ЛС создателю группы, и он их добавит, или нет. Если ты хочешь померятся письками, то пригласи бота в любую беседу и напиши /писюн.",
                                       "random_id": random.randint(1, 2147483647)})
        except Exception as fuck:
            print(fuck)
        time.sleep(1)
else:
    TMP = time.time()
    while True:
        print("Ready")
        try:
            for event in LP.listen():
                if time.time() - TMP > 86400:
                    top_print()
                    TMP = time.time()
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if event.object["message"]["peer_id"] != event.object["message"]["from_id"]:
                        if event.object["message"]["text"].lower() == "/писюн":
                            print(time.asctime(), event.object)
                            delta(event)
                        elif event.object["message"]["text"].lower() == "/топ":
                            top(event)
                        elif event.object["message"]["text"].lower() == "/топ_все":
                            top_all(event)
                        elif event.object["message"]["text"].lower() == "/ролл":
                            roll(event)
                        elif event.object["message"]["text"].lower() == "/чат":
                            summarry(event)
                    elif event.object["message"]["peer_id"] == event.object["message"]["from_id"]:
                        if event.object["message"]["text"][0] != "/":
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