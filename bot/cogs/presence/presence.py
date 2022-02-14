import discord

from discord.ext import commands
from bot.util import config


class Presence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = config.get_config("rich_presence")
    
    @commands.Cog.listener()
    async def on_ready(self):
        global activity, status_info, url
        activity_type = self.config.get("type")
        name = self.config.get("activity_name")
        status = self.config.get("status")
        
        match(activity_type):
            case "game":
                activity = discord.Game(name)
            
            case "streaming":
                url = self.config.get("url")
                activity = discord.Streaming(name=name, url=url)
            
            case "watching":
                activity = discord.Activity(type=discord.ActivityType.watching, name=name)
            
            case "listening":
                activity = discord.Activity(type=discord.ActivityType.listening, name=name)
            
            case _:
                activity = discord.Activity(type=discord.ActivityType.listening, name="-help")
        
        match(status):
            case "online":
                status_info = discord.Status.online
            
            case "dnd":
                status_info = discord.Status.dnd
            
            case "invisible":
                status_info = discord.Status.invisible
            
            case "idle":
                status_info = discord.Status.idle
            
            case _:
                status_info = discord.Status.online
        
        await self.bot.change_presence(status=status_info, activity=activity)

    @commands.group()
    @commands.is_owner()
    async def presence(self, ctx: commands.Context):
        """ Change Presence """
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))
    
    @presence.command()
    async def status(self, ctx: commands.Context, Status: str):
        """ Change Bot Status """
        Status = Status.lower()
        match(Status):
            case "online":
                status_info = discord.Status.online
        
            case "dnd":
                status_info = discord.Status.dnd
        
            case "invisible":
               status_info = discord.Status.invisible
        
            case "idle":
                status_info =discord.Status.idle
        
            case _:
                status_info=discord.Status.online
        
        await self.bot.change_presence(status=status_info, activity=activity)
        
        embed = discord.Embed(title=":white_check_mark: Success", description=f"Successfully changed Bots status to **{Status}**", color=0xa2faa3)
        await ctx.send(embed=embed)

    @presence.command()
    async def activity(self, ctx: commands.Context, activity_type: str, *, name: str):
        """ Change Bot Activity """
        activity_type = activity_type.lower()
        match(activity_type):
            case "game":
                activity = discord.Game(name)
            
            case "streaming":
                await ctx.send("Please use `-presence streaming` instead")
            
            case "watching":
                activity = discord.Activity(type=discord.ActivityType.watching, name=name)
            
            case "listening":
                activity = discord.Activity(type=discord.ActivityType.listening, name=name)
            
            case _:
                activity = discord.Activity(type=discord.ActivityType.listening, name="-help")
        
        await self.bot.change_presence(status=status_info, activity=activity)
        
        embed = discord.Embed(title=":white_check_mark: Success", description=f"Successfully changed Bots Activity to **{activity_type}** - **{name}**", color=0xa2faa3)
        await ctx.send(embed=embed)
    
    @presence.command()
    async def streaming(self, ctx: commands.Context, url, *, name: str):
        """ Change Activity to streaming """
        url = url.strip("<>")
        activity = discord.Streaming(name=name, url=url)
        
        await self.bot.change_presence(status=status_info, activity=activity)
        
        embed = discord.Embed(title=":white_check_mark: Success", description=f"Successfully changed the Bot's status to **Streaming** - *{url}* : **{name}**", color=0xa2faa3)
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Presence(bot))