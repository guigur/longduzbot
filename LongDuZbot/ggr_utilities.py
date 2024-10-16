#import discord
import datetime
import math
import requests
import os
from termcolor import colored
from enum import Enum
from functools import wraps
from discord.ext import commands

#colors https://www.materialpalette.com/colors
ggr_red = 0xf44336
ggr_pink = 0xe91e63
ggr_purple = 0x9c27b0
ggr_deeppurple = 0x673ab7
ggr_indigo = 0x3f51b5
ggr_blue = 0x2196f3
ggr_lightblue = 0x03a9f4
ggr_cyan = 0x00bcd4
ggr_teal = 0x009688
ggr_green = 0x4caf50
ggr_lightgreen = 0x8bc34a
ggr_lime = 0xcddc39
ggr_yellow = 0xffeb3b
ggr_amber = 0xffc107
ggr_orange = 0xff9800
ggr_deeporange = 0xff5722
ggr_brown = 0x795548
ggr_grey = 0x9e9e9e
ggr_bluegrey = 0x607d8b


MasterRoleName = "Maître des Saloperies"
githubBaseUrl = "https://github.com/guigur/longduzbot/"
roleColor = ggr_yellow
roles_list = [{"name":"Maître des Saloperies", "meta": "master", "color": ggr_yellow}, 
			  {"name":"Jean-foutre", "meta": "worst", "color": ggr_purple}]

embedUtilitiesColor = ggr_deeppurple

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

def serverIcon(guild):
	guildUrl = guild.icon_url_as(format='png')
	try:
		guildImg = requests.get(guildUrl, stream=True).raw
	except requests.exceptions.RequestException as e:
		guildImg = pickDefImage(guild.name)

	return guildImg

def userIcon(user):
	userUrl = user.avatar_url_as(format='png')
	try:
		userImg = requests.get(userUrl, stream=True).raw
	except requests.exceptions.RequestException as e:
		userImg = pickDefImage(user.name)
	return userImg

def checkIfIdValid(id):
	if (isinstance(int(id), int) == True):
		if (int(id) > 9999999999999999):
			return True
		else:
			pass
	else:
		print("not instance")
	print("Invalid ID")
	return False

def treedotString(string, maxlen):
	stringret = (string[:maxlen-2] + '...') if len(string) > maxlen else string
	return stringret

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

class LogType(Enum):
	NORMAL = 0
	ERROR = 1
	SUCCESS = 2
	INFO = 3

	def color(self):
		if (self.value == 0):
			return (None)
		elif (self.value == 1):
			return ("red")
		elif (self.value == 2):
			return ("green")
		elif (self.value == 3):
			return ("yellow")

def logger(string, cog=None, ctx=None, logType=LogType.NORMAL):
	usr = colored("server", "cyan")
	if ctx:
		usr = colored(ctx.message.author.name, "yellow")
				
	classname = ""
	if cog:
		classname = ">" + colored(cog.__class__.__name__, "green") 
		
	string = pDT() + " " + usr + classname + "] "+ colored(string, logType.color())
	print(string)
	#todo: add to file

def check_admin():
	async def predicate(ctx):
        # return ctx.guild and ctx.guild.id == guild_id
		return ctx.author and ctx.author.id == int(os.getenv("ADMIN"))

	return commands.check(predicate)

#return the index of the available role. Return None if the index is not found
def check_if_role_available(role_name=None, role_meta=None):
	
	for ri, rl in enumerate(roles_list):
		if (role_name != None):
			if (role_name == rl["name"]):
				return ri
		elif (role_meta != None):
			if (role_meta == rl["meta"]):
				return ri
	return None

async def getRole(guild, role_name=None, role_meta=None):
	ri = check_if_role_available(role_name, role_meta)
	if (ri != None):
		guildRoles = await guild.fetch_roles()
		for gr in guildRoles:
			if gr.name == roles_list[ri]["name"]:
				return gr
		role = await guild.create_role(name=roles_list[ri]["name"], color=roles_list[ri]["color"], hoist=True, mentionable=True)
		return role
	print("role not found")
	return None

async def sudemote(ctx, role_meta):
	"""super promote rank"""
	guild = ctx.message.guild
	role = await getRole(guild, role_meta=role_meta)
	if (role != None):
		for m in role.members:
			logger("Removing the role " + role.name + " to " + m.name, None, ctx)
			await m.remove_roles(role)
	return role

async def supromote(ctx, role_meta):
	"""super promote rank"""
	member = ctx.message.author
	role = await sudemote(ctx, role_meta=role_meta)

	if (role != None):
		logger("Adding the role " + role.name + " to " + member.name, None, ctx)
		await member.add_roles(role)
	return role

class dummyUser:
	"""A dummy User/Guild for discord"""
	id = 0
	name = ""