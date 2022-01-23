import discord
from discord.ext import commands
from typing import Optional
from bot.util import vac as vac_api


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def distracted(self, ctx: commands.Context, a: discord.Member, b: discord.Member, c: discord.Member):
        """ Generate that "distracted boyfriend" meme. """
        image = await vac_api.distracted_bf(boyfriend=str(a.avatar.url),
                                            girlfriend=str(b.avatar.url),
                                            woman=str(c.avatar.url))
        meme = await image.read()
        await ctx.send(file=discord.File(meme, filename="distracted_bf.png"))

    @commands.command()
    async def dock(self, ctx: commands.Context, user: Optional[discord.Member]):
        """ Generate that "dock of shame" meme. """
        user = user or ctx.author
        image = await vac_api.dock_of_shame(str(user.avatar.url))
        meme = await image.read()
        await ctx.send(file=discord.File(meme, filename="dock_of_shame.png"))

    @commands.command()
    async def drip(self, ctx: commands.Context, user: Optional[discord.Member]):
        """ For your own Goku drip memes :) """
        user = user or ctx.author
        image = await vac_api.drip(str(user.avatar.url))
        meme = await image.read()
        await ctx.send(file=discord.File(meme, filename="drip.png"))

    @commands.command(name="carrev")
    async def car_reverse(self, ctx: commands.Context, *, args: str):
        """ Generate that "car reverse" meme. """
        image = await vac_api.car_reverse(args)
        meme = await image.read()
        await ctx.send(file=discord.File(meme, filename="car_reverse.png"))

    @commands.command(name="mind")
    async def change_my_mind(self, ctx: commands.Context, *, args: str):
        """ Generate that "change my mind" meme. """
        image = await vac_api.change_my_mind(args)
        meme = await image.read()
        await ctx.send(file=discord.File(meme, filename="change_my_mind.png"))

    @commands.command()
    async def emergency(self, ctx: commands.Context, *, args: str):
        """ Generate your own Among Us "Emergency Meeting" Meme! """
        image = await vac_api.emergency_meeting(args)
        meme = await image.read()
        await ctx.send(file=discord.File(meme, filename="emergency_meeting.png"))

    @commands.command()
    async def first(self, ctx: commands.Context, user: Optional[discord.Member]):
        """ Generate that "first time" meme. """
        user = user or ctx.author
        image = await vac_api.first_time(str(user.avatar.url))
        meme = await image.read()
        await ctx.send(file=discord.File(meme, filename="first_time.png"))

    @commands.command()
    async def rip(self, ctx: commands.Context, user: Optional[discord.Member]):
        """ Generate a Grave stone. """
        user = user or ctx.author
        image = await vac_api.grave(str(user.avatar.url))
        meme = await image.read()
        await ctx.send(file=discord.File(meme, filename="grave.png"))

    @commands.command()
    async def wide(self, ctx: commands.Context, user: Optional[discord.Member]):
        """ Makes user avatar a *little* bit **thicc**. """
        user = user or ctx.author
        image = await vac_api.wide(str(user.avatar.url))
        meme = await image.read()
        await ctx.send(file=discord.File(meme, filename="wide.png"))

    @commands.command()
    async def cat(self, ctx: commands.Context, a: discord.Member, b: discord.Member):
        """ Generate that "woman yelling at cat" meme. """
        image = await vac_api.woman_yelling_at_cat(woman=str(a.avatar.url),
                                                   cat=str(b.avatar.url))
        meme = await image.read()
        await ctx.send(file=discord.File(meme, filename="woman_yelling_at_cat.png"))

    @commands.command()
    async def table(self, ctx: commands.Context, user: Optional[discord.Member]):
        """ Generate that "Table flip" meme. """
        image = await vac_api.table_flip(user=str(user.avatar.url))
        meme = await image.read()
        await ctx.send(file=discord.File(meme, filename="table_flip.png"))

    @commands.command()
    async def adios(self, ctx: commands.Context, user: Optional[discord.Member]):
        """ Adios """
        user = user or ctx.author
        image = await vac_api.adios(user=str(user.avatar.url))
        meme = await image.read()
        await ctx.send(file=discord.File(meme, filename="Adios.png"))


def setup(bot):
    bot.add_cog(Memes(bot))
