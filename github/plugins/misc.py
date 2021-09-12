import discord
from discord.ext import commands
import sqlite3
from Bot import error_embed, success_embed, no_dm
import math
import time
import json



def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)

startTime = time.time()

def getUptime():
    return time.time() - startTime

class Misc(commands.Cog, name='Misc'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['updateprefix','changeprefix'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, customprefix):
        if len(customprefix) > 10:
            await ctx.send(embed=error_embed("Prefix is too long", "Please set a prefix under 10 characters. Note that if you have spaces in your requested prefix, only the first word will be set as the prefix."))
        else:
            with open('files/json/prefixes.json', 'r') as file:
                prefixes = json.load(file)

            prefixes[str(ctx.guild.id)] = customprefix

            with open('files/json/prefixes.json', 'w') as file:
                json.dump(prefixes, file, indent=4)

            await ctx.send(embed=success_embed("Prefix changed successfully!", f"The prefix for Sniper has been changed to `{customprefix}` for this server!"))

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def info(self, ctx):
        try:
            embed=discord.Embed(description="All info on Sniper", color=0xfdfdfd)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/742833913751142402/852664825301303337/sniperbot_logo.png")
            embed.set_author(name="Info")
            embed.add_field(name="Invite Links", value="[Administrator](https://discord.com/api/oauth2/authorize?client_id=742784763206828032&permissions=8&scope=bot)\n[Selectable Permissions](https://discord.com/api/oauth2/authorize?client_id=742784763206828032&permissions=2148134064&scope=bot)")
            embed.add_field(name="More Links", value="[Top.GG](https://top.gg/bot/742784763206828032)\n[Vote](https://top.gg/bot/742784763206828032/vote)")
            embed.add_field(name=f"Total Server Count: `{len(self.bot.guilds)}`", value=f"Servers currently using Sniper",inline=False)
            # Shards?
            embed.add_field(name=f"Uptime: `{convert(getUptime())}`", value=f"Current uptime for Sniper", inline=False)
            embed.add_field(name=f"Source Code", value="Click [here](https://github.com/xIntensity9/snipe)", inline=False)
            await ctx.send(embed=embed)
        except AttributeError:
            await ctx.send(embed=no_dm)

def setup(bot):
    bot.add_cog(Misc(bot))
    print("Misc has been loaded.")