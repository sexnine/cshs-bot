import discord

from bot.util import default
from discord.ext import commands


async def check_permissions(ctx, perms, *, check=all):

    resolved = ctx.channel.permissions_for(ctx.author)
    return check(getattr(resolved, name, None) == value for name, value in perms.items())


def has_permissions(*, check=all, **perms):
    """ discord.Commands method to check if author has permissions """
    async def pred(ctx):
        return await check_permissions(ctx, perms, check=check)
    return commands.check(pred)


async def check_priv(ctx, member):
    """ Custom (weird) way to check permissions when handling moderation commands """
    try:
        # Self checks
        if member.id == ctx.author.id:
            return await ctx.send(f"You can't {ctx.command.name} yourself")
        if member.id == ctx.bot.user.id:
            return await ctx.send("So that's what you think of me huh..? sad ;-;")

        # Check if user bypasses
        if ctx.author.id == ctx.guild.owner.id:
            return False

        if member.id == ctx.guild.owner.id:
            return await ctx.send(f"You can't {ctx.command.name} the owner, lol")
        if ctx.author.top_role == member.top_role:
            return await ctx.send(f"You can't {ctx.command.name} someone who has the same permissions as you...")
        if ctx.author.top_role < member.top_role:
            return await ctx.send(f"Nope, you can't {ctx.command.name} someone higher than yourself.")
    except Exception:
        pass


def can_handle(ctx, permission: str):
    """ Checks if bot has permissions or is in DMs right now """
    return isinstance(ctx.channel, discord.DMChannel) or getattr(ctx.channel.permissions_for(ctx.guild.me), permission)