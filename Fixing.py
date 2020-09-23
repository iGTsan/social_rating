import random, requests, time, vk_api, os, json, threading, sqlite3, discord
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from discord.ext import commands
from discord.ext import slash

d_token = "ODE1MjAwMTE1NDgwMTk5MTY4.YDo8RQ.wUMiIEt9V6zyeIG--DGh-VVvNLk"


from discord_slash import SlashCommand # Importing the newly installed library.
client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

guild_ids = [782496187194015761]  # Put your server ID in this array.


@slash.slash(name="test", guild_ids=guild_ids)
async def _test(ctx):
    await ctx.send("test")


slash = SlashCommand(client, sync_commands=True)
client.run("your_bot_token_here")