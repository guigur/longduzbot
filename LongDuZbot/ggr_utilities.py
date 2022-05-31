#import discord
import datetime
import math
import requests

roleName = "Maître des Saloperies"
roleColor = 0xffde00

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

def serverIcon(ctx):
	guildUrl = ctx.guild.icon_url_as(format='png')
	try:
		guildImg = requests.get(guildUrl, stream=True).raw
	except requests.exceptions.RequestException as e:
		guildImg = pickDefImage(ctx.guild.name)

	return guildImg

def userIcon(user):
	userUrl = user.avatar_url_as(format='png')
	try:
		userImg = requests.get(userUrl, stream=True).raw
	except requests.exceptions.RequestException as e:
		userImg = pickDefImage(user.name)
	return userImg

def checkIfIdValid(id):
	if (isinstance(id, int)):
		if (int(id) > 9999999999999999):
			return True
		else:
			pass
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

def logger(ctx, string):
	if ctx:
		usr = ctx.message.author.name
	else:
		usr = "server"
	string = pDT() + " " + usr + "] "+ string
	print(string)
	#todo: add to file

async def getRole(guild):
	guildRoles = await guild.fetch_roles()
	role = None
	for r in guildRoles:
		if (r.name == roleName):
			doRoleExist = True
			role = r
	if (role == None):
		role = await guild.create_role(name=roleName, color=roleColor, hoist=True, mentionable=True)
	return role

async def initr(ctx):
	"""init rank"""
	guild = ctx.message.guild
	role = await getRole(guild)

async def promote(ctx):
	"""promote rank"""
	member = ctx.message.author
	guild = ctx.message.guild
	role = await getRole(guild)
	await member.add_roles(role)

async def demote(ctx):
	"""demote rank"""
	member = ctx.message.author
	guild = ctx.message.guild
	role = await getRole(guild)
	await member.remove_roles(role)

async def supromote(ctx):
	"""super promote rank"""
	member = ctx.message.author
	guild = ctx.message.guild
	role = await getRole(guild)

	for m in role.members:
		logger(ctx, "Removing the role " + role.name + " to " + m.name)
		await m.remove_roles(role)
	
	logger(ctx, "Adding the role " + role.name + " to " + member.name)
	await member.add_roles(role)