
import sqlite3
import json

escape = lambda a: json.dumps(a.replace("\"", ""))

class dummyUser:
	"""A dummy User/Guild for discord"""
	def __init__(self, id, name):
		self.id = id
		self.name = name

db = "longduzbot.db"
con = sqlite3.connect(db)
cur = con.cursor()
guild = dummyUser(806284513583169596, "La théorie du Sel")
def createDB():
	requestDB("CREATE TABLE money (moneyID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, money)")
	requestDB("CREATE TABLE moneyTransaction (moneyTransactionID INTEGER PRIMARY KEY AUTOINCREMENT, userEmitterID, userEmitter, userReceiverID, userReceiver, guildID, guild, timestamp, money)")

	requestDB("CREATE TABLE army (armyID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, timestamp, command, saloperies, money)")
	requestDB("CREATE TABLE megaarmy (megaarmyID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, timestamp, command, lines, saloperies, money)")

	requestDB("CREATE TABLE maitre (maitreID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, timestamp, saloperies, megaarmyID INTEGER NOT NULL, isArchive INTEGER NOT NULL, FOREIGN KEY(megaarmyID) REFERENCES megaarmy(megaarmyID))")
	requestDB("CREATE TABLE jeanfoutre (jeanfoutreID INTEGER PRIMARY KEY AUTOINCREMENT, userID, user, guildID, guild, timestamp, saloperies, megaarmyID INTEGER NOT NULL, isArchive INTEGER NOT NULL, FOREIGN KEY(megaarmyID) REFERENCES megaarmy(megaarmyID))")

def requestDB(request):
	try:
		cur.execute(request)
		con.commit()
	except sqlite3.OperationalError as e:
		print(e)
	else:
		print("ok")

def insertMoney(user, guild, Balance):
	request = "REPLACE INTO money VALUES(NULL, " + str(int(user.id)) + ", " + escape(user.name) + ", " + \
	str(int(guild.id)) + ", " + escape(guild.name) + ", " + str(Balance) + ")"
	requestDB(request)

createDB()
f = open('economy.json')
data = json.load(f)
for line in data:
    insertMoney(dummyUser(int(line["id"]), line["name"]), guild, line["balance"])
f.close()
