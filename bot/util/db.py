from __future__ import annotations
from odmantic import Field, Model
from odmantic import AIOEngine
from os import getenv
from typing import Union, Optional
import discord
from bot.util.db_util import Saveable


db = AIOEngine(getenv("MONGO_URI"))


class User(Model, Saveable):
    id: int = Field(primary_field=True)
    xp: int = 0
    level: int = 0

    @classmethod
    async def get(cls, user: Union[int, discord.Member, discord.User]) -> User:
        user_id = user if type(user) is int else user.id
        user = await db.find_one(User, User.id == user_id)
        if not user:
            user = User(id=user_id)
            await db.save(user)
        return user
