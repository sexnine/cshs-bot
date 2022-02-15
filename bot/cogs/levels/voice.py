import discord
from discord.ext import commands
from bot.util.config import get_config
from asyncio import get_event_loop
from .api import LevelsApi
from typing import List


class VoiceAddon:
    def __init__(self, bot: commands.Bot, api: LevelsApi):
        self.bot = bot
        self.api = api
        self.config = get_config("levels")
        self.bot_check_queue: List[int] = []

    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):
        channel = after.channel
        print(self.bot_check_queue)
        if channel and channel.id not in self.bot_check_queue:
            self.bot_check_queue.append(channel.id)
            print(self.bot_check_queue)

    async def check_task(self):
        voice_config = self.config.get("voice")
        ignored_channels: List[int] = voice_config.get("ingored_channels")
        users_to_add_xp = []
        for channel_id in self.bot_check_queue:
            if channel_id in ignored_channels:
                self.bot_check_queue.remove(channel_id)
                continue

            channel: discord.VoiceChannel = self.bot.get_channel(channel_id)

            user_list = list(filter(lambda x: not x.bot, channel.members))

            if len(user_list) < 2:
                self.bot_check_queue.remove(channel_id)
                continue

            if len(list(filter(lambda x: not x.self_deaf and not x.self_mute, [x.voice for x in user_list]))) < 2:
                self.bot_check_queue.remove(channel_id)
                continue

            for user in user_list:
                voice_state = user.voice
                if voice_state.self_deaf or voice_state.self_mute:
                    continue

                users_to_add_xp.append(user.id)

        event_loop = get_event_loop()
        xp_to_add = voice_config.get("xp_per_interval")
        for user in users_to_add_xp:
            event_loop.create_task(self.api.add_xp(user, xp_to_add))
