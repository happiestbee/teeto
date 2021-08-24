# import packages
import discord
from discord.ext import commands

# get api key
with open('api.txt', 'r') as f:
    key = f.read()


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users = {}

    @commands.command(help='Find the profile of a given player or your linked account',
                      alias='p')
    async def profile(self, ctx):
        await ctx.send("hello")


# add cog
def setup(bot):
    bot.add_cog(Profile(bot))
