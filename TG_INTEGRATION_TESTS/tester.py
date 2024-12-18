import time
from telethon import TelegramClient, sync

RUN = open("RUNProdigy.txt", "r")
RUN_arr = RUN.readlines()
api_id = int(RUN_arr[0][:-1])
api_hash = RUN_arr[1]


client = TelegramClient('vitaly', api_id, api_hash)
client.start()


async def main():
    while True:
        me = 'vit_72'
        bot_name = "@social_rating_dev_bot"
        await client.send_message(bot_name, "/соціальный_рейтинг")
        time.sleep(1)
        x = await client.get_messages(bot_name, limit=1)
        if f'{me}, Вітаю в грі соціальный рейтинг, ти зіграв в перший раз і зараз твій соціальный рейтинг має довжину' in \
                x[0].message:
            print("passed1")
        else:
            await client.send_message(-4508773309, "Бот упал - НУЖНО ЧИНИТЬ!(@ne_fakel @GT_san @vit_72)")
        await client.send_message(bot_name, "/топ")
        time.sleep(1)
        x = await client.get_messages(bot_name, limit=1)
        if f'1. {me} -' in x[0].message:
            print("passed2")
        else:
            await client.send_message(-4508773309, "Бот упал - НУЖНО ЧИНИТЬ!(@ne_fakel @GT_san @vit_72)")
        await client.send_message("@social_rating_dev_bot", "/маргинализация")
        time.sleep(1)
        x = await client.get_messages("@social_rating_dev_bot", limit=1)
        if x[0].message == f'{me}, вітаю, ти відрізав собі соціальный рейтинг. Назавжди!':
            print("passed3")
        else:
            await client.send_message(-4508773309, "Бот упал - НУЖНО ЧИНИТЬ!(@ne_fakel @GT_san @vit_72)")
        time.sleep(100)


with client:
    client.loop.run_until_complete(main())
