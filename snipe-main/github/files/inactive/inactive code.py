"""CODE FOR DB STATS"""

"""
on guild join
@client.event
async def on_guild_join(guild):
    connect = sqlite3.connect("files/stats.db")
    cursor = connect.cursor()

    cursor.execute(f"INSERT into stats VALUES ({guild.id}, 0, 0, 0, 0)")

    connect.commit()
    connect.close()
""" # enable stats

"""
on guild remove
c = sqlite3.connect("files/stats.db")
cursor = c.cursor()
cursor.execute(f"SELECT * FROM stats WHERE guild_id={guild.id}")
if not cursor.fetchone():
    ...
else:
    cursor.execute(f"DELETE from stats WHERE guild_id='{guild.id}'")
c.commit()
c.close()
""" 

"""
on message edit
c = sqlite3.connect("files/stats.db")
cursor = c.cursor()

cursor.execute(f"SELECT editmsg FROM stats WHERE guild_id={before.guild.id}")
cursor.execute(f"UPDATE stats SET editmsg = {cursor.fetchone()[0] + 1} WHERE guild_id={before.guild.id}")

c.commit()
c.close()
"""

"""
on message delete
c = sqlite3.connect("files/stats.db")
cursor = c.cursor()

cursor.execute(f"SELECT delmsg FROM stats WHERE guild_id={message.guild.id}")
cursor.execute(f"UPDATE stats SET delmsg = {cursor.fetchone()[0] + 1} WHERE guild_id={message.guild.id}")

c.commit()
c.close()
"""

"""
local stats
cursor.execute(f"SELECT snipe FROM stats WHERE guild_id={ctx.guild.id}")
embed.add_field(name=f"Messages Sniped: {cursor.fetchone()[0]}", value=f"Total amount of messages sniped", inline=False)
cursor.execute(f"SELECT esnipe FROM stats WHERE guild_id={ctx.guild.id}")
embed.add_field(name=f"Messages Editsniped: {cursor.fetchone()[0]}", value=f"Total amount of edited messages sniped", inline=False)
cursor.execute(f"SELECT delmsg FROM stats WHERE guild_id={ctx.guild.id}")
embed.add_field(name=f"Deleted Messages Logged: {cursor.fetchone()[0]}", value=f"Total amount of deleted messages logged", inline=False)
cursor.execute(f"SELECT editmsg FROM stats WHERE guild_id={ctx.guild.id}")
embed.add_field(name=f"Edited Messages Logged: {cursor.fetchone()[0]}", value=f"Total amount of edited messages logged", inline=False)
embed.set_footer(text=f"Server ID: {ctx.guild.id}", icon_url=ctx.guild.icon_url)
"""

"""     
global stats
cursor.execute(f"SELECT snipe FROM stats WHERE guild_id={int(-1)}")
embed.add_field(name="Messages Sniped", value=f"`{cursor.fetchone()[0]}`")
cursor.execute(f"SELECT esnipe FROM stats WHERE guild_id={int(-1)}")
embed.add_field(name="Messages Editsniped", value=f"`{cursor.fetchone()[0]}`")
cursor.execute(f"SELECT delmsg FROM stats WHERE guild_id={int(-1)}")
embed.add_field(name="Deleted Messages Logged", value=f"`{cursor.fetchone()[0]}`")
cursor.execute(f"SELECT editmsg FROM stats WHERE guild_id={int(-1)}")
embed.add_field(name="Edited Messages Logged", value=f"`{cursor.fetchone()[0]}`")
"""

"""
multisnipe
c = sqlite3.connect("files/stats.db")
cursor = c.cursor()

cursor.execute(f"SELECT snipe FROM stats WHERE guild_id={ctx.guild.id}")
cursor.execute(f"UPDATE stats SET snipe={cursor.fetchone()[0] + 1} WHERE guild_id={ctx.guild.id}")

c.commit()
c.close()
"""

"""
usersnipe
c = sqlite3.connect("files/stats.db")
cursor = c.cursor()

cursor.execute(f"SELECT snipe FROM stats WHERE guild_id={ctx.guild.id}")
cursor.execute(f"UPDATE stats SET snipe={cursor.fetchone()[0] + 1} WHERE guild_id={ctx.guild.id}")

c.commit()
c.close()
"""

"""
snipe
c = sqlite3.connect("files/stats.db")
cursor = c.cursor()

cursor.execute(f"SELECT snipe FROM stats WHERE guild_id={ctx.guild.id}")
cursor.execute(f"UPDATE stats SET snipe = {cursor.fetchone()[0] + 1} WHERE guild_id={ctx.guild.id}")

c.commit()
c.close()
"""

