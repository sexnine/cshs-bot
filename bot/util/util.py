from uuid import uuid4
from enum import Enum
import discord
import vacefron

vac = vacefron.Client()


class MsgStatus(Enum):
    NEUTRAL = None
    SUCCESS = 0x42ff52
    WARN = 0xffc942
    ERROR = 0xff4f42


def random_id() -> str:
    return uuid4().hex


def embed_msg(text: str, status: MsgStatus = MsgStatus.SUCCESS) -> discord.Embed:
    return discord.Embed(description=text, color=status.value)
