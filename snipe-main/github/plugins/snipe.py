import datetime
import sqlite3
import time
import os
from os import linesep
import io

import discord
from Bot import error_embed, success_embed, no_dm
from discord.ext import commands

# Snipe
channels = {}
# Editsnipe
beforemsg = {}
aftermsg = {}
# Usersnipe
users = {}
# Multisnipe
multi = {}
times = {}

error_png = "https://cdn.discordapp.com/attachments/642491399790395397/743516486005424268/clipart1203855.png"

class Snipe(commands.Cog, name='Snipe'):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild and not message.author.bot:
            try:
                channels[message.guild.id][message.channel.id] = message
                users[message.author.id][message.guild.id] = message
            
                if len(multi[message.guild.id]) == 10: # This is a mess
                    multi[message.guild.id].remove(multi[message.guild.id][0])
                    multi[message.guild.id].append(message)
                    times[message.guild.id].remove(times[message.guild.id][0])
                    times[message.guild.id].append(message.created_at.utcnow().timestamp())
                else:
                    multi[message.guild.id].append(message)
                    times[message.guild.id].append(message.created_at.utcnow().timestamp())
            except KeyError:
                channels[message.guild.id] = {message.channel.id: message}
                users[message.author.id] = {message.guild.id: message}
                multi[message.guild.id] = [message]
                times[message.guild.id] = [message.created_at.utcnow().timestamp()]

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot is False: 
            try:
                loadedlist = []
                for i in range(len(beforemsg[before.guild.id])):
                    loadedlist.append(str(beforemsg[before.guild.id][i]))

                if before.channel.id not in loadedlist:
                    beforemsg[before.guild.id].append({before.channel.id:[before]})
                    aftermsg[after.guild.id].append({after.channel.id:[after]})
                else:
                    int=0
                    for i in beforemsg[before.guild.id]:
                        if str(i).startswith("{"+f"{before.channel.id}"):
                            if before not in beforemsg[before.guild.id][int][before.channel.id]:
                                if before.content != after.content: #prevents embeds counting as edits
                                    beforemsg[before.guild.id][int][before.channel.id].append(before)
                                    aftermsg[after.guild.id][int][after.channel.id].append(after)
                                    break
                                
                        else:
                            int+=1

            except KeyError:
                beforemsg[before.guild.id] = [{before.channel.id:[before]}]
                aftermsg[after.guild.id] = [{after.channel.id:[after]}]

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def log(self, ctx):
        sender=f"Log for {ctx.guild.name} \nServer ID: {ctx.guild.id}\nLog was requested by {ctx.author}\n\n>> Deleted Messages"    
        #Note that all messages deleted OR edited before Sniper was added/reloaded cannot be logged.
        # on {datetime.datetime.now().strftime('%m/%d/%Y - %I:%M %p UTC')}

        try:
            for i in range(len(multi[ctx.guild.id])):
                msg = multi[ctx.guild.id][i]
                if not msg.content:
                    sender=sender+f"\n\nMessage: (No Message Provided)\nDeleted by {multi[ctx.guild.id][i].author} at {multi[ctx.guild.id][i].created_at.strftime('%I:%M %p UTC, %m/%d')}"
                    sender=sender+f"\nAttachment: {([attachment.filename for attachment in msg.attachments][0])}"
                else:
                    sender=sender+f"\n\nMessage: {multi[ctx.guild.id][i].content}\nDeleted by {multi[ctx.guild.id][i].author} at {multi[ctx.guild.id][i].created_at.strftime('%I:%M %p UTC, %m/%d')}"
                    try:
                        sender=sender+f"\nAttachment: {([attachment.filename for attachment in msg.attachments][0])}"
                    except IndexError:
                        pass
        except KeyError:
            sender=sender+f"\n\nNo messages have been logged."

        sender=sender+"\n\n>> Edited Messages"


        try:
            for i in beforemsg[ctx.guild.id]:  # {123:["msg"]}
                for x in beforemsg[ctx.guild.id][beforemsg[ctx.guild.id].index(i)]:
                    blist = beforemsg[ctx.guild.id][beforemsg[ctx.guild.id].index(i)][x]
                    for bmsg in blist:
                        textchannel= self.bot.get_channel(x)
                        counter = blist.index(bmsg)

                        sender=sender+f"\n\nBefore: {bmsg.content}\nAfter: {aftermsg[ctx.guild.id][aftermsg[ctx.guild.id].index(i)][x][counter].content}"
                        sender=sender+f"\nEdited by {bmsg.author} in #{textchannel}"
                
        except KeyError:
            sender=sender+(f"\n\nNo edits have been logged.")
   
        f = io.StringIO(sender)
        try:
            await ctx.author.send(file=discord.File(fp=f, filename="log.txt"))
            await ctx.send(embed=success_embed("Sent!","The server log has been sent. Check your DMs!"))
        except:
            await ctx.send(embed=error_embed("Can't send log","The log can't be sent to your DMs! You have either blocked Sniper or disallowed DMs from server members. (If logs were sent in the server, everyone would be able to see it!)"))

    
    @commands.command(aliases=['msnipe','multi','m'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def multisnipe(self, ctx):
        try:
            amount = 5
            try:
                embed=discord.Embed(description=f"`<User> <Time>`", color=0xfdfdfd)
                embed.set_author(name="Multisnipe")
                try:
                    for i in range(amount):
                        
                        multi[ctx.guild.id].reverse()
                        times[ctx.guild.id].reverse()
                        sniped=multi[ctx.guild.id][i]
                        d = times[ctx.guild.id][i]

                        t1 = datetime.datetime.utcnow()
                        t = t1.timestamp()
                        factor = round(t-d)

                        if factor > 60:
                            m = round(factor/60,1)
                            txt = f"{m} minute(s)" 
                        
                        elif factor > 3600:
                            h = round(factor/3600,1)
                            txt = f"{h} hour(s)"
                        
                        else:
                            s = round(factor,1)
                            txt = f"{s} second(s)"

                        embed.add_field(name=f"{sniped.author} - {txt} ago", value=sniped.content, inline=False)

                        multi[ctx.guild.id].reverse()
                        times[ctx.guild.id].reverse()

                except KeyError:
                    
                    embed=discord.Embed(description=f"No messages have been deleted", color=0xfdfdfd)
                    embed.set_author(name="Error", icon_url=error_png)
                    embed.add_field(name="What happened?", value=f"No deleted messages have been logged. (Since last reload)")
                
                await ctx.send(embed=embed)

            except TypeError:
                await ctx.send(embed=error_embed("Incorrect Data Type","`[amount]` only accepts `int` data types."))

        except AttributeError:
            await ctx.send(embed=no_dm)
    
    # Used to be exception for type error...
    @commands.command(aliases=['snipeuser','usnipe','u'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def usersnipe(self, ctx, user: discord.Member=None):
        try:
            if not user:
                user=ctx.author
            try:
                sniped = users[user.id][ctx.guild.id]
                embed=discord.Embed(description="`$usersnipe <user>`", color=0xfdfdfd)
                if len(sniped.content) == 0:
                    embed.add_field(name = f"Message ", value=f"(No message was provided)")
                else:
                    embed.add_field(name = f"Message ", value=f"{sniped.content}")

                embed.add_field(name = f"User ", value=f"{sniped.author}", inline=False)
                embed.set_footer(text=f"Msg ID: {sniped.id}")
                embed.set_author(name="Message Snipe", icon_url=sniped.author.avatar_url)
                
                if sniped.attachments:
                    msg="\n\n*Images and files logging is still in development! Sorry for the inconvenience.*"
                    files = [attachment.filename for attachment in sniped.attachments]
                    embed.add_field(name="Attachment(s)", value=f"\n{str(files[0])}{msg}")

                await ctx.send(embed=embed)

            except KeyError:
                await ctx.send(embed=error_embed("No Logged Deleted Messages",f"No deleted messages from {user.mention} have been logged. (Since last reload)"))
        except AttributeError: # FOR DMS
            await ctx.send(embed=no_dm)

    # type error?
    @commands.command(aliases=['sniper','deleted','s','sniped','snip'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def snipe(self, ctx, channel: discord.TextChannel = None):
        try:
            if not channel:
                channel = ctx.channel
            try:
                sniped = channels[ctx.guild.id][channel.id]
                embed=discord.Embed(description="`$snipe <channel>`", color=0xfdfdfd)
                if len(sniped.content) == 0:
                    embed.add_field(name = f"Message ", value=f"(No message was provided)")
                else:
                    embed.add_field(name = f"Message ", value=f"{sniped.content}")

                embed.add_field(name = f"User ", value=f"{sniped.author}", inline=False)
                embed.set_footer(text=f"Msg ID: {sniped.id}")
                embed.set_author(name="Message Snipe", icon_url=sniped.author.avatar_url)

                if sniped.attachments:
                    msg="\n\n*Images and files logging is still in development! Sorry for the inconvenience.*"
                    files = [attachment.filename for attachment in sniped.attachments]
                    embed.add_field(name="Attachment(s)", value=f"\n{str(files[0])}{msg}")

                await ctx.send(embed=embed)

            except KeyError:
                await ctx.send(embed=error_embed("No messages deleted. (Since last reload)","No messages can be sniped. (Sniper doesn't log deleted messages that were sent __before__ its last reload."))
        except AttributeError:
            await ctx.send(embed=no_dm)

    # type error?
    @commands.command(aliases=['esnipe','e','edited'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def editsnipe(self, ctx, channel: discord.TextChannel = None):
        try: 
            if not channel:
                channel = ctx.channel
            try:
                found=None
                index=int()
                for i in beforemsg[ctx.guild.id]:
                    if str(i).startswith("{"+f"{channel.id}"):
                        found=channel.id
                        index=beforemsg[ctx.guild.id].index(i)
                    else:
                        pass

                if found is None:
                    error_embed("Invalid Channel",f"There were no messages edited in {channel}")
                else:
                    before = beforemsg[ctx.guild.id][index][found][len(beforemsg[ctx.guild.id][index][found])-1]
                    after = aftermsg[ctx.guild.id][index][found][len(aftermsg[ctx.guild.id][index][found])-1]

                    embed = discord.Embed(description="`$editsnipe <channel>`", icon_url=before.author.avatar_url, color=0xfdfdfd)
                    embed.add_field(name = f"Before ", value=f"{before.content}")
                    embed.add_field(name = f"After ", value=f"{after.content}")
                    embed.add_field(name = f"User ", value=f"{before.author}", inline=False)
                    embed.set_footer(text=f"Msg ID: {before.id}")
                    embed.set_author(name="Message Editsnipe", icon_url=before.author.avatar_url) 
                    await ctx.send(embed=embed)

            except KeyError:
                await ctx.send(embed=error_embed("No messages have been edited. (Since last reload)","No messages can be editsniped. (Sniper doesn't log edited messages that were sent __before__ its last reload.)"))
        except AttributeError:
            await ctx.send(embed=no_dm)

def setup(bot):
    bot.add_cog(Snipe(bot))
    print("Snipe has been loaded.")
