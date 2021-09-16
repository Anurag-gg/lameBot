from motor.motor_asyncio import AsyncIOMotorClient
from discord.ext import commands
import config


class Mongo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = AsyncIOMotorClient(
            config.MONGO_URL, io_loop=bot.loop)["discord"]

    async def add_blacklist(self, guildID, word):
        collection = self.db.get_collection("blacklist")
        if await collection.find_one({"_id": guildID}):
            await collection.update_one({"_id": guildID}, {
                "$addToSet": {"blacklist_words": word}})
        else:
            data = {"_id": guildID, "blacklist_words": [word]}
            await collection.insert_one(data)

    async def remove_blacklist(self, guildID, word):
        await self.db.get_collection("blacklist").update_one({"_id": guildID}, {
            "$pull": {"blacklist_words": word}})

    async def fetch_blacklist(self, guildID):
        return await self.db.get_collection("blacklist").find_one({"_id": guildID})

    async def update_welcomer(self, guildID, channel):
        collection = self.db.get_collection("welcomer")
        if await collection.find_one({"_id": guildID}):
            await collection.update_one({"_id": guildID}, {
                "$set": {"welcomer_channel": str(channel)}})
        else:
            data = {"_id": guildID, "welcomer_channel": str(channel)}
            await collection.insert_one(data)

    async def fetch_welcomer(self, guildID):
        return await self.db.get_collection("welcomer").find_one({"_id": guildID})

    async def update_prefix(self, guildID, prefix):
        collection = self.db.get_collection("prefixes")
        if await collection.find_one({"_id": guildID}):
            await collection.update_one({"_id": guildID}, {
                "$set": {"prefix": prefix}})
        else:
            data = {"_id": guildID, "prefix": prefix}
            await collection.insert_one(data)

    async def fetch_prefix(self, guildID):
        collection = self.db.get_collection("prefixes")
        return await collection.find_one({"_id": guildID})


def setup(bot):
    bot.add_cog(Mongo(bot))
