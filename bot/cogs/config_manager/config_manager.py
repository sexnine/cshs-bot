# Used for managing the config for the bot and cogs
from discord.ext import commands
from bot.util.config import get_config, ConfigDoesntExistError, ConfigNotLoadedError


# TODO: perms
class ConfigManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name="config")
    async def cmd(self, ctx: commands.Context):
        pass

    @cmd.command(name="get")
    async def get_config_cmd(self, ctx: commands.Context, name: str):
        if not name:
            await ctx.reply("You must specify a config")
            return

        config = None
        try:
            config = get_config(name, False)
        except ConfigDoesntExistError:
            await ctx.reply("That config doesn't exist")
            return

        await ctx.reply("OK")  # TODO: Give user config in dms

    @cmd.command(name="reload")
    async def reload_config_cmd(self, ctx: commands.Context, name: str):
        if not name:
            await ctx.reply("You must specify a config")
            return

        config = None
        try:
            config = get_config(name, False, False)
        except ConfigDoesntExistError:
            await ctx.reply("That config doesn't exist")
            return
        except ConfigNotLoadedError:
            await ctx.reply("That config isn't loaded")
            return

        config._load_config()
        await ctx.reply("done :)")

    @cmd.command(name="set")
    async def set_config_cmd(self, ctx: commands.Context, name: str):
        if not name:
            await ctx.reply("You must specify a config")
            return
