import discord
from discord.ext import commands
from Bot import error_embed, no_dm
import json


class Help(commands.Cog, name='Help'):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='help', invoke_without_command=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def help(self, ctx, command=None):
        try:
            with open("files/json/prefixes.json","r") as f:
                prefixlist = json.load(f)
            
            p = prefixlist[f"{ctx.guild.id}"]

            if not command:
                embed=discord.Embed(description=f"To get an in-depth description of each command, type `{p}help <command>`\nArguments that are wrapped with `[ ]` means that they are required.", color=0xfdfdfd)
                embed.set_author(name="Help")
                embed.add_field(name="Snipe Commands", value=f"`{p}multisnipe`\n`{p}usersnipe <user>`\n`{p}snipe <channel>`\n`{p}editsnipe <channel>`")
                embed.add_field(name="Utility Commands", value=f"`{p}log`\n`{p}autosnipe [arg] [action] <channel>`")
                embed.add_field(name="Misc. Commands", value=f"`{p}info`\n`{p}prefix`")
            elif command == "snipe":
                embed=discord.Embed(description=f"`{p}snipe <channel>`", color=0xfdfdfd)
                embed.set_author(name=f"Snipe")
                embed.add_field(name=f"What is `{p}snipe`?", value=f"`{p}snipe` is a utility command that retrieves the message the was deleted most recently. (Excluding Bot Messages)")
                embed.add_field(name=f"`<channel>`", value="This argument allows you to specify a desired channel to snipe in. It is not required; if not specified, it will return a deleted message from the current channel.")
                embed.add_field(name=f"Extra Info", value=f"**Other Names** >> `{p}s` / `{p}sniper` / `{p}sniped`\n**Permissions Required** >> None\n**Usage Cooldown** >> 5 seconds",inline=False)
            elif command == "multisnipe":
                embed=discord.Embed(description=f"`{p}multisnipe`", color=0xfdfdfd)
                embed.set_author(name=f"Multisnipe")
                embed.add_field(name=f"What is `{p}multisnipe`?", value=f"`{p}multisnipe` is a utility command working similar to `{p}snipe` but instead, sniping 5. If there are less than 5 messages that have been deleted, then Sniper will snipe __all__ the messages.  (Excluding Bot Messages)")
                embed.add_field(name=f"Extra Info", value=f"**Other Names** >> `{p}m` / `{p}multi` / `{p}msnipe`\n**Permissions Required** >> None\n**Usage Cooldown** >> 5 seconds",inline=False)
            elif command == "editsnipe":
                embed=discord.Embed(description=f"`{p}editsnipe <channel>`", color=0xfdfdfd)
                embed.set_author(name=f"Editsnipe")
                embed.add_field(name=f"What is `{p}editsnipe`?", value=f"`{p}editsnipe` is a utility command that retrieves the message the was edited most recently. (Will not retrieve edited bot messages.)")
                embed.add_field(name="`<channel>`", value=f"This argument allows you to specify a desired channel to editsnipe in. It is not required; if not specified, it will return an edit from the current channel.")
                embed.add_field(name=f"Extra Info", value=f"**Other Names** >> `{p}e` / `{p}esnipe` / `{p}edited`\n**Permissions Required** >> None\n**Usage Cooldown** >> 5 seconds",inline=False)
            elif command == "usersnipe":
                embed=discord.Embed(description=f"`{p}usersnipe [user]`", color=0xfdfdfd)
                embed.set_author(name=f"Usersnipe")
                embed.add_field(name=f"What is `{p}usersnipe`?", value=f"`{p}usersnipe` is a utility command that retrieves the most recent deleted message from the targeted user.")
                embed.add_field(name="`<user>`", value=f"In this argument, you specify what user you want to snipe by either pinging them or typing out their full username. (@User#1234 or User#1234) If it is left unspecified, then it will snipe a message from the requester.")
                embed.add_field(name=f"Extra Info", value=f"**Other Names** >> `{p}snipeuser` / `{p}usnipe` / `{p}u`\n**Permissions Required** >> None\n**Usage Cooldown** >> 5 seconds",inline=False)
            elif command == "autosnipe":
                embed=discord.Embed(description=f"`{p}autosnipe [arg] [action] <channel>`", color=0xfdfdfd)
                embed.set_author(name="Autosnipe")
                embed.add_field(name=f"What is `{p}autosnipe`?", value=f"{p}autosnipe is a utility command that automatically snipes messages to a specified, whether it be deleted messages or edited messages, that is up to the user.")
                embed.add_field(name="`[arg]`", value="In this argument, you would specify whether you want to autosnipe edited messages or deleted messages. Type `-d` for deleting or `-e` for editing.", inline=True)
                embed.add_field(name="`[action]`", value="After selecting whether you want to autosnipe edited or deleted messages, you would specify in this argument, what action you would want to do. You can either set a new channel to log the messages in, `-a`, update an existing channel, `-u`, or stop logging messages all together, `-s`.", inline=False)
                embed.add_field(name="`<channel>`", value="This argument is only required for users wanting to set a new channel, `-a`, or update an existing channel, `-u` In here, you specify the channel you want to set by typing `#channel` Note that if Sniper doesn't have access to the channel, Sniper will __not__ be able to autosnipe.", inline=False)
                embed.add_field(name="Examples", value=f"`{p}autosnipe -d -a #deletes` would log all deleted messages into `#deletes`\n`{p}autosnipe -e -u #edits` would change the existing channel that is logging edits to `#edits`",inline=False)
                embed.add_field(name=f"Extra Info", value=f"**Other Names** >> `{p}as`\n**Permissions Required** >> `Manage Server` / `Manage Guild`\n**Usage Cooldown** >> 5 seconds",inline=False)
            elif command == "info":
                embed=discord.Embed(description=f"`{p}info`", color=0xfdfdfd)
                embed.set_author(name=f"Permission required: None")
                embed.add_field(name=f"What is `{p}info`?", value=f"`{p}info` returns an embed with all links relating to Sniper. You can find the current server count, when Sniper was last updated, invite links, etc.")
                embed.add_field(name=f"Extra Info", value="**Other Names** >> None\n**Permissions Required** >> None\n**Usage Cooldown** >> 1 second",inline=False)
            elif command == "log":
                embed=discord.Embed(description=f"`{p}log`",color=0xfdfdfd)
                embed.set_author(name=f"Log")  
                embed.add_field(name=f"What is `{p}log`?", value=f"`{p}log` is a utility command that retrives a direct log of all deletes, and all edits (excluding other bot messages or edits) of a server. Once completed, Sniper will DM the requester a complete log of the server. Any messages before Sniper has been added or reloaded will __not__ be logged.")
                embed.add_field(name="Regarding Direct Messaging", value=f"{p}log is restricted to users that have the permission `Manage Messages` or higher. This is to prevent everyone having the ability retrieve logs. For the same purpose, Sniper will direct message you the log so that others cannot access the file, only the requester. Do note that you __must__ have the option **Allow direct messages from server members** (You can do this under the server privacy setting) turned on for this command to work!")
                embed.add_field(name=f"Extra Info", value="**Other Names** >> None\n**Permissions Required** >> `Manage Messages`\n**Usage Cooldown** >> 15 seconds",inline=False)
            elif command == "prefix":
                embed=discord.Embed(description=f"Permission Required: `Guild Manager` | Aliases: {p}updateprefix, {p}changeprefix",color=0xfdfdfd)
                embed.set_author(name=f"Prefix")  
                embed.add_field(name=f"What is `{p}prefix`?", value=f"`{p}prefix` is a setting-related command that allows server managers/admins to change the prefix for Sniper. This is relative to each guild.")
                embed.add_field(name="`[customprefix]`", value=f"In this argument, you can specify what prefix you want as long as it is under __10__ characters.")
                embed.add_field(name="Forget your prefix?", value=f"In the case of losing or forgetting your prefix, you can always **ping** Sniper to get the current prefix.")
                embed.add_field(name=f"Extra Info", value=f"**Other Names** >> `{p}changeprefix` / `{p}updateprefix`\n**Permissions Required** >> `Manage Guild` / `Manage Server`\n**Usage Cooldown** >> 10 seconds",inline=False)
            else:
                embed=error_embed("Invalid Command",f"`{command}` isn't a valid command.")
            try:
                await ctx.send(embed=embed)
            except NameError:
                pass
        except AttributeError:
            await ctx.send(embed=no_dm)

def setup(bot):
    bot.add_cog(Help(bot))
    print("Help has been loaded.")
