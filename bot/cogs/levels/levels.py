from discord.ext import commands
import discord
from typing import Optional
from .util import get_rank_card
from .api import LevelsApi
from .errors import XPCantBeNegative
from bot.util import embed_msg, MsgStatus
from bot.util.config import get_config
from bot.db import User


class Levels(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = get_config("levels")
        self.api = LevelsApi(bot, self.config, self.on_level_up)

    @commands.command(name="rank", aliases=["r"])
    async def rank_cmd(self, ctx: commands.Context, user: Optional[discord.Member]):
        user = user or ctx.author
        card = await get_rank_card(user)
        embed = discord.Embed().set_image(url=card.url)
        await ctx.reply(embed=embed)

    @commands.command(name="leaderboard", aliases=["lb"])
    async def leaderboard_cmd(self, ctx: commands.Context):
        pass

    # TODO: perms
    @commands.group(name="xp")
    async def xp_cmd(self, ctx: commands.Context):
        pass

    @xp_cmd.command(name="set")
    async def set_xp_cmd(self, ctx: commands.Context, user: discord.Member, xp: int):
        try:
            user_info = await self.api.add_xp(user.id, xp)
        except XPCantBeNegative:
            await ctx.reply(
                embed=embed_msg(f"You can't set {user.mention}'s xp to a negative number.", MsgStatus.ERROR))
            return

        await ctx.reply(embed=embed_msg(f"Set {user.mention}'s xp to `{user_info.xp}`."))

    @xp_cmd.command(name="add")
    async def add_xp_cmd(self, ctx: commands.Context, user: discord.Member, xp: int):
        try:
            user_info = await self.api.add_xp(user.id, xp)
        except XPCantBeNegative:
            await ctx.reply(embed=embed_msg(f"You can't make {user.mention} have negative xp.", MsgStatus.ERROR))
            return

        await ctx.reply(
            embed=embed_msg(f"Added `{xp}` xp to {user.mention}'s total.  {user.mention} now has `{user_info.xp}` xp."))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # TODO: checks, use config
        if not message.author.bot:
            await self.api.add_xp(message.author.id, 50)

    async def on_level_up(self, user: User, old_level: int):
        print(f"{user.id} leveled up to {user.level} from {old_level}")
        # TODO


def setup(bot):
    bot.add_cog(Levels(bot))
