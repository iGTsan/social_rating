import random, requests, time, vk_api, os, json
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

# -*- coding: utf-8 -*-


vk = vk_api.VkApi(token="98aa138c77d7378f8db9e91450bf7f97d9919eb21c153a2f304322a24680e1ce66562bf159c338381fe31")
vk._auth_token()
vk.get_api()
LP = VkBotLongPoll(vk, 193557157)

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

string = str(
    "!!!ВАЖНАЯ ИНФОРМАЦИЯ!! СЕРЁЖА ГАЙДУК - ЕБЛАКЛАК БОТ ПОКА НЕ РАБОТАЕТ ЗАВТРА ВЕСЬ АДМИН СОСТАВ ДАСТ ЕМУ ПИЗДЫ СПАСИБО ЗА ПОНИМАНИЕ")
string.encode('ascii', errors='xmlcharrefreplace')

for i in range(len(tmp)):
    try:
        vk.method("messages.send",
                  {"peer_id": int(tmp[i][0]), "message": string,
                   "random_id": random.randint(1, 2147483647)})
    except Exception as fuck:
        print(fuck)
        os.remove(tmp[i][0] + '.json')
