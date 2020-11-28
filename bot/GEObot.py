#!/usr/bin/env python
import json
import discord
from discord.ext import commands
from datetime import datetime

#https://discord.com/api/oauth2/authorize?client_id=778208288457490432&permissions=0&scope=bot

with open('tokens.json') as json_file:
    token = json.load(json_file)
    
bot = commands.Bot(command_prefix='!')
@bot.event
async def on_ready():
    activity = discord.Activity(name='!help | !whitelist | !squadtime', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)
    print("online")

initial_extensions = ['cogs.whitelist',
                     ]
for extension in initial_extensions:
        bot.load_extension(extension)



bot.run(token["discord"])