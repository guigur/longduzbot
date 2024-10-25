import discord
from discord.ext import commands
import sys
import os
import json
import time
from enum import Enum
from datetime import datetime
import ggr_utilities, ggr_emotes
import Eco, Com

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, BigInteger, and_, func, desc, case
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import select

Base = declarative_base()

class MaitreJeanfoutreType(Enum):
	MAITRE = 0
	JEANFOUTRE = 1

	def data(self):
		if (self.value == 0):
			return {"table": "maitre", "idkey": "maitreID"}
		elif (self.value == 1):
			return {"table": "jeanfoutre", "idkey": "jeanfoutreID"}

# SQLAlchemy Models
class Money(Base):
	__tablename__ = 'money'
	moneyID = Column(Integer, primary_key=True, autoincrement=True)
	userID = Column(BigInteger)
	user = Column(String)
	guildID = Column(BigInteger)
	guild = Column(String)
	money = Column(Integer)

class MoneyTransaction(Base):
	__tablename__ = 'moneyTransaction'
	moneyTransactionID = Column(Integer, primary_key=True, autoincrement=True)
	userEmitterID = Column(BigInteger)
	userEmitter = Column(String)
	userReceiverID = Column(BigInteger)
	userReceiver = Column(String)
	guildID = Column(BigInteger)
	guild = Column(String)
	timestamp = Column(Float)
	money = Column(Integer)

class Army(Base):
	__tablename__ = 'army'
	armyID = Column(Integer, primary_key=True, autoincrement=True)
	userID = Column(BigInteger)
	user = Column(String)
	guildID = Column(BigInteger)
	guild = Column(String)
	timestamp = Column(Float)
	command = Column(String)
	saloperies = Column(Integer)
	money = Column(Integer)

class MegaArmy(Base):
	__tablename__ = 'megaarmy'
	megaarmyID = Column(Integer, primary_key=True, autoincrement=True)
	userID = Column(BigInteger)
	user = Column(String)
	guildID = Column(BigInteger)
	guild = Column(String)
	timestamp = Column(Float)
	command = Column(String)
	lines = Column(Integer)
	saloperies = Column(Integer)
	money = Column(Integer)

class Maitre(Base):
    __tablename__ = 'maitre'
    maitreID = Column(Integer, primary_key=True)  # Primary key
    userID = Column(Integer)
    user = Column(String)
    guildID = Column(Integer)
    guild = Column(String)
    timestamp = Column(Float)
    saloperies = Column(Integer)
    megaarmyID = Column(Integer)
    isArchive = Column(Integer)


class Jeanfoutre(Base):
    __tablename__ = 'jeanfoutre'
    jeanfoutreID = Column(Integer, primary_key=True)  # Primary key
    userID = Column(Integer)
    user = Column(String)
    guildID = Column(Integer)
    guild = Column(String)
    timestamp = Column(Float)
    saloperies = Column(Integer)
    megaarmyID = Column(Integer)
    isArchive = Column(Integer)

