import discord
import os

import time
import discord.ext
import json
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure, check
import server_code.FirebaseAPI.firebase_queue as fb
from flask import Flask
from threading import Thread
from server_code.firebase_lock import *

# # # # # # # # # # # # # # # # # # # # # #
# Discord Bot async requests for commands #
# # # # # # # # # # # # # # # # # # # # # #
client = discord.Client()
bot = commands.Bot(command_prefix='!')

print("Initializing")

@bot.event
async def on_ready():
	print("Bot started!")  

@tasks.loop(seconds = 1) # repeat after every 10 seconds
async def bgCheck():
   	print("Hello")

#Testing Command
@bot.command(pass_context=True)
async def test(message):
	if message.author == bot.user:
		return
	if message.channel.category.id != 908207459074703410:
		return
	
	originChannel = bot.get_channel(message.channel.id)
	embed = discord.Embed(color=0x344FF5)
	channelName = message.channel.name
	class_name = channelName.lower().replace("-", "")[1:]
	print(message.channel.category.text_channels)

	try:
		fireBaseLock.acquire()
		preQueue = fb.access_course(class_name)
		fireBaseLock.release()
	except:
		fireBaseLock.release()
		return

	if preQueue != 'open':
		return

	print(preQueue)
	# Role Stuff
	#print(message.guild.roles)
	#role = discord.utils.get(message.guild.roles, name="Test Role")
	#user = message.author
	#await user.add_roles(user, role)
	

	#print(message.channel.category.id)

#Reaction gives role.
@client.event
async def on_reaction_add(reaction, user):
		if message.channel.category.id != 908207459074703410:
			return
		if reaction.emoji == "🏃":
			Role = discord.utils.get(user.server.roles, name="YOUR_ROLE_NAME_HERE")
			await client.add_roles(user, Role)


# Join Queue
@bot.command()
async def join(message):
	if message.author == bot.user:
		return
	if message.channel.category.id != 908207459074703410:
		return
	
	originChannel = bot.get_channel(message.channel.id)
	embed = discord.Embed(color=0x344FF5)
	channelName = message.channel.name
	class_name = channelName.lower().replace("-", "")[1:]

	try:
		fireBaseLock.acquire()
		preQueue = fb.access_queue(class_name)
		fireBaseLock.release()
	except:
		fireBaseLock.release()
		return

	inQueue = False
	for i in preQueue[0]:
			if i['name'] == str(message.author):
				inQueue = True

	if inQueue:
		embed.add_field(name="Joining Office Hour Queue", value="❌ Error: You are already in the queue.")
		await originChannel.send(embed=embed)
		return

	preLength = preQueue[1]

	try:
		fireBaseLock.acquire()
		fb.enqueue_student(class_name, "", str(message.author))
		postLength = fb.access_queue(class_name)[1]
		fireBaseLock.release()
	except: 
		fireBaseLock.release()

	if preLength < postLength:
		embed.add_field(name="Joining Office Hour Queue", value="You have joined the queue.")
		await originChannel.send(embed=embed)
	else:
		embed.add_field(name="Joining Office Hour Queue", value="❌ Error: You have failed to join the queue.")
		await originChannel.send(embed=embed)

# Dequeue a student.
@bot.command()
async def dequeue(message):
	if message.author == bot.user:
		return
	if message.channel.category.id != 908207459074703410:
		return
	
	originChannel = bot.get_channel(message.channel.id)
	embed = discord.Embed(color=0x344FF5)
	channelName = message.channel.name
	class_name = channelName.lower().replace("-", "")[1:]
	
	try:
		fireBaseLock.acquire()
		ls = fb.access_queue(class_name)
		lengthOfQueue = ls[1]
		fireBaseLock.release()
	except:
		fireBaseLock.release()
		return

	if lengthOfQueue > 0:
		try:
			fireBaseLock.acquire()		
			reply = fb.dequeue_student(class_name)
			fireBaseLock.release()
		except:
			fireBaseLock.release()
		embed.add_field(name="Dequeued Student", value=reply['name'])
		await originChannel.send(embed=embed)
	else: 
		embed.add_field(name="Unable to Dequeue", value='Error: The queue is already empty.')
		await originChannel.send(embed=embed)



@bot.command()
async def view(message):
	if message.author == bot.user:
		return
	if message.channel.category.id != 908207459074703410:
		return
	
	originChannel = bot.get_channel(message.channel.id)
	embed = discord.Embed(color=0x344FF5)
	channelName = message.channel.name
	class_name = channelName.lower().replace("-", "")[1:]

	try:
		fireBaseLock.acquire()
		ls = fb.access_queue(class_name)
		fireBaseLock.release()
	except:
		fireBaseLock.release()
		return

	lengthOfQueue = ls[1]
	queueList = ls[0]
	formattedQueueList = ""

	queueCount = 0
	if lengthOfQueue > 0:
		for i in queueList:
			queueCount += 1
			formattedQueueList += str(queueCount) + ". " +str((i['name'] + "\n"))
		msgTitle = "Current Queue for " + str(class_name)
		embed=discord.Embed(title=msgTitle)
		embed.add_field(name="Current Queue", value=formattedQueueList)
		embed.add_field(name="Length: ", value=str(lengthOfQueue))
		await originChannel.send(embed=embed)
	else:
		embed.add_field(name="Current Queue", value="Noone is in the queue.")
		await originChannel.send(embed=embed)
