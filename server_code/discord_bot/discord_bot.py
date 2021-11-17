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
from firebase_lock import *

# # # # # # # # # # # # # # # # # # # # # #
# Discord Bot async requests for commands #
# # # # # # # # # # # # # # # # # # # # # #
client = discord.Client()
bot = commands.Bot(command_prefix='!')

print("Initializing")

@bot.event
async def on_ready():
	print("Bot started!")  

# Join Queue
@bot.command()
async def joinqueue(message, *, class_name:str = ""): 
	if message.author == bot.user:
			return

	originChannelID = message.channel.id
	originChannel = bot.get_channel(originChannelID)
	embed = discord.Embed(color=0x344FF5)
	class_name = class_name.lower().replace(" ", "")

	if len(class_name) == 0:
		embed.add_field(name="Failed Joining Class", value="❌ Error: Missing Class Name Parameter")
		await originChannel.send(embed=embed)	
		return
	
	try:
		fireBaseLock.acquire()
		preQueue = fb.access_queue(class_name)
		fireBaseLock.release()
	except:
		fireBaseLock.release()
		embed.add_field(name="Failed Joining Queue", value="❌ Error: Course Queue Does Not Exist")
		await originChannel.send(embed=embed)
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
async def dequeue(message, *, class_name:str = ""):
	if message.author == bot.user:
			return

	originChannelID = message.channel.id
	originChannel = bot.get_channel(originChannelID)
	embed = discord.Embed(color=0x344FF5)
	class_name = class_name.lower().replace(" ", "")

	if len(class_name) == 0:
		embed.add_field(name="Failed Creating Queue", value="❌ Error: Missing Class Name Parameter")
		await originChannel.send(embed=embed)
		return
	
	try:
		fireBaseLock.acquire()
		ls = fb.access_queue(class_name)
		lengthOfQueue = ls[1]
		fireBaseLock.release()
	except:
		fireBaseLock.release()
		embed.add_field(name="Failed Dequeuing Student", value="❌ Error: Course Queue Does Not Exist")
		await originChannel.send(embed=embed)	
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
async def viewqueue(message, *, class_name:str = ""):
	if message.author == bot.user:
			return
	
	originChannelID = message.channel.id
	originChannel = bot.get_channel(originChannelID)
	embed = discord.Embed(color=0x344FF5)
	class_name = class_name.lower().replace(" ", "")

	if len(class_name) == 0:
		embed.add_field(name="Failed Creating Queue", value="❌ Error: Missing Class Name Parameter")
		await originChannel.send(embed=embed)
		return


	try:
		fireBaseLock.acquire()
		ls = fb.access_queue(class_name)
		fireBaseLock.release()
	except:
		fireBaseLock.release()
		embed.add_field(name="Failed Viewing Queue", value="❌ Error: Course Queue Does Not Exist")
		await originChannel.send(embed=embed)	
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


@bot.command()
async def createqueue(message, *, class_name:str = ""): 
	if message.author == bot.user:
			return

	originChannelID = message.channel.id
	originChannel = bot.get_channel(originChannelID)
	embed = discord.Embed(color=0x344FF5)
	class_name = class_name.lower().replace(" ", "")

	if len(class_name) == 0:
		embed.add_field(name="Failed Creating Queue", value="❌ Error: Missing Class Name Parameter")
		await originChannel.send(embed=embed)
		return

	try:
		fireBaseLock.acquire()
		returnStat = fb.create_queue(class_name)
		fireBaseLock.release()
	except:
		fireBaseLock.release()
		embed.add_field(name="Failed Creating Queue", value="❌ Error: Queue Already Exists")
		await originChannel.send(embed=embed)
		return
	msgTitle = "Successfully Created Queue for " + str(class_name)
	embed=discord.Embed(title=msgTitle)
	embed.add_field(name="Current Queue:", value=returnStat)
	await originChannel.send(embed=embed)