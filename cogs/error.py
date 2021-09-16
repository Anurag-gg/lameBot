from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        if isinstance(e, commands.CommandNotFound):
            pass
        elif isinstance(e, commands.MissingRequiredArgument):
            await ctx.send("missing arguments")
        elif isinstance(e, commands.BadArgument):
            await ctx.send("parsing / conversion failure")
        elif isinstance(e, commands.TooManyArguments):
            await ctx.send("command was sent too many arguments")
        elif isinstance(e, commands.UserNotFound):
            await ctx.send("user not found")
        elif isinstance(e, commands.MissingPermissions):
            await ctx.send("user missing permissions")
        elif isinstance(e, commands.BotMissingPermissions):
            await ctx.send("bot missing permissions")
        elif isinstance(e, commands.ChannelNotFound):
            await ctx.send("no such channels found")
        else:
            print(e)


def setup(bot):
    bot.add_cog(Errors(bot))
