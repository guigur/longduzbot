import discord
from discord.ext import commands
import ggr_utilities
import ggr_emotes

class Ulian(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def ulian(self, ctx):
		"""Spawn un imposant Ulian devant vous. Serez-vous prêt à faire face ?"""
		ggr_utilities.logger(ctx, ctx.message.content)
		if "teub" in message.content:
			head = teub
		else:
			head = lilinkhisface
			body = lilinkhisrightelbow + head + lilinkhisleftelbow + "\n"
			body += lilinkhisrightarm + lilinkhisbody + lilinkhisleftarm + "\n"
			body += lilinkhisrightleg + lilinkhiscrotch + lilinkhisleftleg + "\n"
			body += lilinkhisrightfoot + lilinkhisleftfoot + lilinkhislefttoes
			await message.channel.send(body)

def setup(bot):
	bot.add_cog(Ulian(bot))
