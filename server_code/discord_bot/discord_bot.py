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

client = discord.Client()
bot = commands.Bot(command_prefix='!')
ohCategoryID = 911003821017272421

print("Initializing")

@bot.event
async def on_ready():
	print("Bot started!")  


#Testing Command
@bot.command(pass_context=True)
async def test(message):
	if message.author == bot.user:
		return
	if message.channel.category.id != ohCategoryID:
		return
	
	originChannel = bot.get_channel(message.channel.id)
	embed = discord.Embed(color=0x344FF5)
	class_name = originChannel.name.lower().replace("-", "")
	
	try:
		fireBaseLock.acquire()
		courseStatus = fb.leave_queue(class_name, message.author)
		fireBaseLock.release()
	except:
		fireBaseLock.release()
		return
	# Role Stuff
	#print(message.guild.roles)
	#role = discord.utils.get(message.guild.roles, name="Test Role")
	#user = message.author


# # # # # # # # # # # # # # # # # # # # # #
# Discord Bot async requests for commands #
# # # # # # # # # # # # # # # # # # # # # #
# Join Queue Command
@bot.command()
async def join(message):
	if message.author == bot.user:
		return
	if message.channel.category.id != ohCategoryID:
		return
	
	originChannel = bot.get_channel(message.channel.id)
	embed = discord.Embed(color=0x344FF5)
	class_name = originChannel.name.lower().replace("-", "")

	#Check courses status and if it is open.
	try:
		fireBaseLock.acquire()
		courseStatus = fb.access_course(class_name)
		fireBaseLock.release()
	except:
		fireBaseLock.release()
		return

	status = str(courseStatus[0])
	eta = str(courseStatus[1])
	preLength = str(courseStatus[2])

	if status == "closed":
		embed.add_field(name="Office Hour Queue Closed", value="❌ Error: This course's office hours are currently closed.")
		await originChannel.send(embed=embed)
		return

	#Accessing the queue to check if user is already in queue
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

	#Queue student
	try:
		fireBaseLock.acquire()
		fb.enqueue_student(class_name, "", str(message.author))
		fireBaseLock.release()
		embed.add_field(name="Joining Office Hour Queue", value="You have joined the queue.")
		await originChannel.send(embed=embed)
	except: 
		fireBaseLock.release()
		embed.add_field(name="Joining Office Hour Queue", value="❌ Error: You have failed to join the queue.")
		await originChannel.send(embed=embed)

# Leave Queue Command
@bot.command()
async def leave(message):
	if message.author == bot.user:
		return
	if message.channel.category.id != ohCategoryID:
		return
	
	originChannel = bot.get_channel(message.channel.id)
	embed = discord.Embed(color=0x344FF5)
	class_name = originChannel.name.lower().replace("-", "")

	#Check courses status and if it is open.
	try:
		fireBaseLock.acquire()
		courseStatus = fb.access_course(class_name)
		fireBaseLock.release()
	except:
		fireBaseLock.release()
		return

	status = str(courseStatus[0])
	eta = str(courseStatus[1])
	preLength = str(courseStatus[2])

	if status == "closed":
		embed.add_field(name="Office Hour Queue Closed", value="❌ Error: This course's office hours are currently closed.")
		await originChannel.send(embed=embed)
		return

	#Accessing the queue to check if user is already in queue
	try:
		fireBaseLock.acquire()
		fb.leave_queue(class_name, message.author)
		fireBaseLock.release()
		embed.add_field(name="Left Office Hour Queue", value="You have left the queue.")
		await originChannel.send(embed=embed)
	except:
		fireBaseLock.release()
		embed.add_field(name="Leaving Office Hour Queue", value="❌ Error: You have failed to leave the queue.")
		await originChannel.send(embed=embed)
		return


#View Command
@bot.command()
async def view(message):
	if message.author == bot.user:
		return
	if message.channel.category.id != ohCategoryID:
		return
	
	originChannel = bot.get_channel(message.channel.id)
	embed = discord.Embed(color=0x344FF5)
	class_name = originChannel.name.lower().replace("-", "")

	#Check courses status and if it is open.
	try:
		fireBaseLock.acquire()
		courseStatus = fb.access_course(class_name)
		fireBaseLock.release()
	except:
		fireBaseLock.release()
		return

	status = str(courseStatus[0])
	eta = str(courseStatus[1])

	if status == "closed":
		embed.add_field(name="Office Hour Queue Closed", value="❌ Error: This course's office hours are currently closed.")
		await originChannel.send(embed=embed)
		return

	#Access the queue from firebase
	try:
		fireBaseLock.acquire()
		queueData = fb.access_queue(class_name)
		fireBaseLock.release()
	except:
		fireBaseLock.release()
		return

	#Format and send message of the queue
	lengthOfQueue = queueData[1]
	queueList = queueData[0]
	formattedQueueList = ""
	queueCount = 0

	if lengthOfQueue == 0:
		embed.add_field(name="Current Queue", value="Noone is in the queue.")
		await originChannel.send(embed=embed)
		return

	for i in queueList:
		queueCount += 1
		formattedQueueList += str(queueCount) + ". " +str((i['name'] + "\n"))
	msgTitle = "Current Queue for " + str(class_name)
	etaMin = eta + " minutes"
	embed=discord.Embed(title=msgTitle)
	embed.add_field(name="Current Queue", value=formattedQueueList)
	embed.add_field(name="Length: ", value=str(lengthOfQueue))
	embed.add_field(name="Time Per Student: ", value=etaMin)
	await originChannel.send(embed=embed)