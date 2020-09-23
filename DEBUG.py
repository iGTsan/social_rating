import random, requests, time, vk_api, os, json, threading
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll


os.chdir("coversations")

with open("2000000001.json", "r") as read_file:
    pr = json.load(read_file)

print(pr)
with open(r"C:\Users\sergh\PycharmProjects\VK_DICK_BOT\coversations\ "[:-1] + str(2000000001) + ".json", "w", encoding='utf-8') as read_file:
            pr = json.load(read_file)
print(pr)