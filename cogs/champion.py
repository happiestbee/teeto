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
    best_role = ""
    highest = 0
    for role in play_rates:
        if play_rates[role] > highest:
            highest = play_rates[role]
            best_role = role.name
    best_role = best_role.capitalize()
    if best_role == "Utility":
        best_role = "Support"
    e = discord.Embed(
        title=champion_query.name.title(),
        colour=discord.Colour.gold(),
        description=title
    )
    e.set_thumbnail(url=icon)
    e.add_field(name="Classes:", value=classes)
    e.add_field(name="Role:", value=best_role)
    e.add_field(name="Lore:", value=lore, inline=False)
    return e


# get stat information
async def get_stats(champion_query: cass.Champion, embed: discord.Embed):
    stats = champion_query.stats
    wr = champion_query.info
    diff = wr.difficulty

    # edit embed message
    embed.clear_fields()
    embed.add_field(name="Difficulty:", value=f"{diff}/10")
    return embed


# get ability information
async def get_abilities(champion_query: cass.Champion, embed: discord.Embed):
    # create dict for ability information
    abilities = {}

    # get passive information
    passive = champion_query.passive
    abilities[0] = (passive.name, passive.description, passive.image_info.url)

    # get regular abilities
    i = 1
    for spell in champion_query.spells:
        abilities[i] = (spell.name, spell.description, spell.image_info.url)
        i += 1

    print(abilities)
    return abilities


# get skins information
async def get_skins(champion_query: cass.Champion):
    skins = {}
    for skin in champion_query.skins:
        skins[skin.name] = skin.splash_url
    return skins


# create skins select for easy viewing
class SkinSelect(discord.ui.Select):
    def __init__(self, skins, msg):
        self.skins = skins
        self.msg = msg

        # create select options
        options = []
        for name, url in self.skins.items():
            options.append(discord.SelectOption(label=name))

        super().__init__(placeholder="Select a skin...", options=options)

    async def callback(self, interaction: discord.Interaction):
        # get name and url and make new embed
        name = interaction.data['values'][0]
        url = self.skins[interaction.data['values'][0]]
        new_embed = discord.Embed(
            title=name,
            colour=discord.Colour.blurple()
        )
        new_embed.set_image(url=url)
        await self.msg.edit(embed=new_embed)


# create view for skin select
class SkinView(discord.ui.View):
    def __init__(self):
        super().__init__()


# create champion view for buttons
class ChampionView(discord.ui.View):
    def __init__(self, ctx, message, champ, embed):
        super().__init__()

        # get message to edit
        self.message = message
        self.embed = embed

        self.champ = champ
        self.ctx = ctx

    # instantiate buttons
    @discord.ui.button(label="Overview",
                       style=discord.ButtonStyle.gray,
                       disabled=True,
                       emoji='❔')
    async def overview(self, button: discord.ui.Button, interaction: discord.Interaction):
        for buttons in self.children:
            if buttons != button:
                buttons.disabled = False
                buttons.style = discord.ButtonStyle.green

        overview_embed = await champion(self.champ)

        button.disabled = True
        button.style = discord.ButtonStyle.gray

        # update message
        await self.message.edit(embed=overview_embed, view=self)

    @discord.ui.button(label="Stats",
                       style=discord.ButtonStyle.green,
                       disabled=False,
                       emoji='📊')
    async def stats(self, button: discord.ui.Button, interaction: discord.Interaction):
        for buttons in self.children:
            if buttons != button:
                buttons.disabled = False
                buttons.style = discord.ButtonStyle.green
        button.disabled = True
        button.style = discord.ButtonStyle.gray

        stats_embed = await get_stats(self.champ, self.embed)

        # update message
        await self.message.edit(embed=stats_embed, view=self)

    @discord.ui.button(label="Abilities",
                       style=discord.ButtonStyle.green,
                       disabled=False,
                       emoji='⚔️')
    async def abilities(self, button: discord.ui.Button, interaction: discord.Interaction):
        for buttons in self.children:
            if buttons != button:
                buttons.disabled = False
                buttons.style = discord.ButtonStyle.green

        abilities = await get_abilities(self.champ, self.embed)
        for index, ability in abilities.items():
            await self.ctx.send(content=f"{ability[0]}, {ability[1]}\n{ability[2]}")

        button.disabled = True
        button.style = discord.ButtonStyle.gray

        # update message
        await self.message.edit(view=self)

    @discord.ui.button(label="Skins",
                       style=discord.ButtonStyle.green,
                       disabled=False,
                       emoji='🎀')
    async def skins(self, button: discord.ui.Button, interaction: discord.Interaction):
        for buttons in self.children:
            if buttons != button:
                buttons.disabled = False
                buttons.style = discord.ButtonStyle.green
        button.disabled = True
        button.style = discord.ButtonStyle.gray

        # clear embed message
        self.embed.clear_fields()
        self.embed.add_field(name="Check the new message to view skins", value="Use the dropdown to select the skin you want to see")

        skins = await get_skins(self.champ)

        # create embed message for skins
        skin_embed = discord.Embed(
            title="Select a skin to start",
            colour=discord.Colour.blurple()
        )
        view = SkinView()
        msg = await self.ctx.send(embed=skin_embed, view=view)
        view.add_item(SkinSelect(skins, msg))
        await msg.edit(view=view)

        # update message
        await self.message.edit(embed=self.embed, view=self)


# champion cog
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
            # create initial embed and message
            champ = cass.get_champion(champion_name)
            e = await champion(champ)
            msg = await ctx.send(embed=e)

            # create view for message with buttons
            view = ChampionView(ctx, msg, champ, e)
            await msg.edit(embed=e, view=view)
        # check if champion exists
        except Exception as e:
            if str(e) == champion_name:
                await ctx.send("Champion not found")
            else:
                raise


# add cog
def setup(bot):
    bot.add_cog(Champion(bot))
