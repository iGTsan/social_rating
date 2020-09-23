import random, requests, time, vk_api, os, json
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll


fils = os.listdir(path=str(os.getcwd()))
ans = []
for i in range(len(fils)):
    if fils[i][0].isdigit():
        with open(fils[i], "r", encoding='utf-8') as read_file:
            pr = json.load(read_file)
        tmp = ans
        for j in pr:
            tmp.append(j)
        tmp = sorted(tmp, key=lambda x: -int(x["len"]))
        ans = []
        for j in tmp:
            flag = True
            for k in ans:
                if k["id"] == j["id"]:
                    flag = False
            if flag:
                ans.append(j)
print(len(ans))