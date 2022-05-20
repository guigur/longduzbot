import discord
from discord.ext import commands
import sys
import os
import ggr_utilities
import ggr_emotes
import eco

class Test(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.roleName = "Maître des Saloperies"
		self.roleColor = 0xffde00

	async def getRole(self, guild):
		guildRoles = await guild.fetch_roles()
		role = None
		for r in guildRoles:
			if (r.name == self.roleName):
				doRoleExist = True
				role = r
		if (role == None):
			role = await guild.create_role(name=self.roleName, color=self.roleColor, hoist=True, mentionable=True)
		return role

	@commands.command()
	async def initr(self, ctx):
		"""init rank"""
		guild = ctx.message.guild
		role = await self.getRole(guild)

	@commands.command()
	async def promote(self, ctx):
		"""promote rank"""
		member = ctx.message.author
		guild = ctx.message.guild
		role = await self.getRole(guild)
		await member.add_roles(role)

	@commands.command()
	async def demote(self, ctx):
		"""demote rank"""
		member = ctx.message.author
		guild = ctx.message.guild
		role = await self.getRole(guild)
		await member.remove_roles(role)

	@commands.command()
	async def supromote(self, ctx):
		"""super promote rank"""
		member = ctx.message.author
		guild = ctx.message.guild
		role = await self.getRole(guild)

		for m in role.members:
			ggr_utilities.logger(ctx, "Removing the role " + role.name + " to " + m.name)
			await m.remove_roles(role)
		
		ggr_utilities.logger(ctx, "Adding the role " + role.name + " to " + member.name)
		await member.add_roles(role)

def setup(bot):
	bot.add_cog(Test(bot))


		#os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
		#print("exit")
		#sys.exit(0)
		#await ctx.send("test")
		#await ctx.send(ctx.author.name)
	
		#eco.Eco.changeBallance(ctx.author, 20)