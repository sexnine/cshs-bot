from ast import alias
from distutils import command
from email import message
from time import sleep
import discord
from discord.ext import commands
from datetime import datetime as d

class misc(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
    
    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        start = d.timestamp(d.now())
        print("\npinging...")
        msg = await ctx.send(content="Pinging...")
        await msg.edit(f"🏓One message round-trip took {round((d.timestamp(d.now()) - start) * 1000, 1)}ms.")

    @commands.command(name="echo")
    async def echo(self, ctx: commands.Context, *, content:str):
        embed = discord.Embed(title=f"{content}", color=discord.Color.green())
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(misc(bot))