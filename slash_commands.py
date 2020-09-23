import requests
import discord

d_token = "ODE1MjAwMTE1NDgwMTk5MTY4.YDo8RQ.wUMiIEt9V6zyeIG--DGh-VVvNLk"
url = "https://discord.com/api/v8/applications/815200115480199168/guilds/782496187194015761/commands"


json = {
    "name": "писюн",
    "description": "Змінює довжину вашого пісюна",
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": d_token
}


r = requests.post(url, headers=headers, json=json)