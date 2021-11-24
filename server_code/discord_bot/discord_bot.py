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

print("Initializing")

@bot.event
async def on_ready():
	print("Bot started!")  


#Testing Command
@bot.command(pass_context=True)
async def test(message):
	if message.author == bot.user:
		return
	if str(message.channel.category) != "Office Hours": #Check if Category is correct
		return
	
	originChannel = bot.get_channel(message.channel.id)
	embed = discord.Embed(color=0x344FF5)
	class_name = originChannel.name.lower().replace("-", "")
	print(message.channel.category)

# # # # # # # # # # # # # # # # # # # # # #
# Discord Bot async requests for commands #
# # # # # # # # # # # # # # # # # # # # # #

# Join Queue Command  #
# # # # # # # # # # # #
@bot.command()
async def join(message):
	if message.author == bot.user:
		return
	if str(message.channel.category) != "Office Hours": #Check if Category is correct
		return
	
	#Reference Setup
	originChannel = bot.get_channel(message.channel.id)
	embed = discord.Embed(color=0x344FF5)
	class_name = originChannel.name.lower().replace("-", "")

	#Checks if user has permission/is registered, gives role if registered
	registeredRole = False
	for i in message.author.roles:
		if i.name == "Registered Student":
			registeredRole = True
	if not registeredRole:	
		#Get User info from firebase
		fbUser = str(message.author)
		fbUser = fbUser.replace("#", "_", 1)
		try:
			fireBaseLock.acquire()
			user_info = fb.access_user(fbUser)
			fireBaseLock.release()
		except:
			fireBaseLock.release()
			embed.add_field(name="Missing User Registration", value="❌ Error: You are not currently registered on the website.")
			await originChannel.send(embed=embed)
			return
		member = message.author
		role = discord.utils.get(member.guild.roles, name="Registered Student")
		await member.add_roles(role)

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

	#Get User info from firebase
	fbUser = str(message.author)
	fbUser = fbUser.replace("#", "_", 1)
	try:
		fireBaseLock.acquire()
		user_info = fb.access_user(fbUser)
		fireBaseLock.release()
	except:
		fireBaseLock.release()
		embed.add_field(name="Missing User Registration", value="❌ Error: You are not currently registered on the website.")
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
			if i['name'] == str(user_info):
				inQueue = True
	if inQueue:
		embed.add_field(name="Joining Office Hour Queue", value="❌ Error: You are already in the queue.")
		await originChannel.send(embed=embed)
		return

	#Queue student
	try:
		fireBaseLock.acquire()
		fb.enqueue_student(class_name, "", user_info)
		fireBaseLock.release()
		embed.add_field(name="Joining Office Hour Queue", value="You have joined the queue.")
		await originChannel.send(embed=embed)
	except: 
		fireBaseLock.release()
		embed.add_field(name="Joining Office Hour Queue", value="❌ Error: You have failed to join the queue.")
		await originChannel.send(embed=embed)



# Leave Queue Command #
# # # # # # # # # # # #
@bot.command()
async def leave(message):
	if message.author == bot.user:
		return
	if str(message.channel.category) != "Office Hours": #Check if Category is correct
		return
	
	#Reference Setup
	originChannel = bot.get_channel(message.channel.id)
	embed = discord.Embed(color=0x344FF5)
	class_name = originChannel.name.lower().replace("-", "")

	#Checks if user has permission/is registered, gives role if registered/is registered, gives role if registered
	registeredRole = False
	for i in message.author.roles:
		if i.name == "Registered Student":
			registeredRole = True
	if not registeredRole:	
		#Get User info from firebase
		fbUser = str(message.author)
		fbUser = fbUser.replace("#", "_", 1)
		try:
			fireBaseLock.acquire()
			user_info = fb.access_user(fbUser)
			fireBaseLock.release()
		except:
			fireBaseLock.release()
			embed.add_field(name="Missing User Registration", value="❌ Error: You are not currently registered on the website.")
			await originChannel.send(embed=embed)
			return
		member = message.author
		role = discord.utils.get(member.guild.roles, name="Registered Student")
		await member.add_roles(role)

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
	preQueue = courseStatus[3]

	if status == "closed":
		embed.add_field(name="Office Hour Queue Closed", value="❌ Error: This course's office hours are currently closed.")
		await originChannel.send(embed=embed)
		return

	fbUser = str(message.author)
	fbUser = fbUser.replace("#", "_", 1)
	try:
		fireBaseLock.acquire()
		user_info = fb.access_user(fbUser)
		fireBaseLock.release()
	except:
		fireBaseLock.release()
		embed.add_field(name="Missing User Registration", value="❌ Error: You are not currently registered on the website.")
		await originChannel.send(embed=embed)
		return
	inQueue = False
	for user in preQueue:
		if user['name'] == user_info:
			inQueue = True

	if not inQueue:
		print("user not in queue")
		embed.add_field(name="Office Hour Queue", value="❌ Error: You can't leave the queue, because you aren't in it.")
		await originChannel.send(embed=embed)
		return
		
	fbUser = str(message.author)
	fbUser = fbUser.replace("#", "_", 1)
	#Accessing the queue to check if user is already in queue
	try:
		fireBaseLock.acquire()
		user_info = fb.access_user(fbUser)
		test = fb.leave_queue(class_name, user_info)
		fireBaseLock.release()
		embed.add_field(name="Left Office Hour Queue", value="You have left the queue.")
		await originChannel.send(embed=embed)
	except:
		fireBaseLock.release()
		embed.add_field(name="Leaving Office Hour Queue", value="❌ Error: You have failed to leave the queue.")
		await originChannel.send(embed=embed)
		return


# View Command  #
# # # # # # # # #
@bot.command()
async def view(message):
	if message.author == bot.user:
		return
	if str(message.channel.category) != "Office Hours": #Check if Category is correct
		return
	
	#Reference Setup
	originChannel = bot.get_channel(message.channel.id)
	embed = discord.Embed(color=0x344FF5)
	class_name = originChannel.name.lower().replace("-", "")

	#Checks if user has permission/is registered, gives role if registered
	registeredRole = False
	for i in message.author.roles:
		if i.name == "Registered Student":
			registeredRole = True
	if not registeredRole:	
		#Get User info from firebase
		fbUser = str(message.author)
		fbUser = fbUser.replace("#", "_", 1)
		try:
			fireBaseLock.acquire()
			user_info = fb.access_user(fbUser)
			fireBaseLock.release()
		except:
			fireBaseLock.release()
			embed.add_field(name="Missing User Registration", value="❌ Error: You are not currently registered on the website.")
			await originChannel.send(embed=embed)
			return
		member = message.author
		role = discord.utils.get(member.guild.roles, name="Registered Student")
		await member.add_roles(role)

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