"""
editsnipe
c = sqlite3.connect("files/stats.db")
cursor = c.cursor()

cursor.execute(f"SELECT esnipe FROM stats WHERE guild_id={int(-1)}")
cursor.execute(f"UPDATE stats SET esnipe = {cursor.fetchone()[0] + 1} WHERE guild_id={int(-1)}")

c.commit()
c.close()
"""

"""
guild remove
@client.event
async def on_guild_remove(guild):

    # Clear out all options for the server

    c = sqlite3.connect("files/edit_log.db")
    cursor = c.cursor()
    cursor.execute(f"SELECT * FROM servers WHERE guild_id={guild.id}")
    if not cursor.fetchone():
        ...
    else:
        cursor.execute(f"DELETE from servers WHERE guild_id='{guild.id}'")
    c.commit()
    c.close()

    c = sqlite3.connect("files/message_log.db")
    cursor = c.cursor()
    cursor.execute(f"SELECT * FROM servers WHERE guild_id={guild.id}")
    if not cursor.fetchone():
        ...
    else:
        cursor.execute(f"DELETE from servers WHERE guild_id='{guild.id}'")
    c.commit()
    c.close()
    """

"""    @commands.command()
    @commands.cooldown(rate=1, per=1)
    async def links(self, ctx):
        embed=discord.Embed(description="Links for Sniper", color=0xfdfdfd)
        embed.set_author(name="Links")
        embed.add_field(name="Invite Links", value="[Manage Messages](https://discord.com/api/oauth2/authorize?client_id=742784763206828032&permissions=8192&scope=bot)\n[Administrator](https://discord.com/api/oauth2/authorize?client_id=742784763206828032&permissions=8&scope=bot)")
        embed.add_field(name="Notice", value="You need the permission `Manage Server` to invite bots to your server!")
        embed.add_field(name="Misc.", value="[Top.gg](https://top.gg/bot/742784763206828032)", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=1)
    async def vote(self, ctx):
        embed=discord.Embed(description="Thanks for voting! Your vote helps Sniper get better recognized by the community!", color=0xfdfdfd)
        embed.set_author(name="Vote")
        embed.add_field(name="Direct Link", value="https://top.gg/bot/742784763206828032/vote")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=1)
    async def stats(self, ctx):
        c = sqlite3.connect("files/stats.db")
        cursor = c.cursor()
        
        embed=discord.Embed(description=f"Current Stats for Sniper", color=0xfdfdfd)
        embed.set_author(name=f"Stats")

        embed.add_field(name=f"Total Server Count: `{len(self.bot.guilds)}`", value=f"Current server count for Sniper")
        embed.add_field(name=f"Total Users: `{sum([len(guild.members) for guild in self.bot.guilds])}`", value=f"Current user count for Sniper", inline=False) # Fix Total Users
        embed.add_field(name=f"Uptime: `{convert(getUptime())}`", value=f"Current uptime for Sniper (hh:mm:ss)", inline=False)
        embed.add_field(name=f"Library: `Discord.py (DPY)`", value=f"Library used for Sniper", inline=False)
        embed.add_field(name=f"Developer: `xIntensity#4818`", value=f"Developer",)

        await ctx.send(embed=embed)"""

