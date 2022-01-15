import discord
from discord.ext import commands
import os
from bot.util.config import get_config
from tortoise import Tortoise

config = get_config("bot")

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=config.get("prefixes", "-"), intents=intents)

cogs = config.get("cogs", [])  # TODO: Move into config file

for cog in cogs:
    bot.load_extension(f"bot.cogs.{cog}.{cog}")


@bot.event
async def on_ready():
    print("Bot ready")
    await Tortoise.init(db_url="sqlite://data/db.sqlite3",
                        modules={"models": ["bot.util.models"]})

    await Tortoise.generate_schemas()


bot.run(os.getenv("DISCORD_TOKEN"))
