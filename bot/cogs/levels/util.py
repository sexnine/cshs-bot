import discord
from vacefron import RankCard
from bot.db import User
from typing import Callable, Awaitable, Optional
from bot.util import vac
from asyncio import get_event_loop
from typing import Tuple, Dict


async def get_rank_card(user: discord.Member) -> RankCard:
    user_info = await User.get(user)
    card = await vac.rank_card(username=str(user),
                               avatar=user.avatar.url,
                               current_xp=user_info.xp,
                               next_level_xp=user_info.next_level_xp,
                               previous_level_xp=user_info.previous_level_xp,
                               level=user_info.level,
                               rank=None)  # TODO: rank
    return card


class LevelUtil:
    def __init__(self, xp_per_level: int, level_up_callback: Callable[[User, int], Awaitable[None]]):
        self.xp_per_level = xp_per_level
        self.level_up_callback = level_up_callback

    async def set_level(self, user: User, force_calculate: bool = False) -> User:
        result = await self.get_level(user, force_calculate)
        if result:
            user.level, user.next_level_xp, user.previous_level_xp = result
        return user

    async def get_level_set(self, user: User, force_calculate: bool = False) -> Dict:
        result = await self.get_level(user, force_calculate)
        if result:
            lvl, next_level_xp, previous_level_xp = result
            return {User.level: lvl, User.next_level_xp: next_level_xp, User.previous_level_xp: previous_level_xp}
        return {}

    async def get_level(self, user: User, force_calculate: bool = False) -> Optional[Tuple[int, int, int]]:
        if user.xp >= user.next_level_xp or force_calculate:
            result = await self.calculate_level(user)
            if result[0] > user.level:
                get_event_loop().create_task(self.level_up_callback(user, user.level))
            return result
        return None

    async def calculate_level(self, user: User) -> Tuple[int, int, int]:
        lvl = 0
        xp = user.xp

        while True:
            if xp < (next_level_xp := .5 * self.xp_per_level * lvl * (lvl + 1)):
                break
            lvl += 1

        previous_level_xp = next_level_xp - lvl * self.xp_per_level

        return lvl, int(next_level_xp), int(previous_level_xp)
