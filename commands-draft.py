async def on_message(message):
    if message.channel.id == 770771959122362398 or message.channel.id == 495361629806919693:
        if message.content.startswith('!helpzbot'):
            if not ggr_utilities.checkMaintenance(message.channel):
                helpmsg = "**!helpzbot :** Affiche ce message.\n"
                helpmsg += "**!teub <emoji>:** Juste teub.\n"
            



            #await member.add_roles(rank)
            
            #user = message.author
            
            #await user.add_roles(discord.utils.get(user.guild.roles, name="Maître des Saloperies")) #add the role
            #await user.remove_roles(discord.utils.get(user.guild.roles, name="Maître des Saloperies")) #add the role
            #role = discord.utils.get("787148372397129748")
            #await member.add_roles(role)


        