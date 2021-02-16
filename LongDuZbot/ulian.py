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
		if "teub" in ctx.message.content: #not working anymore
			head = ggr_emotes.teub
		else:
			head = ggr_emotes.lilinkhisface
			body = ggr_emotes.lilinkhisrightelbow + head + ggr_emotes.lilinkhisleftelbow + "\n"
			body += ggr_emotes.lilinkhisrightarm + ggr_emotes.lilinkhisbody + ggr_emotes.lilinkhisleftarm + "\n"
			body += ggr_emotes.lilinkhisrightleg + ggr_emotes.lilinkhiscrotch + ggr_emotes.lilinkhisleftleg + "\n"
			body += ggr_emotes.lilinkhisrightfoot + ggr_emotes.lilinkhisleftfoot + ggr_emotes.lilinkhislefttoes
			await ctx.message.channel.send(body)

def setup(bot):
	bot.add_cog(Ulian(bot))
