import discord
from vacefron import RankCard
from bot.db import User

from bot.util import vac


async def get_rank_card(user: discord.Member) -> RankCard:
    user_info = await User.get(user)
    # TODO
    card = await vac.rank_card(username=user.name,
                               avatar=user.avatar.url,
                               current_xp=user_info.xp,
                               next_level_xp="?",
                               previous_level_xp="?",
                               rank="?")
    return card
