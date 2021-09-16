from discord.ext import commands
from cogs.mongo import Mongo


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.group()
    async def set(self, ctx):
        pass

    @set.command()
    async def prefix(self, ctx, prefix):
        guild_id = ctx.guild.id
        await Mongo.update_prefix(Mongo(self.bot), guild_id, prefix)
        nickname = ctx.bot.user.name
        await ctx.me.edit(nick=f'{nickname}[{prefix}]')
        await ctx.send(f"prefix changed to {prefix}")

    @set.command()
    async def welcomer(self, ctx, channel: commands.TextChannelConverter):
        guild_id = ctx.guild.id
        await Mongo.update_welcomer(Mongo(self.bot), guild_id, channel)
        await ctx.send(f"welcomer channel set to {channel.name}")

    @commands.Cog.listener()
    async def on_member_join(self, member: commands.UserConverter):
        guild_id = member.guild.id
        result = await Mongo.fetch_welcomer(Mongo(self.bot), guild_id)
        if result is None:
            return
        else:
            welcomer_channel = result["welcomer_channel"]
            channel = member.guild.get_channel(welcomer_channel)
            await channel.send(f"{member} joined this server")


def setup(bot):
    bot.add_cog(Config(bot))


async def what_prefix(bot, message: commands.MessageConverter):
    guild_id = message.guild.id
    result = await Mongo.fetch_prefix(Mongo(bot), guild_id)
    if result is None:
        return "$"
    else:
        return result["prefix"]
