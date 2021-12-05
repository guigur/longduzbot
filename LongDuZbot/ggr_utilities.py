#import discord
import datetime
import math
import requests

def pickDefImage(name):
	folder = "img/default/"
	if name[0] <= 'e':
		return folder + "red.png"
	elif name[0] >= 'f' and name[0] <= 'j':
		return folder + "green.png"
	elif name[0] >= 'k' and name[0] <= 'o':
		return folder + "grey.png"
	elif name[0] >= 'p' and name[0] <= 't':
		return folder + "yellow.png"
	return folder + "blue.png"

def userServerIcon(ctx, user = None):
	if user:
		userUrl = user.avatar_url_as(format='png')
	else:
		userUrl = ctx.author.avatar_url_as(format='png')
	
	try:
		userImg = requests.get(userUrl, stream=True).raw
	except requests.exceptions.RequestException as e:
		userImg = pickDefImage(ctx.author.name)

	guildUrl = ctx.guild.icon_url_as(format='png')
	try:
		guildImg = requests.get(guildUrl, stream=True).raw
	except requests.exceptions.RequestException as e:
		guildImg = pickDefImage(ctx.guild.name)

	return userImg, guildImg

def checkIfIdValid(id):
	if ((type(id) is int) and int(id) > 9999999999999999):
		return True
	print("Invalid ID")
	return False

def digitToEmoji(digit):
	if digit == 0:
		return "0️⃣"
	elif digit == 1:
		return "1️⃣"
	elif digit == 2:
		return "2️⃣"
	elif digit == 3:
		return "3️⃣"
	elif digit == 4:
		return "4️⃣"
	elif digit == 5:
		return "5️⃣"
	elif digit == 6:
		return "6️⃣"
	elif digit == 7:
		return "7️⃣"
	elif digit == 8:
		return "8️⃣"
	elif digit == 9:
		return "9️⃣"

def numbersToEmojis(number):
	decade = digitToEmoji(math.trunc( number / 10))
	dec = digitToEmoji(number % 10)
	return [decade, dec]

def pDT():
	now = datetime.datetime.now()
	return (now.strftime("%m/%d/%Y %H:%M:%S"))

def logger(ctx, string):
	if ctx:
		usr = ctx.message.author.name
	else:
		usr = "server"
	string = pDT() + " " + usr + "]"+ string
	print(string)
	#todo: add to file