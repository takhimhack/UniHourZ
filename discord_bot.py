import discord
import os
import time
import discord.ext
import json
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check

from server_code.FirebaseAPI.firebaseAPI import *
import server_code.FirebaseAPI.firebase_queue as fb
from server_code.FirebaseAPI.queue_exceptions.queue_exceptions import *

bot = discord.Client()
bot = commands.Bot(command_prefix='!')

@bot.event()
async def on_ready():
    print("bot started!") #will print "bot online" in the console when the bot is online
    
@bot.command()
async def joinq(message):
	if message.author == bot.user:
		return
	
	embed = discord.Embed()
	embed.add_field(name="Joining Office Hour Queue", value="Your request to join the queue has been added.")

	msg = await message.channel.send(embed=embed)
	msg.add_reaction("✅")
	msg.add_reaction("❌")

bot.run(os.getenv("TOKEN")) #get your bot token and create a key named `TOKEN` to the secrets panel then paste your bot token as the value. 
#to keep your bot from shutting down use https://uptimerobot.com then create a https:// monitor and put the link to the website that appewars when you run this repl in the monitor and it will keep your bot alive by pinging the flask server
#enjoy!