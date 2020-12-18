import discord

maintenance = True
client = None

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

def setup(masterClient):
    global client
    client = type(masterClient)
    client = masterClient

@client.event
async def checkMaintenance(channel):
    if maintenance:
        print("je suis en maintenance, réessayer plus tard !")
        await channel.send("je suis en maintenance, réessayer plus tard !")
        return True
    return False