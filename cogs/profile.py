# import packages
import discord
from discord.ext import commands
import requests
import json

# get api key
with open('api.txt', 'r') as f:
    key = f.read()


# main profile cog
class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # users used to store and discord user and league username in dict
        self.users = {}

    # load summoner data
    async def summoner(self, ctx, username):
        url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}?api_key={key}"
        data = requests.get(url)
        json_data = json.loads(data.text)
        try:
            user_id = json_data["id"]
        except KeyError:
            await ctx.send("User not found")
            return False
        icon = f"http://ddragon.leagueoflegends.com/cdn/11.16.1/img/profileicon/{json_data['profileIconId']}.png"
        level = json_data["summonerLevel"]
        user = json_data["name"]
        tier, rank, lp, wins, losses = await self.summoner_data(ctx, user_id)
        return icon, level, user, tier, rank, lp, wins, losses

    # get summoner data from id
    async def summoner_data(self, ctx, summoner_id):
        url = f"https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={key}"
        data = requests.get(url)
        try:
            json_data = json.loads(data.text)[0]
        except IndexError:
            await ctx.send("User has no ranked stats")
            return
        tier = json_data["tier"]
        rank = json_data["rank"]
        lp = json_data["leaguePoints"]
        wins = json_data["wins"]
        losses = json_data["losses"]
        return tier, rank, lp, wins, losses

    # create profile command
    @commands.command(help='Find the profile of a given player or your linked account',
                      aliases=['p'])
    # username is optional argument that allows for linked account
    async def profile(self, ctx, *, username=None):
        # check if username is linked if none provided
        if username is None:
            try:
                user = self.users[ctx.author.id]
            except KeyError:
                await ctx.send("You do not have an account linked")
                return

        # getting information about user
        icon, level, user, tier, rank, lp, wins, losses = await self.summoner(ctx, username)
        profile_embed = discord.Embed(
            title=user,
            colour=discord.Colour.gold()
        )
        # creating profile embed
        profile_embed.set_thumbnail(url=icon)
        wr = int((wins/(wins+losses))*1000)/10
        profile_embed.add_field(name="Rank:", value=f"{tier} {rank}, LP: {lp}")
        profile_embed.add_field(name="Win/Loss:", value=f"W: {wins}, L: {losses}, WR: {wr}%", inline=False)
        await ctx.send(embed=profile_embed)


# add cog
def setup(bot):
    bot.add_cog(Profile(bot))
