from __future__ import annotations
import pymongo
from motor.motor_asyncio import AsyncIOMotorClient
# from odmantic import Field, Model
# from odmantic import AIOEngine
from beanie import Document, Indexed, init_beanie
from os import getenv
from typing import Union
import discord
from bot.util.config import get_config

db = AsyncIOMotorClient(getenv("MONGO_URI"))


class User(Document):
    id: int
    xp: Indexed(int, index_type=pymongo.DESCENDING) = 0
    level: int = 1  # updated whenever "xp > next_level_xp" or xp is manually set
    next_level_xp: int = get_config("levels").get("xp_per_level")  # reduces load on the bot
    previous_level_xp: int = 0  # reduces load on the bot

    # @classmethod
    # async def get(cls, user: Union[int, discord.Member, discord.User]) -> User:
    #     user_id = user if type(user) is int else user.id
    #     user = await cls.find_one(User.id == user_id)
    #     if not user:
    #         user = User(id=user_id)
    #         await user.save()
    #     return user


async def init():
    await init_beanie(database=db[getenv("DB_NAME", "bot")], document_models=[User])
    print("db initialized")
