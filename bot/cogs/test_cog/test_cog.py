from discord.ext import commands
import discord
from bot.util.util import random_id
from bot.util.config import get_config


class TestCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = get_config("test")
        self.bruh = self.config.data.get("bruh")

    @commands.command(name="test")
    async def test_cmd(self, ctx: commands.Context):
        await ctx.reply(f"{self.bruh} {random_id()}")


def setup(bot):
    bot.add_cog(TestCog(bot))
