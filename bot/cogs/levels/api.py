from typing import Callable, Awaitable, Optional
from beanie.odm.operators.update.general import Inc, Set
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

    async def add_xp(self, user_id: int, xp: int, return_user: bool = False) -> Optional[User]:
        user = await User.get_user(user_id)
        data_to_set = await self.util.get_level_set(user)
        if data_to_set:
            await user.update(Inc({User.xp: xp}), Set(data_to_set))
        else:
            await user.update(Inc({User.xp: xp}))
        return await User.get_user(user_id) if return_user else None

    async def set_xp(self, user_id: int, xp: int) -> User:
        user = User(id=user_id, xp=xp)
        user = await self.util.set_level(user, force_calculate=True)
        await user.save()
        return user

    async def _refresh_level(self, user_id: int):
        # TODO
        pass
