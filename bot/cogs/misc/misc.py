import discord
from discord.ext import commands
from datetime import datetime as d


class Misc(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        start = d.timestamp(d.now())
        print("\npinging...")
        msg = await ctx.send(content="Pinging...")
        await msg.edit(f"🏓One message round-trip took {round((d.timestamp(d.now()) - start) * 1000, 1)}ms.")

    @commands.command(name="echo")
    async def echo(self, ctx: commands.Context, *, content: str):
        embed = discord.Embed(title=f"{content}", color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_user_join(self, member: discord.Member):
        channel = discord.utils.get(self.bot.guild.text_channels, name="👋-welcome")
        rules = discord.utils.get(self.bot.guild.text_channels, name="📃-rules")
        value = f"Welcome {member.mention} to {member.guild.name}' Discord server! Check out our rules over at {rules.mention} and have a nice stay!"
        await channel.send(value)


def setup(bot):
    bot.add_cog(Misc(bot))
