import discord
from discord.ext import commands
import ggr_utilities
import ggr_emotes

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        """Test cmd"""
        await ctx.send('test ! {0.name}'.format(ctx.author))
        rankName = "caca"#Maître des Saloperies"
        user = ctx.message.author
        try:
            await user.add_roles(discord.utils.get(user.guild.roles, name=rankName))
        except discord.Forbidden:
            print(ggr_utilities.pDT() + "Probleme de droits pour ajouter le rank " + rankName + " à " + user.name)
            pass

def setup(bot):
    bot.add_cog(Test(bot))
