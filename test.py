import math
import discord
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()

def digitToEmoji(digit):
    if digit == 0:
        return ":zero:"
    elif digit == 1:
        return ":one:"
    elif digit == 2:
        return ":two:"
    elif digit == 3:
        return ":three:"
    elif digit == 4:
        return ":four:"
    elif digit == 5:
        return ":five:"
    elif digit == 6:
        return ":six:"
    elif digit == 7:
        return ":seven:"
    elif digit == 8:
        return ":eight:"
    elif digit == 9:
        return ":nine:"

def numbersToEmojis(number):
    decade = math.trunc( number / 10)
    print(digitToEmoji(decade) + digitToEmoji(number % 10))
    

#guild = discord.guild

#user = guild.get_member(234672235342856202)



@client.event
async def on_ready():
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )



client.run(TOKEN)