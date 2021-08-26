# import packages
import discord
from discord.ext import commands
import cassiopeia as cass

# get api key and set up cass
with open('api.txt', 'r') as f:
    key = f.read()
cass.set_riot_api_key(key)
cass.set_default_region("NA")


# get summoner data
async def summoner(ctx, username):
    user = cass.get_summoner(name=username)
    if not user.exists:
        await ctx.send("User not found")
        return
    return user.profile_icon.url


# profile cog
class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # users used to store and discord user and league username in dict
        self.users = {}

    '''# get summoner data from id
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
        return tier, rank, lp, wins, losses'''

    # create profile command
    @commands.command(help='Find the profile of a given player or your linked account',
                      aliases=['p'])
    # username is optional argument that allows for linked account
    async def profile(self, ctx, *, username=None):
        # check if username is linked if none provided
        if username is None:
            try:
                self.users[ctx.author.id]
            except KeyError:
                await ctx.send("You do not have an account linked")
                return

        # getting information about user
        icon = await summoner(ctx, username)
        await ctx.send(icon)

        '''# create profile embed
        profile_embed = discord.Embed(
            title=user,
            colour=discord.Colour.gold()
        )
        profile_embed.set_thumbnail(url=icon)
        wr = int((wins/(wins+losses))*1000)/10
        profile_embed.add_field(name="Rank:", value=f"{tier} {rank}, LP: {lp}")
        profile_embed.add_field(name="Win/Loss:", value=f"W: {wins}, L: {losses}, WR: {wr}%", inline=False)
        await ctx.send(embed=profile_embed)'''


# add cog
def setup(bot):
    bot.add_cog(Profile(bot))
