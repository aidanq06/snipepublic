import discord
import json
from discord.ext import commands
import sys
import sqlite3
import traceback

def error_embed(description, error):
    embed=discord.Embed(description=description, color=0xfdfdfd)
    embed.set_author(name="Error", icon_url="https://cdn.discordapp.com/attachments/642491399790395397/743516486005424268/clipart1203855.png")
    embed.add_field(name="What happened?", value=error)
    return embed

def success_embed(description, completed):
    embed=discord.Embed(description=description, color=0xfdfdfd)
    embed.set_author(name="Success", icon_url="https://cdn.discordapp.com/attachments/742833913751142402/743524321376338051/pngwing.com.png")
    embed.add_field(name="Action Completed:", value=completed)
    return embed

no_dm = error_embed("Direct Messages","Sniper can't be used in DMs! (This is because most of Sniper's commands are server-based!)")

error_embed("Direct Messages","Sniper can't be used in DMs! (This is because most of Sniper's commands are server-based!)")

def getprefix(client, message):
    
    with open('files/json/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    try:
        return prefixes[str(message.guild.id)]
    except: # This is to ignore private messages
        return "$" 

client = commands.Bot(command_prefix=getprefix)

@client.event
async def on_ready():
    guildlist = []
    for i in client.guilds:
        guildlist.append(i.id)
    with open("files/json/prefixes.json", "r") as readList:
        guildprefixes = json.load(readList)
        for x in guildlist:
            try:
                guildprefixes[f"{x}"]
            except KeyError:
                guildprefixes[f"{x}"] = "$"

    with open("files/json/prefixes.json", "w") as writeList:
        json.dump(guildprefixes, writeList, indent=4)

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"$snipe | $help"))

    cogs = ['plugins.snipe', 'plugins.help','plugins.misc','plugins.error'] # ,'plugins.topAPI','plugins.error'

    for cog in cogs:
        try:
            client.load_extension(cog)
        except Exception:
            print(cog, file=sys.stderr)
            traceback.print_exc()

    print("Connected")

class Events(commands.Cog, name="Events"):

    @client.event
    async def on_message(message):
        try:
            if client.user.mentioned_in(message):
                with open("files/json/prefixes.json", "r") as readList:
                    guildprefixes = json.load(readList)
                    if not guildprefixes[f"{message.guild.id}"]: # if guildprfixes
                        guildprefixes[f"{message.guild.id}"] = "$"
                        embed=success_embed("Sniper prefix set", "Your current server's prefix is set to `$`")
                    else:
                        embed=success_embed("Sniper prefix", f"The prefix set for your server is set to: `"+ guildprefixes[f"{message.guild.id}"] + "` Use this to execute commands.")

                await message.channel.send(embed=embed)

            await client.process_commands(message)
        except AttributeError: # Ignores pings
            pass

    @client.event
    async def on_guild_add(guild):
        with open("files/json/prefixes.json", "r") as readList:
            guildprefixes = json.load(readList)

        guildprefixes[guild.id] = "$"
        with open("files/json/prefixes.json", "w") as writeList:
            json.dump(guildprefixes, writeList, indent=4)

    client.help_command = None

    @client.event
    async def on_message_edit(before, after):
        if before.author.bot is False:
            if len(before.content) == 0 and len(after.content) == 0: # Filter out other events
                pass
            else:
                connect = sqlite3.connect("files/database/edit_log.db")

                cursor = connect.cursor()

                cursor.execute(f"SELECT * FROM servers WHERE guild_id={after.guild.id}")
                if not cursor.fetchone():
                    pass
                else:
                    cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={after.guild.id}")

                    channel = client.get_channel(cursor.fetchone()[0])
                    c = client.get_channel(before.channel.id)
                    embed=discord.Embed(description=f"A message was edited in {c.mention}", color=0xfdfdfd)
                    embed.set_author(name="Edited Message", icon_url=before.author.avatar_url)
                    embed.add_field(name="Before", value=before.content)
                    embed.add_field(name="After", value=after.content)
                    embed.add_field(name="Message ID", value=f"`{after.id}`", inline=False)
                    embed.add_field(name="Author", value=before.author)
                    await channel.send(embed=embed)

        else:
            pass

    @client.event
    async def on_message_delete(message):
        if message.author.bot is False:
            connect = sqlite3.connect("files/database/message_log.db")

            cursor = connect.cursor()

            cursor.execute(f"SELECT * FROM servers WHERE guild_id={message.guild.id}")
            if not cursor.fetchone():
                pass
            else:
                cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={message.guild.id}")

                channel = client.get_channel(cursor.fetchone()[0])
                c = client.get_channel(message.channel.id)
                embed=discord.Embed(description=f"A message was deleted in {c.mention}", color=0xfdfdfd)
                if len(message.content) == 0:
                    embed.add_field(name = f"Message ", value=f"(No message was provided)")
                else:
                    embed.add_field(name = f"Message ", value=f"{message.content}")
                embed.set_author(name="Deleted Message", icon_url=message.author.avatar_url)
                embed.add_field(name="Message ID", value=f"`{message.id}`", inline=False)
                embed.add_field(name="Author", value=message.author, inline=False)

                if message.attachments:
                    embed.add_field(name='Attachment(s)', value='\n'.join([attachment.filename for attachment in message.attachments]) + "\n\n*Images and files __cannot__ be recovered after being deleted!*")
                await channel.send(embed=embed)
        else:
            pass

