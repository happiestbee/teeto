# import packages
import discord
from discord.ext import commands

# get token
with open('token.txt', 'r') as f:
    token = f.read()

# getting cogs
initial_extensions = []


# initiating bot
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.change_presence(activity=discord.Game(name=" !help"))


# creating bot object
bot = Bot()

# running bot
bot.run(token)
