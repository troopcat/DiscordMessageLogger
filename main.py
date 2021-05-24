import discord
from discord.ext import commands
import os
from datetime import datetime
import json


logfile = input("File to log: ")

if logfile.strip() == "":
	logfile = "log." + datetime.now().strftime("%d-%m-%Y") + ".txt"

logfile = os.path.join(os.path.join(os.path.dirname(__file__), "logs"), logfile)

with open("config.json", "r", encoding="utf8") as f:
	jso = json.load(f)

token = jso["token"]
logid = jso["logID"]

da = jso["download_attachments"]

client = commands.Bot(command_prefix="", intents=discord.Intents.all())

@client.event
async def on_ready():
	print("Logged In.")

@client.event
async def on_raw_message_delete(payload):
	try:
		if not payload or payload.cached_message.author.id != logid: return
		
	except AttributeError:
		return
	
	try: guildID = message.guild.id
	except AttributeError: guildID = None

	try:
		time = datetime.now().strftime("%H:%M:%S") + " - " + datetime.now().strftime("%d/%m/%Y")

		message = payload.cached_message
		content = message.content

		if message.attachments:
			for a in message.attachments:
				content += " {" + a.filename + "} "


		with open(logfile, "a+", encoding="utf8") as f:
				f.write(f"-\n\n\nEvent: Message deleted \nAuthor: {message.author}\nAuthor ID: {message.author.id}\nGuild: {message.guild}\nGuild ID: {guildID}\nChannel: {message.channel}\nChannel ID: {message.channel.id}\nMessage ID: {message.id}\nTime: {time}\n\nContent:\n{content}\n\n\n-")

	except Exception as e:
		print(f"{time} [ERROR] {e}")

	else:
		print(f"{time} [DEBUG] Message deleted.")

@client.event
async def on_message_edit(before, after):
	if before.author.id != logid: return
	
	try: guildID = before.guild.id
	except AttributeError: guildID = None
	
	try:
		time = datetime.now().strftime("%H:%M:%S") + " - " + datetime.now().strftime("%d/%m/%Y")

		contentafter = after.content
		contentbefore = before.content

		if after.attachments:
			for a in after.attachments:
				contentafter += " {" + a.filename + "} "

		if before.attachments:
			for a in after.attachments:
				contentbefore += " {" + a.filename + "} "

		with open(logfile, "a+", encoding="utf8") as f:
				f.write(f"-\n\n\nEvent: Message edited \nAuthor: {before.author}\nAuthor ID: {before.author.id}\nGuild: {before.guild}\nGuild ID: {guildID}\nChannel: {before.channel}\nChannel ID: {before.channel.id}\nMessage ID: {before.id}\nTime: {time}\n\nBefore:\n{contentbefore}\n\nAfter:\n{contentafter}\n\n\n-")

	except Exception as e:
		print(f"{time} [ERROR] {e}")

	else:
		print(f"{time} [DEBUG] Message edited.")

@client.event
async def on_message(message):
	if message.author.id != logid: return
	
	try:
		time = datetime.now().strftime("%H:%M:%S") + " - " + datetime.now().strftime("%d/%m/%Y")
		content = message.content
		
		try: guildID = message.guild.id
		except AttributeError: guildID = None
		
		if da:
			mid = -1
			firstTry = False

			if message.attachments:
				for a in message.attachments:
					images = os.path.join(os.path.dirname(__file__), "attachments")
					filename = os.path.join(images, a.filename)

					while True:
						if os.path.isfile(filename):

							mid += 1
							
							if firstTry:
								filename = os.path.join(images, a.filename.split(".")[0][:-1 * len(str(mid))] + str(mid) + "." + a.filename.split(".")[1])
							else:
								filename = os.path.join(images, a.filename.split(".")[0] + str(mid) + "." + a.filename.split(".")[1])

							firstTry = True
						else:
							break
					
					
					
					with open(filename, "wb") as f:
						await a.save(f)

					content += " {" + a.filename + "} "

		with open(logfile, "a+", encoding="utf8") as f:
			f.write(f"-\n\n\nEvent: Message sent \nAuthor: {message.author}\nAuthor ID: {message.author.id}\nGuild: {message.guild}\nGuild ID: {guildID}\nChannel: {message.channel}\nChannel ID: {message.channel.id}\nMessage ID: {message.id}\nTime: {time}\n\nContent:\n{content}\n\n\n-")

	except Exception as e:
		print(f"{time} [ERROR] {e}")

	else:
		print(f"{time} [DEBUG] Message sent.")



client.run(token)