from logging import exception
import discord
from discord.ext import commands
import os
from bot.util.config import get_config

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

@bot.event
async def on_user_join(member):
    try:
        channel = discord.utils.get(bot.guild.text_channels, name="👋-welcome")
        rules = discord.utils.get(bot.guild.text_channels, name="📃-rules")
        try:
            value=f"Welcome {member.mention} to {member.guild.name}' Discord server! Check out our rules over at {rules.mention} and have a nice stay!"
            await channel.send(value)
        except Exception as e:
            raise e
    except Exception as e:
        raise e

bot.run(os.getenv("DISCORD_TOKEN"))
