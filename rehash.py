import random, requests, time, vk_api, os, json, threading, sqlite3, discord
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from discord.ext import commands
import asyncio

d_token = "ODE1MjAwMTE1NDgwMTk5MTY4.YDo8RQ.wUMiIEt9V6zyeIG--DGh-VVvNLk"
bot = commands.Bot(command_prefix = "/")

connection = sqlite3.connect('d_base505.db')
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS basechel (globalid INT PRIMARY KEY, peerid INT, id INT, len INT, time INT, name TEXT, delta INT)")
connection.commit()
client = discord.Client()

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
    id = ctx.message.author.id
    tmp = {"id": "", "len": "", "time": "", "name": ""}
    tmp["id"], tmp["len"], tmp["time"] = id, str(random.randint(1, 10)), str(current_day())
    name = ctx.message.author.name
    tmp["name"] = str(name)
    if tmp["name"][-12:] == " | ВКонтакте":
        tmp["name"] = tmp["name"][:-12]
    return tmp

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




@bot.command()
async def писюн(ctx):
    string = str(ctx.message.guild.id)
    id = str(ctx.message.author.id)
    author = ctx.message.author
    day = current_day()
    cursor.execute("SELECT * FROM basechel WHERE peerid=? and id=?", (int(string), int(id)))
    chel = cursor.fetchone()
    if chel != None:
        chel = list(chel)
        if day - (int(chel[gtime])) < 1:
            await ctx.send(f'{author.mention}, ти сьогодні вже грав(')
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
            await ctx.send(f'{author.mention}, у тебе відвалилася піська(')
        else:
            fin = fin + ans
            if ans > 0:
                await ctx.send(f'{author.mention}, твій пісюн виріс на {str(ans)}см. Тепер його довжина {str(fin)} см.')
            else:
                await ctx.send(f'{author.mention}, твій пісюн зменшився на {str(-ans)}см. Тепер його довжина {str(fin)} см.')
        chel[glen] = int(fin)
        chel[gtime] = int(current_day())
        cursor.execute("REPLACE INTO basechel VALUES(?, ?, ?, ?, ?, ?, ?);", chel)
        connection.commit()

    if chel == None:
        new_chel = gen_new(ctx)

        await ctx.send(f'{author.mention}, Вітаю в грі писюн, ти зіграв в перший раз і зараз твій пісюн має довжину {new_chel["len"]} см.')


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

@bot.command()
async def топ_все(ctx):
    string = str(ctx.message.guild.id)
    cursor.execute("SELECT * FROM basechel WHERE peerid=?", (int(string),))
    chel = cursor.fetchall()
    pr = sorted(chel, key=lambda tmp: -int(tmp[glen]))
    ans = ""
    counter = 0
    tmp = 0
    for i in range(len(pr)):
        if counter > 4000:
            break
        ans += pr[i][gname] + " - " + str(pr[i][glen]) + " см." + " \n"
        tmp += 1
        counter = len(ans)
    await ctx.send(f'{ans}')
    if counter >= 4000:
        while tmp <= len(pr):
            counter = 0
            ans = ""
            for i in range(tmp, len(pr)):
                ans += pr[i][gname] + " - " + str(pr[i][glen]) + " см." + " \n"
                counter = len(ans)
                tmp += 1
            await ctx.send(f'{ans}')


@bot.command()
async def топ(ctx):
    string = str(ctx.message.guild.id)
    cursor.execute("SELECT * FROM basechel WHERE peerid=?", (int(string),))
    chel = cursor.fetchall()
    pr = sorted(chel, key=lambda tmp: -int(tmp[glen]))
    ans = ""
    for i in range(min(10, len(pr))):
        ans += pr[i][gname] + " - " + str(pr[i][glen]) + " см." + " \n"
    await ctx.send(f'{ans}')


@bot.command()
async def ролл(ctx):
    author = ctx.message.author
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
    await ctx.send(f'{author.mention},  получает случайное число(1-100):  {chislo}')


@bot.command()
async def чат(ctx):
    string = str(ctx.message.guild.id)
    cursor.execute("SELECT * FROM basechel WHERE peerid=?", (int(string),))
    chel = cursor.fetchall()
    summ = 0
    for i in chel:
        summ += int(i[glen])
    await ctx.send(f'Довжина писюна вашого чату {str(summ)} см.')


@bot.command()
async def мой_писюн(ctx):
    print(ctx.message)
    print(ctx.send(1488))
    string = str(ctx.message.guild.id)
    id = str(ctx.message.author.id)
    author = ctx.message.author
    cursor.execute("SELECT * FROM basechel WHERE peerid=? and id=?", (int(string), int(id)))
    chel = cursor.fetchone()
    await ctx.send(f'{author.mention}, довжина твого писюна {str(chel[glen])} см.')

def del_post(name):
    f = open(name, 'r')
    tmp = f.readlines()
    tmp = tmp[0].split()
    tmp = tmp[1][:-1]
    f.close()
    vk_admin.method("wall.delete",
                    {"owner_id": "-" + RUN_arr[1], "post_id": tmp})

async def top_chel():
    print(1488)
    cursor.execute("SELECT * FROM basechel ORDER BY len DESC")
    chel = cursor.fetchall()
    #print(chel)
    ans = []
    for i in chel:
        besed_id = i[gpeerid]
        print(besed_id)
        name = bot.get_guild(int(besed_id)).name
        tmp = [i, name]
        #print(tmp)
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
    #print(ans)
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
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!del_post("Chels_ID.txt")
    channel = bot.get_channel(815230126903656468)
    await channel.send("s")
    return "GG"
    #f = open('d_Chels_ID.txt', 'w')
    #f.write(str(ID))
    #f.close()


asyncio.run(top_chel())
print("Started")
bot.run(d_token)