import random, requests, time, vk_api, os, json, threading, sqlite3, psycopg2, numpy
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from psycopg2 import Error, pool

ip = "172.23.166.223"

connection1 = psycopg2.pool.ThreadedConnectionPool(1, 50, user="DrBalanc",
                               # пароль, который указали при установке PostgreSQL
                               password="$stalker",
                               host=ip,
                               port="5432",
                               database="DrBalanc")

            # Создайте курсор для выполнения операций с базой данных



connection = psycopg2.pool.ThreadedConnectionPool(1, 50, user="S013k",
                               # пароль, который указали при установке PostgreSQL
                               password="$stalker",
                               host=ip,
                               port="5432",
                               database="S013k")

cnn = connection.getconn()
cursor = cnn.cursor()
cursor.execute("SELECT * FROM basechel")
chel = cursor.fetchall()

cnn = connection1.getconn()
cursor1 = cnn.cursor()
cursor1.execute(
    "CREATE TABLE IF NOT EXISTS basechel (globalid serial primary KEY, peerid INT, id INT, len INT, time INT, name TEXT, delta INT)")
cnn.commit()


def f(x):
    print("lol")
    global connection1
    connection = connection1.getconn()
    cursor = connection.cursor()
    # SQL-запрос для создания новой таблицы

    cursor.executemany(
        "INSERT INTO basechel (peerid, id, len, time, name, delta) VALUES(%s, %s, %s, %s, %s, %s)", [j[1:] for j in x])
    connection.commit()


chel = numpy.asarray(chel)
a = numpy.array_split(chel, 20)
for x in a:
    threading.Thread(target=f, args=[x]).start()

'''for x in chel:
    try:
        cursor.execute("INSERT OR UPDATE INTO basechel(globalid, peerid, id, len, time, name, delta) VALUES(%s, %s, %s, %s, %s, %s, %s);",
                       [x[0], x[1], x[2], x[3], x[4], x[5], x[6]])
        connection.commit()
        #print(x)
    except Exception as fuck:
        a = 1
        #print(fuck)
cursor.execute("SELECT * FROM basechel")
chel = cursor.fetchall()

print(len(chel))'''