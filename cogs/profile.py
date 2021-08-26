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


# get champion data and make embed
async def champion(ctx, champion: cass.Champion):
    icon = champion.image.url
    classes = ", ".join(champion.tags)
    tips = champion.ally_tips
    title = champion.title
    lore = champion.lore
    play_rates = champion.play_rates
    for role in play_rates:
        print(play_rates[role])
    e = discord.Embed(
        title=champion.name.title(),
        colour=discord.Colour.gold(),
        description=title
    )
    e.set_thumbnail(url=icon)
    e.add_field(name="Classes:", value=classes)
    e.add_field(name="Lore:", value=lore, inline=False)
    return e


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
                user = self.users[ctx.author.id]
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

    # create champion command
    @commands.command(help="Get brief info .about a champion")
    async def champion(self, ctx, *, champion_name=None):
        # check if user provided a champio name
        if champion_name is None:
            await ctx.send("Please provide a champion name")
            return
        # convert champion name to correct format for search
        champion_name = champion_name.lower().title()
        try:
            champ = cass.get_champion(champion_name)
            e = await champion(ctx, champ)
            await ctx.send(embed=e)
        # check if champion exists
        except Exception as e:
            if str(e) == champion_name:
                await ctx.send("Champion not found")
            else:
                raise


# add cog
def setup(bot):
    bot.add_cog(Profile(bot))
