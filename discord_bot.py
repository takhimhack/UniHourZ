import discord
import os
import time
import discord.ext
import json
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure, check

import server_code.FirebaseAPI.firebase_queue as fb

client = discord.Client()

bot = commands.Bot(command_prefix='!')
course = "cse 354"
OHchannel = 907808237104017499

@client.event
async def on_ready():
	print("bot started!")  

#Async waiting for command messages
@bot.command()
async def joinqueue(message): 
	if message.author == bot.user:
			return
	preQueue = fb.access_queue(course)

	inQueue = False
	for i in preQueue[0]:
			if i['name'] == str(message.author):
				inQueue = True

	if inQueue:
		embed = discord.Embed()
		embed.add_field(name="Joining Office Hour Queue",
										value="Error: You are already in the queue.")
		OHQueueChannel = bot.get_channel(OHchannel)
		msg = await OHQueueChannel.send(embed=embed)
		await msg.add_reaction("❌")
	else:
		preLength = preQueue[1]
		fb.enqueue_student(course, "", str(message.author))
		postLength = fb.access_queue(course)[1]

		if preLength < postLength:
			embed = discord.Embed()
			embed.add_field(name="Joining Office Hour Queue",
											value="You have joined the queue.")
			OHQueueChannel = bot.get_channel(OHchannel)
			msg = await OHQueueChannel.send(embed=embed)
			
			await msg.add_reaction("✅")
		else:
			embed = discord.Embed()
			embed.add_field(name="Joining Office Hour Queue",
											value="Error: You have failed to join the queue.")
			OHQueueChannel = bot.get_channel(OHchannel)
			msg = await OHQueueChannel.send(embed=embed)
			await msg.add_reaction("❌")


@bot.command()
async def dequeue(message):
	if message.author == bot.user:
			return

	ls = fb.access_queue(course)
	lengthOfQueue = ls[1]

	if lengthOfQueue > 0:		
		reply = fb.dequeue_student(course)
		embed = discord.Embed()
		embed.add_field(name="Dequeued Student",
										value=reply['name'])
		OHQueueChannel = bot.get_channel(OHchannel)
		msg = await OHQueueChannel.send(embed=embed)
	else: 
		embed = discord.Embed()
		embed.add_field(name="Unable to Dequeue",
		value='The queue is empty.')
		OHQueueChannel = bot.get_channel(OHchannel)
		msg = await OHQueueChannel.send(embed=embed)


@bot.command()
async def viewqueue(message):
	if message.author == bot.user:
			return

	ls = fb.access_queue(course)
	lengthOfQueue = ls[1]
	queueList = ls[0]
	formattedQueueList = ""

	queueCount = 0
	if lengthOfQueue > 0:
		for i in queueList:
			queueCount += 1
			formattedQueueList += str(queueCount) + ". " +str((i['name'] + "\n"))
		embed = discord.Embed()
		embed.add_field(name="Current Queue", value=formattedQueueList)
		embed.add_field(name="Length: ", value=str(lengthOfQueue))
		OHQueueChannel = bot.get_channel(OHchannel)
		msg = await OHQueueChannel.send(embed=embed)
	else:
		embed = discord.Embed()
		embed.add_field(name="Current Queue", value="No Queue")
		OHQueueChannel = bot.get_channel(OHchannel)
		msg = await OHQueueChannel.send(embed=embed)	



bot.run(os.getenv("TOKEN"))