"""    @client.event # For log command
    async def on_command_error(ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
            await ctx.send(embed=error_embed("Can't send log","The log can't be sent to your DMs! You have either blocked Sniper or disallowed DMs from server members. (If logs were sent in the server, everyone would be able to see it!)"))
        #if isinstance(error, discord.ext.commands.errors.HTTPException):
            #watch out may cause error"""

@commands.has_permissions(manage_guild=True)
@client.command(aliases=["as"])
@commands.cooldown(1, 5, commands.BucketType.user)
async def autosnipe(ctx, arg=None, action=None, channel: discord.TextChannel=None):
    with open("files/json/prefixes.json", "r") as f:
            content = json.load(f)

    if not arg:
        embed=discord.Embed(description=f"`{content[f'{ctx.guild.id}']}autosnipe [arg] [action] <channel>`", color=0xfdfdfd)
        embed.set_author(name="Autosnipe")
        embed.add_field(name=f"What is `{content[f'{ctx.guild.id}']}autosnipe`?", value=f"`{content[f'{ctx.guild.id}']}autosnipe` is a utility command that automatically snipes messages to a specified, whether it be deleted messages or edited messages, that is up to the user.")
        embed.add_field(name="`[arg]`", value="In this argument, you would specify whether you want to autosnipe edited messages or deleted messages. Type `-d` for deleting or `-e` for editing.", inline=True)
        embed.add_field(name="`[action]`", value="After selecting whether you want to autosnipe edited or deleted messages, you would specify in this argument, what action you would want to do. You can either set a new channel to log the messages in, `-a`, update an existing channel, `-u`, or stop logging messages all together, `-s`.", inline=False)
        embed.add_field(name="`<channel>`", value="This argument is only required for users wanting to set a new channel, `-a`, or update an existing channel, `-u` In here, you specify the channel you want to set by typing `#channel` Note that if Sniper doesn't have access to the channel, Sniper will __not__ be able to autosnipe.", inline=False)
        embed.add_field(name="Examples", value=f"`{content[f'{ctx.guild.id}']}autosnipe -d -a #deletes` would log all deleted messages into `#deletes`\n`{content[f'{ctx.guild.id}']}autosnipe -e -u #edits` would change the existing channel that is logging edits to `#edits`",inline=False)
        embed.add_field(name=f"Extra Info", value=f"**Other Names** >> `{content[f'{ctx.guild.id}']}as`\n**Permissions Required** >> `Manage Server` / `Manage Guild`\n**Usage Cooldown** >> 10 seconds",inline=False)
        await ctx.send(embed=embed)
    else:
        try:
            if not arg in ["-e","-d"]:
                await ctx.send(embed=error_embed("Invalid action",f"`{arg}` is an invalid choice! (Case Sensitive!) Type `{content[f'{ctx.guild.id}']}autosnipe` to refer to the possible usages for autosnipe!"))
            else:
                if not action in ["-a","-u","-s"]:
                    await ctx.send(embed=error_embed("Invalid action",f"`{action}` is an invalid choice! (Case Sensitive!) Type `{content[f'{ctx.guild.id}']}autosnipe` to refer to the possible usages for autosnipe!"))
                else:
                    connect = sqlite3.connect("files/database/message_log.db")
                    cursor = connect.cursor()

                    connect2 = sqlite3.connect("files/database/edit_log.db")
                    cursor2 = connect2.cursor()

                    # Stop logging deletes
                    if action.lower() == "-s" and arg.lower() == "-d":
                        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM servers WHERE guild_id='{ctx.guild.id}')")

                        if cursor.fetchone()[0] == 0:
                            await ctx.send(embed=error_embed("No specified channel!","Your server doesn't have a specified autosniping channel yet! (For deleted messages)"))

                        else:
                            cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                            channel = client.get_channel(cursor.fetchone()[0])
                            cursor.execute(f"DELETE from servers WHERE guild_id='{ctx.guild.id}'")
                            connect.commit()
                            server = client.get_guild(ctx.guild.id)
                            await ctx.send(embed=success_embed("Action has been completed successfully!",f"Deleted messages are no longer autosniped into {channel}!"))

                    # Add a channel to log deletes
                    if action.lower() == "-a" and arg.lower() == "-d":
                        cursor.execute(f"SELECT * FROM servers WHERE guild_id={ctx.guild.id}")

                        if not cursor.fetchone():
                            cursor.execute(f"INSERT INTO servers VALUES ({ctx.guild.id}, {channel.id})")
                            await ctx.send(embed=success_embed("Action has been completed successfully!",f"All deleted messages in `{ctx.guild.name}` are logged in {channel}"))
                            connect.commit()

                        else:
                            cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                            channel = client.get_channel(cursor.fetchone()[0])
                            await ctx.send(embed=error_embed("Existing Logging Channel",f"{channel.mention} has already been set for the deleted-message logger.\nYou can update it with `$delchannel -u <channel_id>`"))

                    # Update a channel to log deletes
                    if action.lower() == "-u" and arg.lower() == "-d":
                        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM servers WHERE guild_id='{ctx.guild.id}')")

                        if cursor.fetchone()[0] == 0:
                            await ctx.send(embed=error_embed("No specified channel!","Your server does not have a specified channel to log deleted messages!"))

                        else:
                            cursor.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                            if cursor.fetchone()[0] == channel.id:
                                await ctx.send(embed=error_embed("Channel already logging.","The channel ID you have enter is already being used as a deleted-message logger."))

                            else:
                                cursor.execute(f"UPDATE servers SET channel_id={channel.id} WHERE guild_id={ctx.guild.id}")
                                await ctx.send(embed=success_embed("Action has been completed successfully!",f"All deleted messages in `{ctx.guild.name}` are logged in {channel.mention}"))
                                connect.commit()

                    # EDITS BELOW

                    # Stop logging edits
                    if action.lower() == "-s" and arg.lower() == "-e":
                        cursor2.execute(f"SELECT EXISTS(SELECT 1 FROM servers WHERE guild_id='{ctx.guild.id}')")

                        if cursor2.fetchone()[0] == 0:
                            await ctx.send(embed=error_embed("No channel.", "Your server doesn't have a channel to autosnipe edits in."))

                        else:
                            cursor2.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                            channel = client.get_channel(cursor2.fetchone()[0])
                            cursor2.execute(f"DELETE from servers WHERE guild_id='{ctx.guild.id}'")
                            connect2.commit()
                            server = client.get_guild(ctx.guild.id)
                            await ctx.send(embed=success_embed("Autosnipe channel removed!", f"Edited messages are no longer autosniped into {channel.mention}!"))

                    # Add a channel to log edits
                    if action.lower() == "-a" and arg.lower() == "-e":
                        cursor2.execute(f"SELECT * FROM servers WHERE guild_id={ctx.guild.id}")

                        if not cursor2.fetchone():
                            cursor2.execute(f"INSERT INTO servers VALUES ({ctx.guild.id}, {channel.id})")
                            await ctx.send(embed=success_embed("Action has been completed successfully!",f"All edited messages in `{ctx.guild.name}` are logged in {client.get_channel(int(channel.id)).mention}"))
                            connect2.commit()

                        else:
                            cursor2.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                            channel = client.get_channel(cursor2.fetchone()[0])
                            await ctx.send(embed=error_embed("Existing Logging Channel",f"{channel.mention} has already been set for the edited-message logger.\nYou can update it with `$editchannel -u <channel_id>`"))

                    # Update a channel to log edits
                    if action.lower() == "-u" and arg.lower() == "-e":
                        cursor2.execute(f"SELECT EXISTS(SELECT 1 FROM servers WHERE guild_id='{ctx.guild.id}')")

                        if cursor2.fetchone()[0] == 0:
                            await ctx.send(embed=error_embed("This action could not be completed.", "Your server does not have a specified channel to log edited messages!"))

                        else:
                            cursor2.execute(f"SELECT channel_id FROM servers WHERE guild_id={ctx.guild.id}")
                            if cursor2.fetchone()[0] == channel.id:
                                await ctx.send(embed=error_embed("Channel already logging.", "The channel ID you have enter is already being used as a edited-message logger."))

                            else:
                                cursor2.execute(f"UPDATE servers SET channel_id={channel.id} WHERE guild_id={ctx.guild.id}")
                                await ctx.send(embed=success_embed("Action has been completed successfully!", f"All edited messages in `{ctx.guild.name}` are logged in {channel.mention}!"))
                                connect2.commit()

        except AttributeError:
            pass


if __name__ == '__main__':
    with open("files/json/token.json", "r") as f:
        client.run(json.load(f))
