import random, requests, time, vk_api, os, json
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

fils = os.listdir(path=str(os.getcwd()))
for i in range(len(fils)):
    if fils[i][-1] == "n":
        with open(fils[i], "r", encoding='utf-8') as read_file:
            data = json.load(read_file)
        for j in data:
            print(j["name"])
            if j["name"][-12:] == " | ВКонтакте":
                j["name"] = j["name"][:-12]
            print(j["name"])
        with open(fils[i], "w", encoding='utf-8') as write_file:
            json.dump(data, write_file)