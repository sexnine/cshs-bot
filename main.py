import time
import discord
import os

from logging import exception
from discord.ext import commands
from bot.util.config import get_config
from bot.util.help import DefaultHelpCommand

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
    help_command=DefaultHelpCommand()
    )

cogs = config.get("cogs", [])  # TODO: Move into config file

for cog in cogs:
    bot.load_extension(f"bot.cogs.{cog}.{cog}")

@bot.event
async def on_ready():
    print("Bot ready")

try:
    bot.run(os.getenv("DISCORD_TOKEN"))
except Exception as e:
    print(f"Error when logging in {e}")
