from discord.ext import commands
from cogs.mongo import Mongo


class Moderation(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = 10, *, reason=None):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'{amount} messages purged.\nreason = {reason}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: commands.UserConverter, *, reason=None):
        await ctx.guild.ban(member, reason=reason)
        await ctx.send(f"{member} has been banned")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: commands.UserConverter, *, reason=None):
        await ctx.guild.unban(member, reason=reason)
        await ctx.send(f'{member} has been unbanned')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: commands.UserConverter, *, reason=None):
        await ctx.guild.kick(member, reason=reason)
        await ctx.send(f'{member} has been kicked')

    @commands.has_permissions(manage_messages=True)
    @commands.group(invoke_without_command=True)
    async def censor(self, ctx, word):
        guild_id = ctx.guild.id
        await Mongo.add_blacklist(Mongo(self.bot), guild_id, word)
        await ctx.send(f"'{word}' has been censored")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def uncensor(self, ctx, word):
        guild_id = ctx.guild.id
        await Mongo.remove_blacklist(Mongo(self.bot), guild_id, word)
        await ctx.send(f"'{word}' has been uncensored")

    @censor.command()
    async def list(self, ctx):
        guild_id = ctx.guild.id
        result = await Mongo.fetch_blacklist(Mongo(self.bot), guild_id)
        await ctx.send("CENSORED WORDS:\n" + "\n".join(result["blacklist_words"]))

    @commands.Cog.listener("on_message")
    async def whatever_you_want_to_call_it(self, message):
        if message.author.bot:
            return
        result = await Mongo.fetch_blacklist(Mongo(self.bot), message.guild.id)
        result = result["blacklist_words"]
        for bad_words in result:
            if bad_words in message.content:
                await message.delete()
                await message.channel.send(f'hey {message.author.mention} that word is censored')


def setup(bot):
    bot.add_cog(Moderation(bot))
