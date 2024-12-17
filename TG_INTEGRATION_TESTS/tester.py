import time
RUN = open("RUNProdigy.txt", "r")
RUN_arr = RUN.readlines()
api_id = int(RUN_arr[0][:-1])
api_hash = RUN_arr[1]
from telethon import TelegramClient, sync
# from telethon.tl.functions.channels.delete_messages import DeleteMessagesRequest

# Вставляем api_id и api_hash
# api_id = 12345
# api_hash = '0123456789abcdef0123456789abcdef'

client = TelegramClient('vitaly', api_id, api_hash)
client.start()
async def main():
    while True:
        me = 'vit_72'
        bot_name = "@social_rating_dev_bot"
        await client.send_message(bot_name, "/соціальный_рейтинг")
        time.sleep(1)
        x = await client.get_messages(bot_name, limit=1)
        if f'{me}, Вітаю в грі соціальный рейтинг, ти зіграв в перший раз і зараз твій соціальный рейтинг має довжину' in x[0].message :
            print("passed1")
        else:
            await client.send_message(-4508773309, "Бот упал - НУЖНО ЧИНИТЬ!")
        await client.send_message(bot_name, "/топ")
        time.sleep(1)
        x = await client.get_messages(bot_name, limit=1)
        if f'1. {me} -' in x[0].message:
            print("passed2")
        else:
            await client.send_message(-4508773309, "Бот упал - НУЖНО ЧИНИТЬ!")
        await client.send_message("@social_rating_dev_bot", "/маргинализация")
        time.sleep(1)
        x = await client.get_messages("@social_rating_dev_bot", limit=1)
        if x[0].message == 'vit_72, вітаю, ти відрізав собі соціальный рейтинг. Назавжди!':
            print("passed3")
        else:
            await client.send_message(-4508773309, "Бот упал - НУЖНО ЧИНИТЬ!")
        time.sleep(100)



with client:
    client.loop.run_until_complete(main())
# participants = client.get_participants()
# print(participants)
# for dialog in client.iter_dialogs():
#     print(dialog.title, dialog.id)