from bot.util.models import User
from discord.ext import commands


class LevelsApi:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ignore these errors for now, they will be using self
    async def add_xp(self, user_id: int, xp: int) -> User:
        user, was_created = await User.get_or_create(id=user_id, defaults={"xp": xp if xp > 0 else 0})
        if not was_created:
            user.xp = user.xp + xp
            await user.save()
        return user

    async def set_xp(self, user_id: int, xp: int) -> User:
        user, _ = await User.update_or_create(id=user_id, defaults={xp: xp})
        return user

    async def get_xp(self, user_id: int) -> int:
        user, _ = await User.get_or_create(id=user_id, defaults={"xp": 0})
        return user.xp

    async def _refresh_level(self, user_id: int):
        # TODO
        pass