class Database(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db_url = "sqlite:///Database.db"
		self.engine = create_engine(self.db_url, echo=False)
		Base.metadata.create_all(self.engine)
		Session = sessionmaker(bind=self.engine)
		self.session = Session()

	def __del__(self):
		ggr_utilities.logger(self.__class__.__name__ + " Cog Unloaded!", self, None, ggr_utilities.LogType.WARN)

	######################## DISCORD COMMANDS ########################

	######################### SHELL COMMANDS #########################

	############################ ROUTINES ############################

	#ECO
	def periodHelper(self, startTimestamp, endTimestamp):
		if startTimestamp and endTimestamp:
			return (and_(MegaArmy.timestamp > startTimestamp, MegaArmy.timestamp < endTimestamp))
		return True

	def getStatsPercentileSaloperiesMegaArmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		query = self.session.query(MegaArmy.userID, MegaArmy.guildID, func.sum(MegaArmy.saloperies).label('total_saloperies'),
								   func.percent_rank().over(order_by=func.sum(MegaArmy.saloperies).desc()).label('percentile_rank')
								   ).filter(MegaArmy.guildID == guild.id).group_by(MegaArmy.userID, MegaArmy.guildID).subquery()
		result = self.session.query(query).filter(query.c.userID == user.id).first()
		return result

	def getStatsPercentileCommandMegaArmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		# Step 1: Count the total saloperies for each user in the given guild and apply filters
		subquery = self.session.query(
			MegaArmy.userID,
			func.count(MegaArmy.saloperies).label('total_saloperies')
		).filter(MegaArmy.guildID == guild.id)

		if startTimestamp:
			subquery = subquery.filter(MegaArmy.timestamp >= startTimestamp)
		if endTimestamp:
			subquery = subquery.filter(MegaArmy.timestamp <= endTimestamp)

		subquery = subquery.group_by(MegaArmy.userID).subquery()

		# Step 2: Calculate percentile rank using PERCENT_RANK() over total_saloperies in descending order
		percentile_query = self.session.query(
			subquery.c.userID,
			subquery.c.total_saloperies,
			func.percent_rank().over(order_by=subquery.c.total_saloperies.desc()).label('percentile_rank')
		).subquery()

		# Step 3: Fetch the specific user's percentile rank data
		user_percentile_data = self.session.query(percentile_query).filter(percentile_query.c.userID == user.id).first()

		# Step 4: Format the response
		if user_percentile_data:
			percentile_rank = 100 * (1 - user_percentile_data.percentile_rank)
		else:
			percentile_rank = 0  # Default if user has no data in this period

		return {
			'user_id': user.id,
			'total_saloperies': user_percentile_data.total_saloperies if user_percentile_data else 0,
			'percentile_rank': percentile_rank
		}

	def getStatsCountSaloperiesMegaArmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		result = self.session.query(func.count(MegaArmy.megaarmyID).label('nbr_cmds')).filter(
			MegaArmy.userID == user.id,
			MegaArmy.guildID == guild.id,
			self.periodHelper(startTimestamp, endTimestamp)
		).first()
		return result[0]

	def getStatsBestDaySaloperiesMegaArmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		result = self.session.query(func.strftime('%Y-%m-%d', MegaArmy.timestamp, 'unixepoch').label('day'),
									func.sum(MegaArmy.saloperies).label('max_saloperies')
									).filter(
			MegaArmy.userID == user.id,
			MegaArmy.guildID == guild.id,
			self.periodHelper(startTimestamp, endTimestamp)
		).group_by('day').order_by(func.sum(MegaArmy.saloperies).desc()).first()
		if (result == None):
			return {'timestamp': startTimestamp, "saloperies": 0} #if no records are present of this period, then return the startTimestamp
		return {'timestamp': datetime.strptime(result[0], '%Y-%m-%d').timestamp(), "saloperies": result[1]}

	def getStatsSaloperiesMegaArmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		query = self.session.query(func.coalesce(func.sum(MegaArmy.saloperies), 0).label('sumSaloperies'))\
							.filter(MegaArmy.userID == user.id, MegaArmy.guildID == guild.id)

		# Apply timestamp filtering
		if startTimestamp:
			query = query.filter(MegaArmy.timestamp >= startTimestamp)
		if endTimestamp:
			query = query.filter(MegaArmy.timestamp <= endTimestamp)

		result = query.first()
		return result.sumSaloperies

	def getStatsSaloperieArmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		query = self.session.query(func.coalesce(func.sum(Army.saloperies), 0).label('sumSaloperies'))\
							.filter(Army.userID == user.id, Army.guildID == guild.id)

		if startTimestamp:
			query = query.filter(Army.timestamp >= startTimestamp)
		if endTimestamp:
			query = query.filter(Army.timestamp <= endTimestamp)

		result = query.first()
		return result.sumSaloperies

	def getStatsWadsOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		query = self.session.query(func.coalesce(func.sum(MoneyTransaction.money), 0).label('sumMoney'))\
							.filter(MoneyTransaction.userReceiverID == user.id, MoneyTransaction.guildID == guild.id)

		if startTimestamp:
			query = query.filter(MoneyTransaction.timestamp >= startTimestamp)
		if endTimestamp:
			query = query.filter(MoneyTransaction.timestamp <= endTimestamp)

		result = query.first()
		return result.sumMoney

	def getStatsWadsBestDayOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		query = self.session.query(func.coalesce(func.max(MoneyTransaction.money), 0).label('maxMoney'))\
							.filter(MoneyTransaction.userReceiverID == user.id, MoneyTransaction.guildID == guild.id)

		if startTimestamp:
			query = query.filter(MoneyTransaction.timestamp >= startTimestamp)
		if endTimestamp:
			query = query.filter(MoneyTransaction.timestamp <= endTimestamp)

		result = query.first()
		return result.maxMoney

	def getBestMegaArmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		query = self.session.query(func.coalesce(func.max(MegaArmy.saloperies), 0).label('maxSaloperies'))\
							.filter(MegaArmy.userID == user.id, MegaArmy.guildID == guild.id)

		if startTimestamp:
			query = query.filter(MegaArmy.timestamp >= startTimestamp)
		if endTimestamp:
			query = query.filter(MegaArmy.timestamp <= endTimestamp)

		result = query.first()
		return result.maxSaloperies

	def getStatsPercentileWads(self, user, guild):
		subquery = (
			self.session.query(
				MoneyTransaction.userReceiverID,
				MoneyTransaction.guildID,
				MoneyTransaction.money,
				func.rank().over(order_by=MoneyTransaction.money.desc()).label('rank')
			)
			.filter(MoneyTransaction.guildID == guild.id)
			.subquery()
		)

		total_rows = self.session.query(subquery).count()

		# Calculate percentile rank
		user_rank = self.session.query(subquery)\
								.filter(subquery.c.userReceiverID == user.id)\
								.first()

		if total_rows > 1:
			percentile = 100 - (user_rank.rank / total_rows * 100)
		else:
			percentile = 100

		return percentile

	def getWorstMegaArmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		query = self.session.query(func.coalesce(func.min(MegaArmy.saloperies), 0).label('minSaloperies'))\
							.filter(MegaArmy.userID == user.id, MegaArmy.guildID == guild.id)

		if startTimestamp:
			query = query.filter(MegaArmy.timestamp >= startTimestamp)
		if endTimestamp:
			query = query.filter(MegaArmy.timestamp <= endTimestamp)

		result = query.first()
		return result.minSaloperies

	def getBestArmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		query = self.session.query(func.coalesce(func.max(Army.saloperies), 0).label('maxSaloperies'))\
							.filter(Army.userID == user.id, Army.guildID == guild.id)

		if startTimestamp:
			query = query.filter(Army.timestamp >= startTimestamp)
		if endTimestamp:
			query = query.filter(Army.timestamp <= endTimestamp)

		result = query.first()
		return result.maxSaloperies

	def getWorstArmyOnPeriod(self, user, guild, startTimestamp=None, endTimestamp=None):
		query = self.session.query(func.coalesce(func.min(Army.saloperies), 0).label('minSaloperies'))\
							.filter(Army.userID == user.id, Army.guildID == guild.id)

		if startTimestamp:
			query = query.filter(Army.timestamp >= startTimestamp)
		if endTimestamp:
			query = query.filter(Army.timestamp <= endTimestamp)

		result = query.first()
		return result.minSaloperies

	def getDBMoneyRichOrder(self, guild, limit=0):
		query = self.session.query(Money)\
							.filter(Money.guildID == guild.id)\
							.order_by(Money.money.desc())

		if limit > 0:
			query = query.limit(limit)

		rows = query.all()
		return rows

	def changeDBBalanceMoney(self, user, guild):
		money = self.getDBMoney(user, guild)
		if money is None:
			self.createDBAccountMoney(user, guild)
		return self.getDBMoney(user, guild)

	def getDBMoneyVerif(self, user, guild):
		money = self.getDBMoney(user, guild)
		if money is None:
			self.createDBAccountMoney(user, guild)
		return self.getDBMoney(user, guild)


	def getDBMoney(self, user, guild):
		result = self.session.query(Money).filter_by(userID=user.id, guildID=guild.id).order_by(Money.moneyID.desc()).first()
		return result

	def createDBAccountMoney(self, user, guild):
		freeStartingMoney = 1
		money = self.getDBMoney(user, guild)
		if not money:
			new_money = Money(userID=user.id, user=user.name, guildID=guild.id, guild=guild.name, money=freeStartingMoney)
			self.session.add(new_money)
			self.session.commit()
			ggr_utilities.logger("Welcome to the bank of " + Eco.moneyName() + " " + user.name, self)
		else:
			ggr_utilities.logger("The account for user " + user.name + " already exists", self)

	def changeDBBalanceMoney(self, user, guild, diff):
		currentBalance = self.getDBMoney(user, guild)
		if currentBalance:
			currentBalance.money += diff
			self.session.commit()

			# Log the money transaction
			self.logDBMoneyTransaction(userEmitter=guild, userReceiver=user, guild=guild, timestamp=time.time(), money=diff)

	def logDBMoneyTransaction(self, userEmitter, userReceiver, guild, timestamp, money):
		transaction = MoneyTransaction(
			userEmitterID=userEmitter.id,
			userEmitter=userEmitter.name,
			userReceiverID=userReceiver.id,
			userReceiver=userReceiver.name,
			guildID=guild.id,
			guild=guild.name,
			timestamp=timestamp,
			money=money
		)
		self.session.add(transaction)
		self.session.commit()

	#Army
	def setDBMaitreJeanfoutre(self, type, user, guild, timestamp, saloperies, megaarmyID):
		table_class = Maitre if type == MaitreJeanfoutreType.MAITRE else Jeanfoutre
		row = self.session.query(table_class).order_by(table_class.__table__.c[type.data()['idkey']].desc()).first()

		if row is None or row.isArchive != 0:
			ggr_utilities.logger("No past " + type.data()['table'] + ". Creating a new line!", self)
			new_record = table_class(
				userID=user.id, user=user.name, guildID=guild.id, guild=guild.name,
				timestamp=timestamp, saloperies=saloperies, megaarmyID=megaarmyID, isArchive=0
			)
			self.session.add(new_record)
			self.session.commit()  # Commit here to get the `id`
			return new_record.maitreID if type == MaitreJeanfoutreType.MAITRE else new_record.jeanfoutreID
		else:
			row.id = row.maitreID if type == MaitreJeanfoutreType.MAITRE else row.jeanfoutreID
			ggr_utilities.logger("Old " + type.data()['table'] + " is out, using his old line " + str(row.id), self)
			row.userID = user.id
			row.user = user.name
			row.guildID = guild.id
			row.guild = guild.name
			row.timestamp = timestamp
			row.saloperies = saloperies
			row.megaarmyID = megaarmyID
			row.isArchive = 0  # Set it as active again
			self.session.commit()
			return row.id

	def getDBMaitreJeanfoutre(self, type, guild):
		table_class = Maitre if type == MaitreJeanfoutreType.MAITRE else Jeanfoutre
		row = self.session.query(table_class).filter_by(isArchive=0, guildID=guild.id).order_by(table_class.__table__.c[type.data()['idkey']].desc()).first()
		return row

	def setDBArchiveMaitreJeanfoutre(self, type, guild):
		table_class = Maitre if type == MaitreJeanfoutreType.MAITRE else Jeanfoutre
		self.session.query(table_class).filter_by(isArchive=0, guildID=guild.id).update({"isArchive": 1})
		self.session.commit()

	def addDBArmy(self, user, guild, timestamp, command, saloperies, money):
		new_army = Army(
			userID=user.id, user=user.name, guildID=guild.id, guild=guild.name,
			timestamp=timestamp, command=command, saloperies=saloperies, money=money
		)
		self.session.add(new_army)
		self.session.commit()
		return new_army.armyID

	def addDBMegaArmy(self, user, guild, timestamp, command, lines, saloperies, money):
		new_mega_army = MegaArmy(
			userID=user.id, user=user.name, guildID=guild.id, guild=guild.name,
			timestamp=timestamp, command=command, lines=lines, saloperies=saloperies, money=money
		)
		self.session.add(new_mega_army)
		self.session.commit()
		return new_mega_army.megaarmyID

	def requestDB(self, query):
		ggr_utilities.logger("SQLAlchemy Query Executed", self)

def setup(bot):
	bot.add_cog(Database(bot))

def teardown(bot):
	print(bot.__name__)