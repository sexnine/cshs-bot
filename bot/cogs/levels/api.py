from bot.db import User
from discord.ext import commands
from errors import XPCantBeNegative


class LevelsApi:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ignore these errors for now, they will be using self
    async def add_xp(self, user_id: int, xp: int) -> User:
        user = await User.get(id=user_id)
        user.xp += xp
        if user.xp < 0:
            raise XPCantBeNegative
        await user.save()
        return user

    async def set_xp(self, user_id: int, xp: int) -> User:
        user = User(id=user_id, xp=xp)
        await user.save()
        return user

    async def _refresh_level(self, user_id: int):
        # TODO
        pass
