import random, requests, time, vk_api, os, json, threading, sqlite3, discord
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from discord.ext import commands
import asyncio
from discord.ext import tasks

d_token = "ODE1MjAwMTE1NDgwMTk5MTY4.YDo8RQ.wUMiIEt9V6zyeIG--DGh-VVvNLk"
bot = commands.Bot(command_prefix="/", intents=discord.Intents.default())

connection = sqlite3.connect('d_base505.db')
cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS basechel (globalid INT PRIMARY KEY, peerid INT, id INT, len INT, time INT, name TEXT, delta INT)")
connection.commit()
client = discord.Client(intents=discord.Intents.default())

gpeerid = 1
gid = 2
glen = 3
gtime = 4
gname = 5


def current_day():
    return int(((time.time() + 10800) / 86400))


def current_hour():
    return int(((time.time() + 10800) % 86400) / 3600)


def gen_new(ctx):
    id = ctx.author.id
    tmp = {"id": "", "len": "", "time": "", "name": ""}
    tmp["id"], tmp["len"], tmp["time"] = id, str(random.randint(1, 10)), str(current_day())
    name = ctx.author.name
    tmp["name"] = str(name)
    if tmp["name"][-12:] == " | ВКонтакте":
        tmp["name"] = tmp["name"][:-12]
    return tmp

async def nsfw_check(ctx):
    if not(ctx.channel.is_nsfw()):
        await ctx.respond(
                    f'{ctx.author.mention}, вибач, але ця команда працює тільки в NSFW каналах.')
        return 1
    return 0

'''
@bot.command()
async def ok(ctx):
    channel = bot.get_channel(815230126903656468)
    await channel.send(f'Hello, {author.mention} пидарас!')
    print(ctx.message)
    print(ctx.message.author.id)
    print(ctx.message.guild.id)
    print(ctx.message.author.name)
    author = ctx.message.author
    await ctx.send(f'Hello, {author.mention} пидарас!')
'''
@bot.slash_command(name="help", guild_ids=None, description = "список доступных команд")
async def хэлп(ctx):
    await ctx.respond("""Основные функции (NSFW):
/писюн - раз в день наращивает ваш личный болт;
/мой_писюн - выводит вашу личную длину;
/топ - выводит топ 10 писек сервера;
/топ_все - выводит топ всех писек на сервере;
/чат - выводит суммарную длину вашего сервера;
/кострация - сбрасывает до нуля всё наращенное (и удаляет вас из нащих баз!).

Рандомные случайно добавленные фичи (Work in progress):
/ролл - позволяет пойти на мид (случайное число 0-100)

Политика конфиденциальности и правила использования доступна по ссылочкам 
https://vk.com/@dickkraftbot-privacy-policy
https://vk.com/@dickkraftbot-terms-of-service
https://docs.google.com/document/d/1LWCtroAp5JwAN95LUdGakD-1jOOMrNpruriW-P8agig/edit?usp=sharing

Написать разработчикам можно по тегам: 
-bourobon#7651
-Ch4in4opa#7554
-DrBalanc#2952
-S013k#4649""", ephemeral=True)

