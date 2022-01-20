import discord
import psutil
import os
import time

from discord.ext import commands
from datetime import datetime as d

class Misc(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

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
        embed = discord.Embed(title=f"{content}", color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(aliases=["info", "stats", "status"])
    async def about(self, ctx):
        """ About the bot """
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = sum(g.member_count for g in self.bot.guilds) / len(self.bot.guilds)

        embedColour = discord.Embed.Empty
        if hasattr(ctx, "guild") and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour

        embed = discord.Embed(colour=embedColour)
        embed.set_thumbnail(url=ctx.bot.user.avatar)
        embed.add_field(name="Library", value="pycord")
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers:,.2f} users/server )")
        embed.add_field(name="Commands loaded", value=len([x.name for x in self.bot.commands]))
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB")

        await ctx.send(content=f"ℹ About **{ctx.bot.user}**", embed=embed)

    @commands.Cog.listener()
    async def on_user_join(self, member: discord.Member):
        channel = discord.utils.get(self.bot.guild.text_channels, name="👋-welcome")
        rules = discord.utils.get(self.bot.guild.text_channels, name="📃-rules")
        value = f"Welcome {member.mention} to {member.guild.name}' Discord server! Check out our rules over at {rules.mention} and have a nice stay!"
        await channel.send(value)


def setup(bot):
    bot.add_cog(Misc(bot))
