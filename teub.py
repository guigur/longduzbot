import discord
from discord.ext import commands
import ggr_utilities
import ggr_emotes

class Teub(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="teub *emote*")
	async def teub(self, ctx):
		"""Juste teub."""
		ggr_utilities.logger(ctx, ctx.message.content)
		if 'Tim' in message.content:
			msg = faces["Tim"] + teub
		else:
			msg = "Je ne trouve pas l'émote demandée \némotes disponibles : Tim"
			ggr_utilities.logger(ctx, "emote not found")
		await message.channel.send(msg)

def setup(bot):
	bot.add_cog(Teub(bot))