@bot.slash_command(name="писюн", guild_ids=None, description = "раз в день наращивает ваш личный болт")
async def писюн(ctx):
    if (await nsfw_check(ctx)):
        return
    string = ctx.guild.id    #str(ctx.message.guild.id)
    id = ctx.author.id   #str(ctx.message.author.id)
    author = ctx.author   #ctx.message.author
    day = current_day()
    cursor.execute("SELECT * FROM basechel WHERE peerid=? and id=?", (int(string), int(id)))
    chel = cursor.fetchone()
    if chel != None:
        chel = list(chel)
        if day - (int(chel[gtime])) < 1:
            await ctx.respond(f'{author.mention}, ти сьогодні вже грав(')
            return
        fin = int(chel[glen])
        ans = random.randint(-10, 10)
        if ans < 0:
            ans = random.randint(-10, 10)
        while ans == 0:
            ans = random.randint(-10, 10)
        #        print(ans, fin)
        if fin + ans <= 0:
            fin = 0
            await ctx.respond(f'{author.mention}, у тебе відвалилася піська(')
        else:
            fin = fin + ans
            if ans > 0:
                await ctx.respond(f'{author.mention}, твій пісюн виріс на {str(ans)}см. Тепер його довжина {str(fin)} см.')
            else:
                await ctx.respond(
                    f'{author.mention}, твій пісюн зменшився на {str(-ans)}см. Тепер його довжина {str(fin)} см.')
        chel[glen] = int(fin)
        chel[gtime] = int(current_day())
        cursor.execute("REPLACE INTO basechel VALUES(?, ?, ?, ?, ?, ?, ?);", chel)
        connection.commit()

    if chel == None:
        new_chel = gen_new(ctx)

        await ctx.respond(
            f'{author.mention}, Вітаю в грі писюн, ти зіграв в перший раз і зараз твій пісюн має довжину {new_chel["len"]} см.')

        RUN = open("GLOBALID", 'r')
        globalid = int(RUN.read())
        RUN.close()
        tchel = (globalid, int(string), int(id), int(new_chel["len"]), int(new_chel["time"]), str(new_chel["name"]), 0)
        cursor.execute("INSERT OR REPLACE INTO basechel VALUES(?, ?, ?, ?, ?, ?, ?);", tchel)
        connection.commit()
        globalid += 1
        RUN = open("GLOBALID", 'w')
        RUN.write(str(globalid))
        RUN.close()


@bot.slash_command(name="топ_все", guild_ids=None, description = "выводит топ всех писек на сервере")
async def топ_все(ctx):
    if (await nsfw_check(ctx)):
        return
    string = ctx.guild.id  # str(ctx.message.guild.id)
    #string = str(ctx.message.guild.id)
    cursor.execute("SELECT * FROM basechel WHERE peerid=?", (int(string),))
    chel = cursor.fetchall()
    pr = sorted(chel, key=lambda tmp: -int(tmp[glen]))
    ans = ""
    counter = 0
    tmp = 0
    flag = 1
    await ctx.respond("Топ:")
    while flag:
        flag = 0
        while tmp < len(pr):
            counter = 0
            ans = ""
            for i in range(tmp, len(pr)):
                if counter > 1000:
                    flag = 1
                    break
                ans += str(tmp + 1) + ". " + pr[i][gname] + " - " + str(pr[i][glen]) + " см." + " \n"
                counter = len(ans)
                tmp += 1
            if ans != "":
                await ctx.send(f'{ans}')
        else:
            break


@bot.slash_command(name="топ", guild_ids=None, description = "выводит топ 10 писек сервера")
async def топ(ctx):
    if (await nsfw_check(ctx)):
        return
    string = ctx.guild.id  # str(ctx.message.guild.id)
    #string = str(ctx.message.guild.id)
    cursor.execute("SELECT * FROM basechel WHERE peerid=?", (int(string),))
    chel = cursor.fetchall()
    pr = sorted(chel, key=lambda tmp: -int(tmp[glen]))
    ans = ""
    for i in range(min(10, len(pr))):
        ans += str(i + 1) + ". " + pr[i][gname] + " - " + str(pr[i][glen]) + " см." + " \n"
    await ctx.respond(f'{ans}')


