import discord
import time

from discord.ext import commands
from bot.util import config


class Misc(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.config = config.get_config("bot")

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """ Pong! """
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        message = await ctx.send("🏓 Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")

    @commands.command(name="echo")
    async def echo(self, ctx: commands.Context, *, content: str):
        """ echo! """
        embed = discord.Embed(title=f"{content}", color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_user_join(self, member: discord.Member):
        channel = discord.utils.get(self.bot.guild.text_channels, name="👋-welcome")
        rules = discord.utils.get(self.bot.guild.text_channels, name="📃-rules")
        value = f"Welcome {member.mention} to {member.guild.name}' Discord server! Check out our rules over at {rules.mention} and have a nice stay!"
        await channel.send(value)
    
    @commands.Cog.listener()
    async def on_ready(self):
        activity = discord.Game(name=self.config.get("status", ""))
        config_activity = self.config.get("activity", "")
        await self.bot.change_presence(status=config_activity, activity=activity)


def setup(bot):
    bot.add_cog(Misc(bot))
