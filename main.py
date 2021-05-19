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
logid = jso["logid"]
logimg = jso["logimg"]

client = commands.Bot(command_prefix="", intents=discord.Intents.all())

@client.event
async def on_ready(): print("Online.")
	
@client.event
async def on_message_edit(before, after):
	if before.author.id != logid: return

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
				f.write(f"----------\n\n\nEvent: Message edited \nAuthor: {before.author},\nAuthor ID: {before.author.id}\nGuild: {before.guild}\nChannel: {before.channel}\nMessage ID: {before.id}\nTime: {time}\n\nBefore: {contentbefore}\nAfter: {contentafter}\n\n\n----------")

	except Exception as e:
		print(f"[ERROR] {e}")

	else:
		print("[DEBUG] Message edited.")

@client.event
async def on_message(message):
	if message.author.id != logid: return
	
	try:
		time = datetime.now().strftime("%H:%M:%S") + " - " + datetime.now().strftime("%d/%m/%Y")
		content = message.content

		if logimg:
			mid = -1
			firstTry = False

			if message.attachments:
				for a in message.attachments:
					images = os.path.join(os.path.dirname(__file__), "images")
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
			f.write(f"----------\n\n\nEvent: Message sent \nAuthor: {message.author},\nAuthor ID: {message.author.id}\nGuild: {message.guild}\nChannel: {message.channel}\nMessage ID: {message.id}\nTime: {time}\n\nContent: {content}\n\n\n----------")

	except Exception as e:
		print(f"[ERROR] {e}")

	else:
		print("[DEBUG] Message sent.")



client.run(token)