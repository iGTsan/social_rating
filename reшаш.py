import random, requests, time, vk_api, os, json, sqlite3
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

connection = sqlite3.connect('base505.db')
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS adminka (peerid INT PRIMARY KEY, iss BOOL, name TEXT)")
connection.commit()
RUN = open('RUN.txt', 'r')
RUN_arr = RUN.readlines()
vk = vk_api.VkApi(token=RUN_arr[0][:-1])
vk._auth_token()
api = vk.get_api()
LP = VkBotLongPoll(vk, RUN_arr[1])
RUN.close()
vk_admin = vk_api.VkApi('+79998776270', '27ezaguf')
vk_admin.auth()
vk_admin.get_api()

def is_admin(peer_id):
    try:
        vk.method("messages.getConversationMembers", {"peer_id": peer_id})
    except Exception:
        return False
    return True


tmp = "OnlineShop Fortnite 🔥"

cursor.execute("SELECT * FROM basechel WHERE peerid=?", (2000003436,))
chely = list(set(cursor.fetchall()))
print(chely)
ch = []
for i in chely:
    ch.append(list(i))
for i in range(len(ch)):
    ch[i][3] = 0
print(ch)
for i in ch:
    cursor.execute("INSERT OR REPLACE INTO basechel VALUES(?, ?, ?, ?, ?, ?, ?);", i)

connection.commit()