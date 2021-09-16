from discord.ext import commands
import logging


class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger = logging.getLogger('discord')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(
            filename='discord.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)


def setup(bot):
    bot.add_cog(Log(bot))