"""
@commands.has_permissions(manage_guild=True)
@client.command()
async def editchannel(ctx, arg=None, channel_id=None):

    connect = sqlite3.connect("files/edit_log.db")
    cursor = connect.cursor()

    if not arg:
        await ctx.send(embed=error_embed("`<argument>` not specified.", "Please specify what you wish to do with `$editchannel`\nTyping `$help editchannel` will give you a list of `$editchannel` usages."))
    
    else:
        if arg == "-u":
            cursor.execute(f"SELECT EXISTS(SELECT 1 FROM servers WHERE guild_id='{ctx.guild.id}')")

            if cursor.fetchone()[0] == 0:
                await ctx.send(embed=error_embed("This action could not be completed.", "Your server does not have a specified channel to log edited messages!"))

            else:
                try:
                    c = client.get_channel(int(channel_id))
                    if c == None:
                        await ctx.send(embed=error_embed("Invalid channel ID", "The `<channel_id>` you have entered is not valid."))

                    else:
                        cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                        if cursor.fetchone()[0] == int(channel_id):

                            await ctx.send(embed=error_embed("Channel already logging.", "The channel ID you have enter is already being used as a edited-message logger."))

                        else:
                            if str(client.get_channel(int(channel_id)).guild) != str((client.get_guild(ctx.guild.id)).name):
                                await ctx.send(embed=error_embed(f"Invalid channel ID `({channel_id})`", "Please enter a channel ID __within__ the server.\nChannels from other servers cannot be used."))

                            else:
                                cursor.execute(f"UPDATE servers SET channel_id={channel_id} WHERE guild_id={ctx.guild.id}")
                                await ctx.send(embed=success_embed("Action has been completed successfully!", f"All edited messages in `{ctx.guild.name}` are logged in {client.get_channel(int(channel_id)).mention}"))
                                connect.commit()

                except ValueError:
                    await ctx.send(embed=error_embed("Incorrect data type","`<channel_id>` only accepts number data types! (You can't enter words)"))

        elif arg == "-s":
            cursor.execute(f"SELECT EXISTS(SELECT 1 FROM servers WHERE guild_id='{ctx.guild.id}')")

            if cursor.fetchone()[0] == 0:
                await ctx.send(embed=error_embed("This action could not be completed.", "Your server does not have a specified channel to log edited messages!"))

            else:
                cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                channel = client.get_channel(cursor.fetchone()[0])
                cursor.execute(f"DELETE from servers WHERE guild_id='{ctx.guild.id}'")
                connect.commit()
                server = client.get_guild(ctx.guild.id)
                await ctx.send(embed=success_embed("Action has been completed successfully!", f"Edited messages no longer logged for `{server}`\nEdited messages no longer yielded in {channel.mention}"))

        elif arg == "-a":
            cursor.execute(f"SELECT * FROM servers WHERE guild_id={ctx.guild.id}")

            if not cursor.fetchone():
                try:
                    c = client.get_channel(int(channel_id))
                    if c == None:
                        await ctx.send(embed=error_embed("Invalid channel ID","The `<channel_id>` you have entered is not valid."))
                        
                    else:
                        if str(client.get_channel(int(channel_id)).guild) != str((client.get_guild(ctx.guild.id)).name):
                            await ctx.send(embed=error_embed(f"Invalid channel ID `({channel_id})`","Please enter a channel ID __within__ the server.\nChannels from other servers cannot be used."))

                        else:
                            cursor.execute(f"INSERT INTO servers VALUES ({ctx.guild.id}, {channel_id})")
                            await ctx.send(embed=success_embed("Action has been completed successfully!",f"All edited messages in `{ctx.guild.name}` are logged in {client.get_channel(int(channel_id)).mention}"))
                            connect.commit()

                except ValueError:
                        await ctx.send(embed=error_embed("Incorrect data type.","`<channel_id>` only accepts number data types! (You can't enter words)"))

            else:
                cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                channel = client.get_channel(cursor.fetchone()[0])
                await ctx.send(embed=error_embed("Existing Logging Channel",f"{channel.mention} has already been set for the edited-message logger.\nYou can update it with `$editchannel -u <channel_id>`"))

            connect.close()



@commands.has_permissions(manage_guild=True)
@client.command()
async def delchannel(ctx, arg=None, channel_id=None):

    connect = sqlite3.connect("files/message_log.db")
    cursor = connect.cursor()

    if not arg:
        await ctx.send(embed=error_embed("`<argument>` not specified.","Please specify what you wish to do with `$delchannel`\nTyping `$help delchannel` will give you a list of `$delchannel` usages."))
    
    else:
        if arg == "-u":
            cursor.execute(f"SELECT EXISTS(SELECT 1 FROM servers WHERE guild_id='{ctx.guild.id}')")

            if cursor.fetchone()[0] == 0:
                await ctx.send(embed=error_embed("No specified channel!","Your server does not have a specified channel to log deleted messages!"))

            else:
                try:
                    c = client.get_channel(int(channel_id))
                    if c == None:
                        await ctx.send(embed=error_embed("Invalid channel ID","The `<channel_id>` you have entered is not valid"))
                    
                    else:
                        cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                        if cursor.fetchone()[0] == int(channel_id):
                            await ctx.send(embed=error_embed("Channel already logging.","The channel ID you have enter is already being used as a deleted-message logger."))
                        
                        else:
                            if str(client.get_channel(int(channel_id)).guild) != str((client.get_guild(ctx.guild.id)).name):
                                await ctx.send(embed=error_embed(f"Invalid channel ID `({channel_id})`", "Please enter a channel ID __within__ the server.\nChannels from other servers cannot be used."))

                            else:
                                cursor.execute(f"UPDATE servers SET channel_id={channel_id} WHERE guild_id={ctx.guild.id}")
                                await ctx.send(embed=success_embed("Action has been completed successfully!",f"All deleted messages in `{ctx.guild.name}` are logged in {client.get_channel(int(channel_id)).mention}"))
                                connect.commit()

                except ValueError:
                        await ctx.send(embed=error_embed("Incorrect data type.","`<channel_id>` only accepts number data types! (You can't enter words)"))

        elif arg == "-s":
            cursor.execute(f"SELECT EXISTS(SELECT 1 FROM servers WHERE guild_id='{ctx.guild.id}')")

            if cursor.fetchone()[0] == 0:
                await ctx.send(embed=error_embed("No specified channel!","Your server does not have a specified channel to log deleted messages!"))

            else:
                cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                channel = client.get_channel(cursor.fetchone()[0])
                cursor.execute(f"DELETE from servers WHERE guild_id='{ctx.guild.id}'")
                connect.commit()
                server = client.get_guild(ctx.guild.id)
                await ctx.send(embed=success_embed("Action has been completed successfully!",f"Deleted messages no longer logged for `{server}`\nDeleted messages no longer yielded in {channel.mention}"))

        elif arg == "-a":
            cursor.execute(f"SELECT * FROM servers WHERE guild_id={ctx.guild.id}")

            if not cursor.fetchone():
                try:
                    c = client.get_channel(int(channel_id))
                    if c == None:
                        await ctx.send(embed=error_embed("Invalid channel ID","The `<channel_id>` you have entered is not valid."))

                    else:
                        if str(client.get_channel(int(channel_id)).guild) != str((client.get_guild(ctx.guild.id)).name):
                            await ctx.send(embed=error_embed(f"Invalid channel ID `({channel_id})`","Please enter a channel ID __within__ the server.\nChannels from other servers cannot be used."))

                        else:
                            cursor.execute(f"INSERT INTO servers VALUES ({ctx.guild.id}, {channel_id})")
                            await ctx.send(embed=success_embed("Action has been completed successfully!",f"All deleted messages in `{ctx.guild.name}` are logged in {client.get_channel(int(channel_id)).mention}"))
                            connect.commit()

                except ValueError:
                        await ctx.send(embed=error_embed("Incorrect data type.","`<channel_id>` only accepts number data types! (You can't enter words)"))

            else:
                cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                channel = client.get_channel(cursor.fetchone()[0])
                await ctx.send(embed=error_embed("Existing Logging Channel",f"{channel.mention} has already been set for the deleted-message logger.\nYou can update it with `$delchannel -u <channel_id>`"))

            connect.close()

        else:
            ...
"""

