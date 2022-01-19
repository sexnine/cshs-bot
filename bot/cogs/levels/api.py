from typing import Callable, Awaitable
from bot.db import User
from discord.ext import commands
from .errors import XPCantBeNegative
from bot.util.config import Config
from .util import LevelUtil


class LevelsApi:
    def __init__(self, bot: commands.Bot, config: Config, level_up_callback: Callable[[User, int], Awaitable[None]]):
        self.bot = bot
        self.config = config
        self.util = LevelUtil(self.config.get("xp_per_level"), level_up_callback)

    async def add_xp(self, user_id: int, xp: int) -> User:
        user = await User.get(user=user_id)
        user.xp += xp
        if user.xp < 0:
            raise XPCantBeNegative
        user = await self.util.set_level(user)
        await user.save()
        return user

    async def set_xp(self, user_id: int, xp: int) -> User:
        user = User(id=user_id, xp=xp)
        user = await self.util.set_level(user, force_calculate=True)
        await user.save()
        return user

    async def _refresh_level(self, user_id: int):
        # TODO
        pass
