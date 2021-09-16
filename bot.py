from discord.ext import commands
from discord import Intents
import config

import cogs
from cogs.botConfig import what_prefix


intents = Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=what_prefix, intents=intents)


initial_extensions = cogs.default
if __name__ == "__main__":
    for i in initial_extensions:
        bot.load_extension(f'cogs.{i}')

bot.run(config.BOT_TOKEN)
