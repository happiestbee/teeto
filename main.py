# import packages
import discord
from discord.ext import commands

# get token
with open('token.txt', 'r') as f:
    token = f.read()


# initiating bot
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        await self.change_presence(activity=discord.Game(name=" !help"))


# creating bot object
bot = Bot()

# getting cogs and loading cogs
initial_extensions = ['cogs.profile', 'cogs.champion']
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}., {e}')

# running bot
bot.run(token)
