from motor.motor_asyncio import AsyncIOMotorClient
from discord.ext import commands
import config


class MongoDBConnectionManager():
    def __init__(self, URL, bot):
        self.URL = URL
        self.connection = None
        self.bot = bot

    def __enter__(self):
        self.connection = AsyncIOMotorClient(
            self.URL, io_loop=self.bot.loop)["discord"]
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.close


class Mongo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def add_blacklist(self, guildID, word):
        with MongoDBConnectionManager(config.MONGO_URL, self.bot) as db:

            collection = db.connection.get_collection("blacklist")
            if await collection.find_one({"_id": guildID}):
                await collection.update_one({"_id": guildID}, {
                    "$addToSet": {"blacklist_words": word}})
            else:
                data = {"_id": guildID, "blacklist_words": [word]}
                await collection.insert_one(data)

    async def remove_blacklist(self, guildID, word):
        with MongoDBConnectionManager(config.MONGO_URL, self.bot) as db:

            await db.connection.get_collection("blacklist").update_one({"_id": guildID}, {
                "$pull": {"blacklist_words": word}})

    async def fetch_blacklist(self, guildID):
        with MongoDBConnectionManager(config.MONGO_URL, self.bot) as db:

            return await db.connection.get_collection("blacklist").find_one({"_id": guildID})

    async def update_welcomer(self, guildID, channel):
        with MongoDBConnectionManager(config.MONGO_URL, self.bot) as db:

            collection = db.connection.get_collection("welcomer")
            if await collection.find_one({"_id": guildID}):
                await collection.update_one({"_id": guildID}, {
                    "$set": {"welcomer_channel": str(channel)}})
            else:
                data = {"_id": guildID, "welcomer_channel": str(channel)}
                await collection.insert_one(data)

    async def fetch_welcomer(self, guildID):
        with MongoDBConnectionManager(config.MONGO_URL, self.bot) as db:

            return await db.connection.get_collection("welcomer").find_one({"_id": guildID})

    async def update_prefix(self, guildID, prefix):
        with MongoDBConnectionManager(config.MONGO_URL, self.bot) as db:

            collection = db.connection.get_collection("prefixes")
            if await collection.find_one({"_id": guildID}):
                await collection.update_one({"_id": guildID}, {
                    "$set": {"prefix": prefix}})
            else:
                data = {"_id": guildID, "prefix": prefix}
                await collection.insert_one(data)

    async def fetch_prefix(self, guildID):
        with MongoDBConnectionManager(config.MONGO_URL, self.bot) as db:

            collection = db.connection.get_collection("prefixes")
            return await collection.find_one({"_id": guildID})


def setup(bot):
    bot.add_cog(Mongo(bot))
