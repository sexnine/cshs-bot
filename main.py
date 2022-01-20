import discord
import os
from discord.ext import commands
from bot.util.config import get_config
from bot.util.help import DefaultHelpCommand
from bot.db import init as init_beanie

config = get_config("bot")

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.reactions = True
intents.presences = True
bot = commands.Bot(
    command_prefix=config.get("prefixes", "-"),
    intents=intents,
    allowed_mentions=discord.AllowedMentions(
        roles=False,
        users=True,
        everyone=False
    ),
    help_command=DefaultHelpCommand(),
    owner_ids=config.get("owners")
)

cogs = config.get("cogs", [])
if "config_manager" not in cogs:
    cogs.append("config_manager")

for cog in cogs:
    bot.load_extension(f"bot.cogs.{cog}.{cog}")


@bot.event
async def on_ready():
    print("Bot ready")
    await init_beanie()


try:
    bot.run(os.getenv("DISCORD_TOKEN"))
except Exception as e:
    print(f"Error when logging in {e}")
