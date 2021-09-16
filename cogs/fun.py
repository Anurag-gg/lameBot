from discord.ext import commands
from math import log
import requests
import random
import json

URL_UD = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
URL_TRAN = "https://nlp-translation.p.rapidapi.com/v1/translate"


class Fun(commands.Cog):
    def __init__(self,  bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        ping = ctx.bot.latency
        await ctx.send(f'ping is {ping:2f}ms')

    @commands.command()
    async def roll(self, ctx, value: commands.Greedy[int] = [100]):
        await ctx.send(random.randint(0, value[0]))

    # DANGEROUS DONT USE THIS
    @commands.command()
    async def calc(self, ctx, expression):
        try:
            await ctx.send(eval(expression))
        except Exception as e:
            await ctx.send(f"error:{e}")

    @commands.command(aliases=["definition", "dict"])
    async def ud(self, ctx, *, args):
        querystring = {"term": "".join(args)}
        headers = {
            'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
            'x-rapidapi-key': "2c1f383f4cmsh2b7aaaaedc2c4b3p1ff3a9jsnfd0be5ed9013"
        }
        response = requests.request(
            "GET", URL_UD, headers=headers, params=querystring)
        data = response.text
        data = json.loads(data)
        if data["list"] != []:
            for i, entry in enumerate(data["list"]):
                if i < 5:
                    definition = entry["definition"]
                    await ctx.send(f'{i+1}> {definition}')
        else:
            await ctx.send("no definitions found")

    @commands.command()
    async def translate(self, ctx, *, args):
        querystring = {"text": "".join(args), "to": "en"}

        headers = {
            'x-rapidapi-host': "nlp-translation.p.rapidapi.com",
            'x-rapidapi-key': "2c1f383f4cmsh2b7aaaaedc2c4b3p1ff3a9jsnfd0be5ed9013"
        }

        response = requests.request(
            "GET", URL_TRAN, headers=headers, params=querystring)
        data = response.text
        data = json.loads(data)
        await ctx.send(data["translated_text"]["en"])


def setup(bot):
    bot.add_cog(Fun(bot))