@bot.slash_command(name="ролл", guild_ids=None, description = "позволяет пойти на мид (случайное число 0-100)")
async def ролл(ctx):
    author = ctx.author  # ctx.message.author
    #author = ctx.message.author
    arr = ['0 0 1', '0 0 2', '0 0 3', '0 0 4', '0 0 5', '0 0 6', '0 0 7', '0 0 8', '0 0 9', '0 1 0', '0 1 1', '0 1 2',
           '0 1 3', '0 1 4', '0 1 5', '0 1 6', '0 1 7', '0 1 8', '0 1 9', '0 2 0', '0 2 1', '0 2 2', '0 2 3', '0 2 4',
           '0 2 5', '0 2 6', '0 2 7', '0 2 8', '0 2 9', '0 3 0', '0 3 1', '0 3 2', '0 3 3', '0 3 4', '0 3 5', '0 3 6',
           '0 3 7', '0 3 8', '0 3 9', '0 4 0', '0 4 1', '0 4 2', '0 4 3', '0 4 4', '0 4 5', '0 4 6', '0 4 7', '0 4 8',
           '0 4 9', '0 5 0', '0 5 1', '0 5 2', '0 5 3', '0 5 4', '0 5 5', '0 5 6', '0 5 7', '0 5 8', '0 5 9', '0 6 0',
           '0 6 1', '0 6 2', '0 6 3', '0 6 4', '0 6 5', '0 6 6', '0 6 7', '0 6 8', '0 6 9', '0 7 0', '0 7 1', '0 7 2',
           '0 7 3', '0 7 4', '0 7 5', '0 7 6', '0 7 7', '0 7 8', '0 7 9', '0 8 0', '0 8 1', '0 8 2', '0 8 3', '0 8 4',
           '0 8 5', '0 8 6', '0 8 7', '0 8 8', '0 8 9', '0 9 0', '0 9 1', '0 9 2', '0 9 3', '0 9 4', '0 9 5', '0 9 6',
           '0 9 7', '0 9 8', '0 9 9', '1 0 0']
    chislo = arr[random.randint(0, 99)]
    await ctx.respond(f'{author.mention},  получает случайное число(1-100):  {chislo}')


@bot.slash_command(name="чат", guild_ids=None, description = "выводит суммарную длину вашего сервера")
async def чат(ctx):
    if (await nsfw_check(ctx)):
        return
    string = ctx.guild.id  # str(ctx.message.guild.id)
    #string = str(ctx.message.guild.id)
    cursor.execute("SELECT * FROM basechel WHERE peerid=?", (int(string),))
    chel = cursor.fetchall()
    summ = 0
    for i in chel:
        summ += int(i[glen])
    await ctx.respond(f'Довжина писюна вашого сервера {str(summ)} см.')


@bot.slash_command(name="мой_писюн", guild_ids=None, description = "выводит вашу личную длину")
async def мой_писюн(ctx):
    if (await nsfw_check(ctx)):
        return
    string = ctx.guild.id  # str(ctx.message.guild.id)
    id = ctx.author.id  # str(ctx.message.author.id)
    author = ctx.author  # ctx.message.author
    cursor.execute("SELECT * FROM basechel WHERE peerid=? and id=?", (int(string), int(id)))
    chel = cursor.fetchone()
    if chel == None:
        await ctx.respond(f'{author.mention}, Пробач, брате, але в тебе ще немає писюна')
    else:
        await ctx.respond(f'{author.mention}, довжина твого писюна {str(chel[glen])} см.')

@bot.slash_command(name="кострация", guild_ids=None, description = "сбрасывает до нуля всё наращенное (и удаляет вас из нащих баз!)", nsfw = 1)
async def remove_cock(ctx):
    if (await nsfw_check(ctx)):
        return
    cursor = connection.cursor()
    string = ctx.guild.id  # str(ctx.message.guild.id)
    id = ctx.author.id  # str(ctx.message.author.id)
    author = ctx.author  # ctx.message.author
    cursor.execute("SELECT * FROM basechel WHERE peerid=? and id=?", (int(string), int(id)))
    chel = cursor.fetchone()
    if chel == None:
        await ctx.respond(f'Пробач, {author.mention}, але в тебе ще немає писюна')
    else:
        cursor.execute("DELETE FROM basechel WHERE peerid=? and id=?", (int(string), int(id)))
        await ctx.respond(f'{author.mention}, вітаю, ти відрізав собі писюн. Назавжди!')
    connection.commit()


