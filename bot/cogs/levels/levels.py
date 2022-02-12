from discord.ext import commands
import discord
from discord.ui import Button
from typing import Optional
from .util import get_rank_card
from .api import LevelsApi
from .errors import XPCantBeNegative
from .voice import VoiceAddon
from bot.util import embed_msg, MsgStatus
from bot.util.config import get_config
from bot.db import User
from bot.util.conversation import ConversationBuilder


class Levels(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = get_config("levels")
        self.api = LevelsApi(bot, self.config, self.on_level_up)
        VoiceAddon(self.bot, self.api)

    @commands.command(name="rank", aliases=["r"])
    async def rank_cmd(self, ctx: commands.Context, user: Optional[discord.Member]):
        user = user or ctx.author
        card = await get_rank_card(user)
        embed = discord.Embed().set_image(url=card.url)
        await ctx.reply(embed=embed)

    @commands.command(name="leaderboard", aliases=["lb"])
    async def leaderboard_cmd(self, ctx: commands.Context):
        items_per_page = 12
        query = User.find(User.xp > 0).sort().limit(items_per_page)
        conversation = ConversationBuilder(self.bot, cancel_button=False, timeout=30.0, wait_for_interaction=True, edit_last_message=True)

        async def do_nothing(_):
            pass

        conversation._send_timeout_msg = do_nothing

        conversation_ongoing = True
        page = 0
        user_count = await User.find(User.xp > 0).count()

        while conversation_ongoing:
            embed = discord.Embed(title="🏆 Leaderboard")
            users = await query.skip(page * items_per_page).to_list()
            embed.set_footer(text=f"Requested by {ctx.author} | Page {page + 1}")

            for i, user in enumerate(users):
                discord_user = self.bot.get_user(user.id)
                name = discord_user.name if discord_user else "Unknown User"
                embed.add_field(name=f"#{page*items_per_page+i+1}: {name}", value=f"Level: `{user.level}`\nTotal XP: `{user.xp:,}`")

            response = await conversation.ask(ctx, embed=embed, buttons={"prev": Button(label="Previous Page", disabled=page == 0),
                                                                         "next": Button(label="Next Page", disabled=user_count <= (page + 1) * items_per_page)})

            if response.action == "prev":
                page -= 1
            elif response.action == "next":
                page += 1
            elif response.finished:
                conversation_ongoing = False
                message = response.last_message_sent
                await message.edit(view=None)

    @commands.is_owner()
    @commands.group(name="xp")
    async def xp_cmd(self, ctx: commands.Context):
        pass

    @xp_cmd.command(name="set")
    async def set_xp_cmd(self, ctx: commands.Context, user: discord.Member, xp: int):
        try:
            user_info = await self.api.set_xp(user.id, xp)
        except XPCantBeNegative:
            await ctx.reply(
                embed=embed_msg(f"You can't set {user.mention}'s xp to a negative number.", MsgStatus.ERROR))
            return

        await ctx.reply(embed=embed_msg(f"Set {user.mention}'s xp to `{user_info.xp:,}`."))

    @xp_cmd.command(name="add")
    async def add_xp_cmd(self, ctx: commands.Context, user: discord.Member, xp: int):
        if xp <= 0:
            await ctx.reply(
                embed=embed_msg(f"You can't add negative XP, please use `set` instead of `add`", MsgStatus.ERROR))
            return

        user_info = await self.api.add_xp(user.id, xp, True)

        await ctx.reply(
            embed=embed_msg(f"Added `{xp:,}` xp to {user.mention}'s total.  {user.mention} now has `{user_info.xp:,}` xp."))

    @xp_cmd.group(name="debug")
    async def xp_debug_cmd(self, ctx: commands.Context):
        pass

    @xp_debug_cmd.command(name="add_from_file")
    async def xp_debug_add_from_file_cmd(self, ctx: commands.Context):
        attachments = ctx.message.attachments
        if len(attachments) != 1:
            await ctx.reply(embed=embed_msg("Please send `1` file with your message", MsgStatus.ERROR))
            return

        attachment = attachments[0]
        file_content_bytes = await attachment.read()
        file_content = file_content_bytes.decode("utf-8")
        lines = file_content.splitlines()
        await ctx.reply(embed=embed_msg(f"Starting now with {len(lines)} lines"))

        error_lines = []
        for i, line in enumerate(lines):
            try:
                user, xp = line.split(",")
                await self.api.add_xp(int(user), int(xp), force_recalculate=True)
            except Exception as e:
                error_lines.append(i+1)
                print(f"Error adding xp from file on line {i+1}: {e}")

        error_lines_text = "`, `".join([str(x) for x in error_lines])
        error_text = f"\n\nHad errors on `{len(error_lines)}` lines: `{error_lines_text}`" if error_lines_text else ""

        await ctx.reply(embed=embed_msg("Done" + error_text))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # TODO: checks
        if not message.author.bot:
            await self.api.add_xp(message.author.id, self.config.get("xp_per_message"))

    async def on_level_up(self, user_id: int, level: int, next_level_xp: int, previous_level_xp: int):
        discord_user = self.bot.get_user(user_id)
        embed = discord.Embed(title="**🎉 LEVEL UP!**",
                              description=f"{discord_user.mention} just reached Level **{level}**")
        embed.add_field(name="Next Level:", value=f"`{next_level_xp:,}` xp")
        embed.set_thumbnail(url=discord_user.avatar.url)

        await self.bot.get_channel(self.config.get("level_up_channel")).send(embed=embed)


def setup(bot):
    bot.add_cog(Levels(bot))
