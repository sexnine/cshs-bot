from discord.ext import commands
import discord
from typing import Union, Dict, Optional
import asyncio

from bot.util.util import random_id


class ConversationResponse:
    def __init__(self, response: Union[discord.Message, discord.Interaction, None] = None, finished: bool = False,
                 action: str = None, last_message_sent: discord.Message = None):
        self.response = response
        self.type = type(response) if response else None
        self.finished = finished
        self.action = action
        self.last_message_sent = last_message_sent


class ConversationBuilder:
    def __init__(self, bot: commands.Bot, cancel_button: bool = True, timeout: float = 60.0,
                 wait_for_message: bool = False, wait_for_interaction: bool = False, edit_last_message: bool = False):
        self.bot = bot
        self.cancel_button = cancel_button
        self.timeout = timeout
        self.wait_for_message = wait_for_message
        self.wait_for_interaction = wait_for_interaction
        self.edit_last_message = edit_last_message
        self.last_message = None

    @staticmethod
    def _cancel_button() -> discord.ui.Button:
        return discord.ui.Button(label="Cancel",
                                 style=discord.ButtonStyle.danger,
                                 custom_id=random_id())

    @staticmethod
    async def _send_cancelled_msg(ctx: commands.Context, message: str = None) -> None:
        await ctx.send(content=ctx.author.mention,
                       embed=discord.Embed(description=message or "Cancelled", color=0xff5e5e))

    @staticmethod
    async def _send_timeout_msg(ctx: commands.Context) -> None:
        await ctx.send(content=ctx.author.mention,
                       embed=discord.Embed(description="You didn't respond in time, cancelled.", color=0xff5e5e))

    async def ask(self, ctx: commands.Context, message: Optional[str] = None, cancel_button: bool = None,
                  buttons: Dict[str, discord.ui.Button] = None, wait_for_message: bool = None,
                  wait_for_interaction: bool = None, timeout: float = None, edit_last_message: bool = None, embed: discord.Embed = None) -> ConversationResponse:
        def check_is_msg_response(m: discord.Message) -> bool:
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id

        def check_is_interaction_reply(i: discord.Interaction) -> bool:
            return i.data.get("custom_id") in interactions and i.user.id == ctx.author.id

        if buttons is None:
            buttons = {}
        if cancel_button is None:
            cancel_button = self.cancel_button
        if wait_for_interaction is None:
            wait_for_interaction = self.wait_for_interaction
        if wait_for_message is None:
            wait_for_message = self.wait_for_message
        if not wait_for_message and not wait_for_interaction:
            raise ValueError("wait_for_interaction and/or wait_for_message must be True")
        if timeout is None:
            timeout = self.timeout
        if cancel_button:
            buttons["cancel"] = self._cancel_button()
        if edit_last_message is None:
            edit_last_message = self.edit_last_message

        view = None
        interactions = {}
        if buttons:
            if not wait_for_interaction:
                raise ValueError("wait_for_interaction must be True if you have buttons")
            view = discord.ui.View()
            for action, button in buttons.items():
                interactions[button.custom_id] = action
                view.add_item(button)

        embed = embed or discord.Embed(description=message)
        message_kwargs = {"content": ctx.author.mention, "embed": embed, "view": view}
        if edit_last_message and self.last_message:
            await self.last_message.edit(**message_kwargs)
        else:
            self.last_message = await ctx.send(**message_kwargs)

        result = None
        if wait_for_message and wait_for_interaction:
            done_tasks, pending_tasks = await asyncio.wait(
                [self.bot.wait_for("interaction", check=check_is_interaction_reply),
                 self.bot.wait_for("message", check=check_is_msg_response)],
                return_when=asyncio.FIRST_COMPLETED,
                timeout=timeout)
            for task in pending_tasks:
                task.cancel()
            if not done_tasks:
                await self._send_timeout_msg(ctx)
            for task in done_tasks:
                result = await task
        else:
            check_func = check_is_msg_response if wait_for_message else check_is_interaction_reply
            event_name = "message" if wait_for_message else "interaction"
            try:
                result = await self.bot.wait_for(event_name, check=check_func, timeout=timeout)
            except asyncio.TimeoutError:
                await self._send_timeout_msg(ctx)

        action = interactions.get(result.data.get("custom_id")) if type(
            result) is discord.Interaction and result.data.get("custom_id") else None
        finished = result is None
        if action == "cancel":
            await self._send_cancelled_msg(ctx)
            finished = True

        return ConversationResponse(response=result, finished=finished, action=action, last_message_sent=self.last_message)
