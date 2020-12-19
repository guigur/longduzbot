@client.event
async def on_message(message):
    if message.channel.id == 770771959122362398 or message.channel.id == 495361629806919693:
        if message.content.startswith('!helpzbot'):
            if not ggr_utilities.checkMaintenance(message.channel):
                helpmsg = "**!helpzbot :** Affiche ce message.\n"
                helpmsg += "**!ulian :** Spawn un imposant Ulian devant vous. Serez-vous prêt à faire face ?\n"
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
        