def top_runner():
    print(1499)
    bot.loop.create_task(del_posts())
    bot.loop.create_task(top_chel())
    bot.loop.create_task(top_print())
    #print(141010)
    while True:
        if time.ctime(time.time()).split()[3].split(":")[0] == "12" and time.ctime(time.time()).split()[3].split(":")[
            1] == "00":
            bot.loop.create_task(del_posts())
            bot.loop.create_task(top_chel())
            bot.loop.create_task(top_print())
            time.sleep(60)
        time.sleep(30)

@bot.event
async def del_posts():
    await bot.wait_until_ready()
    print("deleting")
    chanel = bot.get_channel(815230126903656468)
    messages = await chanel.history().flatten()
    for i in messages:
        await i.delete()
        #await asyncio.sleep(1.2)
    print("deleted")



@bot.event
async def top_chel():
    # await bot.start(d_token)
    await bot.wait_until_ready()
    print(1488)
    cursor.execute("SELECT * FROM basechel ORDER BY len DESC")
    chel = cursor.fetchall()
    # print(chel)
    ans = []
    for i in chel:
        besed_id = i[gpeerid]
        print(besed_id)
        if bot.get_guild(int(besed_id)) != None:
            name = bot.get_guild(int(besed_id)).name
        else:
            name  = " - "
        tmp = [i, name]
        # print(tmp)
        if tmp[0][gid] in [i[0][gid] for i in ans]:
            print("AAAAAAAAAA")
            print([i[0][gid] for i in ans])
            print("BBBBBBBBBBBB")
            num = [i[0][gid] for i in ans].index(tmp[0][gid])
            if ans[num][0][glen] < tmp[0][glen]:
                ans[num] = tmp
        else:
            ans.append(tmp)

        if len(ans) == 11:
            break
    # print(ans)
    s = "Лучшие челы сегодня:" + "\n" + "\n"
    for i in range(len(ans)):
        j = ans[i][0]
        s += str(str(i + 1) + ". " + j[gname] + " - " + str(j[glen]) + " см." + " (" + ans[i][1] + ")" + '\n')
    # vk.method("messages.send",
    #         {"peer_id": "310573776", "message": s,
    #         "random_id": random.randint(1, 2147483647)})
    # vk.method("messages.send",
    #         {"peer_id": "231688699", "message": s,
    #         "random_id": random.randint(1, 2147483647)})
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!del_post("Chels_ID.txt")
    s += '\n' + '\n' + "-----------------------------------------------"
    channel = bot.get_channel(815230126903656468)
    await channel.send(s)
    # f = open('d_Chels_ID.txt', 'w')
    # f.write(str(ID))
    # f.close()

@bot.event
async def top_print():
    await bot.wait_until_ready()
    cursor.execute("SELECT * FROM basechel")
    chels = cursor.fetchall()
    tops = {}
    for chel in chels:
        peerid = chel[gpeerid]
        ln = chel[glen]
        nowlen = tops.get(peerid)
        if nowlen == None:
            tops.update({peerid: ln})
        else:
            tops.update({peerid: nowlen + ln})
    ans = [[i, j] for i, j in sorted(tops.items(), key=lambda item: -item[1])]
    tmp = []
    #print(ans)
    for i in range(len(ans)):
        #print(len(tmp), tmp)
        # print(tmp[i])
        peerid = ans[i][0]
        if bot.get_guild(int(peerid)) != None:
            name = bot.get_guild(int(peerid)).name
        else:
            name = " - "
        tmp.append([ans[i][1], name])
        if len(tmp) == 9:
            break
    tmpe = "Лучшие чаты сегодня:" + "\n" + "\n"
    # print(ans)

    for i in range(len(tmp)):
        tmpe += str(i + 1) + ". " + str(tmp[i][-1]) + ", довжина писюна вашого чату - " + str(tmp[i][0]) + " см." + "\n"
    channel = bot.get_channel(815230126903656468)
    await channel.send(tmpe)


time.sleep(2)
# asyncio.run(top_chel())
# bot.loop.create_task(top_chel())
#threading.Thread(target=top_runner).start()
#tmp = looper
t = threading.Thread(target = top_runner)
t.setDaemon(True)
t.start()

print("Started")
bot.run(d_token)
