import dbl
import discord
from discord.ext import commands


class topAPI(commands.Cog, name="topAPI"):

    def __init__(self, bot): 
        self.bot = bot
        self.token = 'insert token here' # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True)

def setup(bot):
    bot.add_cog(topAPI(bot))
    print("topAPI has been loaded.")