"""
SLASH
slash = SlashCommand(client, sync_commands=True)
"""

"""
 try:
                                for i in checklist:
                                    for x in range(len(beforemsg[ctx.guild.id][i])):
                                        textchannel = self.bot.get_channel(i)
                                        w.write(f"\n\nBefore: {beforemsg[ctx.guild.id][i][x].content}\nAfter: {aftermsg[ctx.guild.id][i][x].content}\nEdited by {beforemsg[ctx.guild.id][i][x].author} in #{textchannel}")
"""
"""
    @commands.command()
    @commands.cooldown(rate=1,per=60)
    async def permissions(self, ctx, arg=None, value=None): 
        if not arg: 
            embed=discord.Embed(color=0xfdfdfd) # work on the embed
        elif arg in ["snipe","log","prefix"]:
            if not value:
                error_embed("Enter a role",f"No permission was provided for {arg}")
            elif value in ["@n","@ms","@mm"]:
                
            else:
                error_embed("Invalid choice",f"`{value}` is not part of the valid permissions, `None (@n)`, `Manage Messages (@mm)`, and `Manage Server(@ms)`")
        else: 
            error_embed("Invalid choice",f"`{arg}` is not part of the valid choices, `snipe`, `log`, and `prefix`")
            """

# all dict() directiories for beforemsg/aftermsg
 #[ctx.guild.id] returns [{channel:[msg,msg1]},{channel2:[msg,msg1]}]
                    #[ctx.guild.id][x] assuming x = range(len()) of [ctx.guild.id] ]returns selected channel, reroutes to exception if there is no channel id
                    #[ctx.guild.id][x][i] assuming i = channelid list returns a list of stored messages for the channel
                    #[ctx.guild.id][x][i][z] returns a certain message
                    #exceptions cannot be toggled