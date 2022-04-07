import discord
import os
from discord.ext import commands
from bot.util.config import get_config
from bot.util.help import HelpCommand
from bot.db import init as init_beanie

config = get_config("bot")
# Uses config for owner(s), fallbacks to application info
commands.Bot.owner_ids = property(lambda self: config.get("owners") or self._owner_ids, lambda self, users: setattr(self, "_owner_ids", users))
commands.Bot.owner_id = property(lambda self: None if self.owner_ids else self._owner_id, lambda self, user_id: setattr(self, "_owner_id", user_id))

intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=config.get("prefixes", "-"),
    intents=intents,
    allowed_mentions=discord.AllowedMentions(
        roles=False,
        users=True,
        everyone=False
    ),
    help_command=HelpCommand(),
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
