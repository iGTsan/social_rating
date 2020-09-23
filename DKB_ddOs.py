import random, requests, time, vk_api, os, json, threading, sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
gpeerid = 1
gid = 2
glen = 3
gtime = 4
gname = 5
RUN = open('RUN_anime.txt', 'r')
RUN_arr = RUN.readlines()
vk = vk_api.VkApi(token=RUN_arr[0][:-1])
vk._auth_token()
api = vk.get_api()
LP = VkBotLongPoll(vk, RUN_arr[1])
RUN.close()
def send_photo(peer_id, owner_id, photo_id, access_key, name):
    api.messages.send(peer_id=peer_id,
                      message=name,
                      attachment=f'photo{owner_id}_{photo_id}_{access_key}',
                      random_id=random.randint(1, 2147483647))
while True:
    print("Ready")
    dick_thread = 0
    try:
        for event in LP.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.object["message"]["peer_id"] != event.object["message"]["from_id"]:
                    if event.object["message"]["text"] == "/аниме":
                        api.messages.send(peer_id=event.object["message"]["peer_id"],
                                          message="Через в течении 30 секунд запрос будет обработан.",
                                          random_id=random.randint(1, 2147483647))
                        flag = 1
                        for item in event.object['message']['attachments']:
                            #print(1)
                            if item['type'] == 'photo':
                                flag = 0
                                #print(2)
                                tmp = []
                                for i in item['photo']['sizes']:
                                    tmp.append(int(i['width']))
                                m = max(tmp)
                                for i in range(len(tmp)):
                                    if tmp[i] == m:
                                        img = item['photo']['sizes'][i]['url']
                                        break
                                print(img)
                                p = requests.get(img)
                                out = open("TMPimg.jpg", "wb")
                                out.write(p.content)
                                out.close()
                                ssyl = "https://trace.moe/"
                                op = webdriver.ChromeOptions()
                                op.add_argument('--headless')
                                driver = webdriver.Chrome(options=op)
                                driver.get(ssyl)
                                time.sleep(3)
                                driver.find_element_by_xpath("//input[@type='file']").send_keys(os.getcwd()+"/TMPimg.jpg")
                                time.sleep(17)
                                soup = BeautifulSoup(driver.page_source, features="lxml")
                                driver.close()
                                name = soup.find('div', class_='info_title__9CCp5').get_text()
                                send_photo(event.object["message"]["peer_id"], item['photo']['owner_id'],
                                           item['photo']['id'], item['photo']['access_key'], name)
                                break
                        if flag:
                            api.messages.send(peer_id=event.object["message"]["peer_id"],
                                              message="Некорректный запрос(",
                                              random_id=random.randint(1, 2147483647))
    except Exception as fuck:
        print("fuck", fuck)
    time.sleep(1)