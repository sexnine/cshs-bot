from dis import dis
import discord
import time

from discord.ext import commands
from bot.util import config


class Misc(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.config = config.get_config("misc")

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """ Pong! """
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        message = await ctx.send("🏓 Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")

    @commands.command()
    async def echo(self, ctx: commands.Context, *, content: str):
        """ echo! """
        embed = discord.Embed(title=content, color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.errors.MissingRequiredArgument) or isinstance(err, commands.errors.BadArgument):
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send_help(helper)
        
        elif isinstance(err, commands.errors.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown... try again in {err.retry_after:.2f}")
    
    @commands.Cog.listener()
    async def on_user_join(self, member: discord.Member):
        welcome_channel = member.guild.get_channel(self.config.get("welcome_channel"))
        rules_channel = member.guild.get_channel(self.config.get("rules_channel"))
        value = f"Welcome {member.mention} to {member.guild.name}' Discord server! Check out our rules over at {rules_channel.mention} and have a nice stay!"
        await welcome_channel.send(value)

    @commands.command(aliases=["gh"])
    async def github(self, ctx: commands.Context):
        embed = discord.Embed(description="**[Github](https://github.com/sexnine/cshs-bot)**")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))
