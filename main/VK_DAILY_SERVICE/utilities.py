import time, psycopg2, multiprocessing
from psycopg2 import Error, pool

gglobalid = 0
gpeerid = 1
gid = 2
glen = 3
gtime = 4
gname = 5


def getRUN_arr(isProdigy):
    if isProdigy:
        RUN = open('RUNProdigy.txt', 'r')
        RUN_arr = RUN.readlines()
        RUN.close()
        return RUN_arr
    else:
        RUN = open('RUN.txt', 'r')
        RUN_arr = RUN.readlines()
        RUN.close()
        return RUN_arr


def current_day():
    return int(((time.time() + 10800) / 86400))


def current_hour():
    return int(((time.time() + 10800) % 86400) / 3600)

def StartDB(isProdigy, isLocal):
    ip = None
    if isLocal:
        ip = "db"
    else:
        ip = "172.23.166.223"
    if isProdigy:
        for i in range(12):
            try:
                # Подключиться к существующей базе данных
                connection_pool = psycopg2.pool.ThreadedConnectionPool(10, 50, user="S013k",
                                                                       # пароль, который указали при установке PostgreSQL
                                                                       password="K0ntR0L3r",
                                                                       host=ip,
                                                                       #port="5432"
                                                                       database="dkb_vk")
                print("Подключились к PostgreSQL")
                return connection_pool

            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
                time.sleep(5)

        return None
    else:
        for i in range(12):
            try:
                connection_pool = psycopg2.pool.ThreadedConnectionPool(10, 50, user="S013k",
                                                                       # пароль, который указали при установке PostgreSQL
                                                                       password="K0ntR0L3r",
                                                                       host=ip,
                                                                       # port="5432"
                                                                       database="dkb_vk")
                print("Подключились к PostgreSQL")
                return connection_pool

            except (Exception, Error) as error:
                time.sleep(5)
                print("Ошибка при работе с PostgreSQL", error)

        return None
