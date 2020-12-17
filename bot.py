# bot.py
import os
import random
import time
import math
import json
import datetime
import requests
import certif
import asyncio

import discord
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()

flingued = "<:flingued:784167892668252181>"
flingueg = "<:flingueg:784167860930609172>"

salty = "<a:salty:788971656726839306>"

maing = "<:maing:>"
maind = "<:maind:>"

lilian3flip = "<:lilian3flip:>"
Lilian3 = "<:Lilian3:>"

DrakeOK = "<:DrakeOK:>"
DrakeNO = "<:DrakeNO:>"

Knife = "<:Knife:>"

teub = "<:teub:784174377205104671>"

petou = "<:petou:>"

Ulian = "<:Ulian:784169312976896040>"
Moth = "<:Moth:784169313019101204>"

lilinkhisrightelbow = "<:lilinkhisrightelbow:784177962970513438>"
lilinkhisface = "<:lilinkhisface:784177963008524288>"
lilinkhisleftelbow = "<:lilinkhisleftelbow:784177962961338378>"
lilinkhisrightarm = "<:lilinkhisrightarm:784177962986504213>"
lilinkhisbody = "<:lilinkhisbody:784177962865262643>"
lilinkhisleftarm = "<:lilinkhisleftarm:784177962978246686>"
lilinkhisrightleg = "<:lilinkhisrightleg:784182056790786059>"
lilinkhiscrotch = "<:lilinkhiscrotch:784182057152151582>"
lilinkhisleftleg = "<:lilinkhisleftleg:784182057093038150>"
lilinkhisrightfoot = "<:lilinkhisrightfoot:784184399536455681>"
lilinkhisleftfoot = "<:lilinkhisleftfoot:784184399511814186>"
lilinkhislefttoes = "<:lilinkhislefttoes:784184399955755029>"

faces = {'Tim': '<:Tim:784142816896352296>', 
'Pretzel': '<:Pretzel:>',
'Poscoll': '<:Poscoll:>',
'Poscol2': '<:Poscol2:>',
'Poscol1': '<:Poscol1:>',
'Paul': '<:Paul:>',
'Pat3': '<:Pat3:>',
'Pat2': '<:Pat2:>',
'Pat1': '<:Pat1:>',
'Olox6': '<:Olox6:>',
'Olox5': '<:Olox5:>',
'Olox4': '<:Olox4:>',
'Olox3': '<:Olox3:>',
'Olox2': '<:Olox2:>',
'Olox1': '<:Olox1:>',
'Olox': '<:Olox:>',
'Noe1': '<:Noe1:>',
'Noe': '<:Noe:>',
'Nico': '<:Nico:>',
'Mat7': '<:Mat7:>',
'Mat6': '<:Mat6:>',
'Mat5': '<:Mat5:>',
'Mat4': '<:Mat4:>',
'Mat3': '<:Mat3:>',
'Mat2': '<:Mat2:>',
'Mat1': '<:Mat1:>',
'Mae2': '<:Mae2:>',
'Mae1': '<:Mae1:>',
'Lilian7': '<:Lilian7:>',
'Lilian6': '<:Lilian6:>',
'Lilian5': '<:Lilian5:>',
'Lilian4': '<:Lilian4:>',
'Lilian2': '<:Lilian2:>',
'lilian': '<:lilian:>',
'Guillaume': '<:Guillaume:>',
'Franck': '<:Franck:>',
'Forian': '<:Forian:>',
'Flo': '<:Flo:>',
'Chriss': '<:Chriss:>',
'Chat': '<:Chat:>',
'Charlotte': '<:Charlotte:>',
'Carotte': '<:Carotte:>',
'Benoir2': '<:Benoir2:>',
'Benoir1': '<:Benoir1:>',
'Arnould': '<:Arnould:>',
'Antoinos2': '<:Antoinos2:>',
'Antoinos1': '<:Antoinos1:>',
'Anna3': '<:Anna3:>',
'Anna2': '<:Anna2:>',
'Anna': '<:Anna:>',
'AlexPetard': '<:AlexPetard:>',
}

timeReady = 0

with open('maitre.json', encoding='utf-8') as json_file:
    saveFile = json.load(json_file)
    
def spawnArmy():
    army = ""
    armynbr = random.randint(10, 40)
    for x in range(0, armynbr):
        armymbr = random.randint(0, 1)
        if armymbr == 0:
            army += Ulian
        else:
            army += Moth
    return [army, armynbr]



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
    
def saveToFile():
    print("Saving to file")
    with open('maitre.json', 'w') as json_file:
        json.dump(saveFile, json_file)


def pDT():
    now = datetime.datetime.now()
    return (now.strftime("%m/%d/%Y %H:%M:%S]"))

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    global timeReady
    timeReady = time.time()



