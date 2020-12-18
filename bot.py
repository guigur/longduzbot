# bot.py
import os
import random
import time
import math
import json
import datetime
import requests
import asyncio
import discord

client = discord.Client()

import certif
import ggr_utilities
import ggr_emotes

from dotenv import load_dotenv
load_dotenv()


ggr_utilities.setup(client)

TOKEN = os.getenv("DISCORD_TOKEN")


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
            if not ggr_utilities.checkMaintenance(message.channel):
                helpmsg = "**!helpzbot :** Affiche ce message.\n"
                helpmsg += "**!ulian :** Spawn un imposant Ulian devant vous. Serez-vous prêt à faire face ?\n"
                helpmsg += "**!army :** Spawn une armée de minis Ulians et Moth de 10 à 50 membres dévoués et sanguinaires.\n"
                helpmsg += "**!megaarmy :** Spawn une imposante armée de minis Ulians et Moth sur plusieurs lignes (5 à 20). Cette commande ne peut être utilisé qu'une fois toutes les 20 minutes.\n"
                helpmsg += "**!maitre :** Affiche le maître des saloperies et son record.\n"
                helpmsg += "**!teub <emoji>:** Juste teub.\n"
                await message.channel.send(helpmsg)
            
        if message.content.startswith('!ulian'):
            if not ggr_utilities.checkMaintenance(message.channel):
                if "teub" in message.content:
                        head = teub
                else:
                    head = lilinkhisface
                body = lilinkhisrightelbow + head + lilinkhisleftelbow + "\n" + lilinkhisrightarm + lilinkhisbody + lilinkhisleftarm + "\n" + lilinkhisrightleg + lilinkhiscrotch + lilinkhisleftleg + "\n" + lilinkhisrightfoot + lilinkhisleftfoot + lilinkhislefttoes
                await message.channel.send(body)
        if message.content.startswith('!maitre'):
            if not ggr_utilities.checkMaintenance(message.channel):
                await message.channel.send("Le maître des saloperie est **" + saveFile['maitre']['user'] + "** avec un score de **" + str(saveFile['maitre']['best']) + "** saloperies invoqués")
            
        if message.content.startswith('!army'):
            if not ggr_utilities.checkMaintenance(message.channel):
                army = spawnArmy()[0]
                await message.channel.send(army)
        
        if message.content.startswith('!megaarmy'):
            if not ggr_utilities.checkMaintenance(message.channel):
                global timeReady
                armytotmembers = 0
                if message.author.name != saveFile['maitre']['user']:
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
                else:
                    await message.channel.send("Un maître n'a pas besoin de prouver sa valeur.\nLa votre est de **" + str(saveFile['maitre']['best']) + "** Saloperies.")


        if message.content.startswith('!test'):
            if not ggr_utilities.checkMaintenance(message.channel):
                message = await message.channel.send(salty)
           


        if message.content.startswith('!balance'):
            if not ggr_utilities.checkMaintenance(message.channel):
                message = await message.channel.send(salty)

            #await member.add_roles(rank)
            
            #user = message.author
            
            #await user.add_roles(discord.utils.get(user.guild.roles, name="Maître des Saloperies")) #add the role
            #await user.remove_roles(discord.utils.get(user.guild.roles, name="Maître des Saloperies")) #add the role
            #role = discord.utils.get("787148372397129748")
            #await member.add_roles(role)

            
            
        if message.content.startswith('!teub'):
            if not ggr_utilities.checkMaintenance():
                if 'Ulian' in message.content:
                    msg = faces["Tim"] + teub
                else:
                    msg = "Je ne trouve pas l'émote demandé \nÉmotes disponibles : Ulian"
                await message.channel.send(msg)
        
client.run(TOKEN)
print("prout")