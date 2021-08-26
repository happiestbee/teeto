# import packages
import discord
from discord.ext import commands
import cassiopeia as cass

# get api key and set up cass
with open('api.txt', 'r') as f:
    key = f.read()
cass.set_riot_api_key(key)
cass.set_default_region("NA")


# get champion data and make embed
async def champion(champion_query: cass.Champion):
    icon = champion_query.image.url
    classes = ", ".join(champion_query.tags)
    tips = champion_query.ally_tips
    title = champion_query.title
    lore = champion_query.lore
    play_rates = champion_query.play_rates
    for role in play_rates:
        print(play_rates[role])
    e = discord.Embed(
        title=champion_query.name.title(),
        colour=discord.Colour.gold(),
        description=title
    )
    e.set_thumbnail(url=icon)
    e.add_field(name="Classes:", value=classes)
    e.add_field(name="Lore:", value=lore, inline=False)
    return e


# profile cog
class Champion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # create champion command
    @commands.command(help="Get brief info .about a champion")
    async def champion(self, ctx, *, champion_name=None):
        # check if user provided a champion name
        if champion_name is None:
            await ctx.send("Please provide a champion name")
            return
        # convert champion name to correct format for search
        champion_name = champion_name.lower().title()
        try:
            champ = cass.get_champion(champion_name)
            e = await champion(champ)
            await ctx.send(embed=e)
        # check if champion exists
        except Exception as e:
            if str(e) == champion_name:
                await ctx.send("Champion not found")
            else:
                raise


# add cog
def setup(bot):
    bot.add_cog(Champion(bot))
