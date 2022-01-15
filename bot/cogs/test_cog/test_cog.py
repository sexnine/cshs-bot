from discord.ext import commands
import discord
from bot.util.util import random_id
from bot.util.config import get_config
from bot.util.models import User


class TestCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = get_config("test")
        self.bruh = self.config.data.get("bruh")

    @commands.command(name="test")
    async def test_cmd(self, ctx: commands.Context):
        await ctx.reply(f"{self.bruh} {random_id()}")

    @commands.command(name="givexp")
    async def test2_cmd(self, ctx: commands.Context, xp: int):
        user, was_created = await User.get_or_create(id=ctx.author.id, defaults={"xp": xp})
        if not was_created:
            user.xp = user.xp + xp
            await user.save()
        await ctx.reply(f"your xp is now {user.xp}")


def setup(bot):
    bot.add_cog(TestCog(bot))
