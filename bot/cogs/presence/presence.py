import discord

from discord.ext import commands
from bot.util import config

class Presence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = config.get_config("rich_presence")
    
    @commands.Cog.listener()
    async def on_ready(self):
        global activity
        activity_type = self.config.get("type")
        name = self.config.get("activity_name")
        status = self.config.get("status")
        
        match(activity_type):
            case "game":
                await self.bot.change_presence(activity=discord.Game(name))
            case "streaming":
                url = self.config.get("url")
                activity=discord.Streaming(name=name, url=url)
            case "watching":
                activity=discord.Activity(type=discord.ActivityType.watching, name=name)
            case "listening":
                activity=discord.Activity(type=discord.ActivityType.listening, name=name)
            case _:
                activity=discord.Activity(type=discord.ActivityType.listening, name="-help")
        
        match(status):
            case "online":
                await self.bot.change_presence(status=discord.Status.online, activity=activity)
            case "dnd":
                await self.bot.change_presence(status=discord.Status.dnd, activity=activity)
            case "invisible":
                await self.bot.change_presence(status=discord.Status.invisible, activity=activity)
            case "idle":
                await self.bot.change_presence(status=discord.Status.idle, activity=activity)
            case _:
                await self.bot.change_presence(status=discord.Status.online, activity=activity)

        
def setup(bot):
    bot.add_cog(Presence(bot))