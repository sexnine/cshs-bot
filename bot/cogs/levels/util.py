import discord
from vacefron import RankCard
from bot.db import User
from typing import Callable, Awaitable
from bot.util import vac


async def get_rank_card(user: discord.Member) -> RankCard:
    user_info = await User.get(user)
    card = await vac.rank_card(username=str(user),
                               avatar=user.avatar.url,
                               current_xp=user_info.xp,
                               next_level_xp=user_info.next_level_xp,
                               previous_level_xp=user_info.previous_level_xp,
                               rank=None)  # TODO: rank
    return card


class LevelUtil:
    def __init__(self, xp_per_level: int, level_up_callback: Callable[[User, int], Awaitable[None]]):
        self.xp_per_level = xp_per_level
        self.level_up_callback = level_up_callback

    async def set_level(self, user: User, force_calculate: bool = False) -> User:
        old_level = user.level
        if user.xp > user.next_level_xp or force_calculate:
            user = await self.calculate_level(user)
            if user.level > old_level:
                await self.level_up_callback(user, old_level)
        return user

    async def calculate_level(self, user: User) -> User:
        lvl = 0
        xp = user.xp

        while True:
            if xp < (next_level_xp := .5 * self.xp_per_level * lvl * (lvl + 1)):
                break
            lvl += 1

        user.level = lvl
        user.next_level_xp = next_level_xp
        user.previous_level_xp = next_level_xp - lvl * self.xp_per_level

        return user
