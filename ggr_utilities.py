#import discord
import datetime
import math


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