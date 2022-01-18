from discord.ext import commands
import discord
from bot.util.util import random_id
from bot.util.config import get_config
from bot.util.db import User
from typing import Optional


class Levels(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="rank")
    async def rank_cmd(self, ctx: commands.Context, user: Optional[discord.Member]):
        user = user or ctx.author
        # TODO

    @commands.command(name="leaderboard")
    async def leaderboard_cmd(self, ctx: commands.Context):
        pass

    @commands.group(name="xp")
    async def xp_cmd(self, ctx: commands.Context):
        pass

    @xp_cmd.command(name="set")
    async def set_xp_cmd(self, ctx: commands.Context, user: discord.Member, xp: int):
        pass

    @xp_cmd.command(name="add")
    async def add_xp_cmd(self, ctx: commands.Context, user: discord.Member, xp: int):
        pass