@client.event
async def on_message(message):
    if message.channel.id == 770771959122362398 or message.channel.id == 495361629806919693:
        if message.content.startswith('!helpzbot'):
            helpmsg = "**!helpzbot :** Affiche ce message.\n"
            helpmsg += "**!ulian :** Spawn un imposant Ulian devant vous. Serez-vous prêt à faire face ?\n"
            helpmsg += "**!army :** Spawn une armée de minis Ulians et Moth de 10 à 50 membres dévoués et sanguinaires.\n"
            helpmsg += "**!megaarmy :** Spawn une imposante armée de minis Ulians et Moth sur plusieurs lignes (5 à 20). Cette commande ne peut être utilisé qu'une fois toutes les 20 minutes.\n"
            helpmsg += "**!maitre :** Affiche le maître des saloperies et son record.\n"
            helpmsg += "**!teub <emoji>:** Juste teub.\n"
            await message.channel.send(helpmsg)
            
        if message.content.startswith('!ulian'):
            if "teub" in message.content:
                    head = teub
            else:
                head = lilinkhisface
            body = lilinkhisrightelbow + head + lilinkhisleftelbow + "\n" + lilinkhisrightarm + lilinkhisbody + lilinkhisleftarm + "\n" + lilinkhisrightleg + lilinkhiscrotch + lilinkhisleftleg + "\n" + lilinkhisrightfoot + lilinkhisleftfoot + lilinkhislefttoes
            await message.channel.send(body)
        if message.content.startswith('!maitre'):
            await message.channel.send("Le maître des saloperie est **" + saveFile['maitre']['user'] + "** avec un score de **" + str(saveFile['maitre']['best']) + "** saloperies invoqués")
            
        if message.content.startswith('!army'):
            army = spawnArmy()[0]
            await message.channel.send(army)
        
        if message.content.startswith('!megaarmy'):
            global timeReady
            armytotmembers = 0
            if time.time() > timeReady:
                print(pDT() + "User " + message.author.name + " summoned a megaarmy")
                timeReady = time.time() + 1200
                armyLines = random.randint(5, 20)
                for x in range(0, armyLines):
                    retarmy = spawnArmy()
                    army = retarmy[0]
                    armytotmembers += retarmy[1]
                    await message.channel.send(army)
                for emojinmb in numbersToEmojis(armyLines):
                    await message.add_reaction(emojinmb)
                print(pDT() + "User " + message.author.name + " summoned " + str(armytotmembers))
                await message.channel.send("Votre armée compte **" + str(armytotmembers) + "** saloperies. Beau travail.")
                
                
                if armytotmembers > saveFile['maitre']['best']:
                    print(pDT() + "User " + message.author.name + " is now the master")

                    user = message.author

                    #oldmaitre = user.guild.members() #199222032787963904) #user = client.get_user()
                    #await user.remove_roles(discord.utils.get(user.guild.roles, name="Maître des Saloperies")) #remove the role
                    
                    saveFile['maitre']['best'] = armytotmembers;
                    saveFile['maitre']['user'] = message.author.name
                    saveFile['maitre']['userid'] = message.author.id
                    saveFile['maitre']['date'] = datetime.datetime.timestamp(datetime.datetime.now())


                    saveToFile()
                    await message.channel.send("Félicitations " + user.mention + " vous êtes le nouveau **Maître des Saloperies**")
                    url = message.author.avatar_url_as(format='png')          
                    picture = certif.certifGen(requests.get(url, stream=True).raw, message.author.name, armytotmembers)
                    await message.channel.send(file=discord.File('tmp/certif_filled.png'))
                    await message.channel.send("Ce certificat prouve votre titre de **Maître des Saloperies**\nN'hésitez pas à mentionner ce titre prestigieux sur votre CV.")
                    await user.add_roles(discord.utils.get(user.guild.roles, name="Maître des Saloperies"))

                else:
                    await message.channel.send("Bien mais il y a mieux")
            else:
                await message.channel.send("La méga armée de saloperies n'est pas prête.\nRéessayez dans quelques minutes.")
                await message.add_reaction("❌")


        if message.content.startswith('!test'):
            message = await message.channel.send(salty)
           


        if message.content.startswith('!balance'):
            message = await message.channel.send(salty)

            #await member.add_roles(rank)
            
            #user = message.author
            
            #await user.add_roles(discord.utils.get(user.guild.roles, name="Maître des Saloperies")) #add the role
            #await user.remove_roles(discord.utils.get(user.guild.roles, name="Maître des Saloperies")) #add the role
            #role = discord.utils.get("787148372397129748")
            #await member.add_roles(role)

            
            
        if message.content.startswith('!teub'):
            if 'Ulian' in message.content:
                msg = faces["Tim"] + teub
            else:
                msg = "Je ne trouve pas l'émote demandé \nÉmotes disponibles : Ulian"
            await message.channel.send(msg)
        
client.run(TOKEN)
print("prout")