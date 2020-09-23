import random, requests, time, vk_api, os, json, sqlite3
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

connection = sqlite3.connect('base505.db')
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS basechel (globalid INT PRIMARY KEY, peerid INT, id INT, len INT, time INT, name TEXT, delta INT)")
connection.commit()


fils = os.listdir(path=str(os.getcwd()))
globalid = 0
for i in range(len(fils)):
    if fils[i][-4:] == "json" and '0' <= fils[i][0] <= '9':
        with open(fils[i], "r", encoding='utf-8') as read_file:
            data = json.load(read_file)
        for j in data:
            chel = (globalid, int(fils[i][:-5]), int(j["id"]), int(j["len"]), int(j["time"]), j["name"], 0)
            cursor.execute("INSERT INTO basechel VALUES(?, ?, ?, ?, ?, ?, ?);", chel)
            connection.commit()
            globalid += 1
        print(globalid)
print(globalid)
RUN = open("GLOBALID", 'w')
RUN.write(str(globalid))
RUN.close()