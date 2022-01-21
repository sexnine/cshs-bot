# Used for managing the config for the bot and cogs
from discord.ext import commands
from bot.util.config import get_config, ConfigDoesntExistError, ConfigNotLoadedError, get_config_discord_file
from bot.util import embed_msg, MsgStatus


class ConfigManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name="config")
    @commands.dm_only()
    @commands.is_owner()
    async def cmd(self, ctx: commands.Context):
        """Manage configs for the bot and cogs"""
        pass

    @cmd.command(name="get")
    async def get_config_cmd(self, ctx: commands.Context, name: str):
        """Retrieve a config file"""
        if not name:
            await ctx.reply(embed=embed_msg("You must specify a config", MsgStatus.ERROR))
            return

        try:
            config_file = get_config_discord_file(name)
        except ConfigDoesntExistError:
            await ctx.reply(embed=embed_msg("That config doesn't exist", MsgStatus.ERROR))
            return

        await ctx.reply(embed=embed_msg(f"Here's the `{name}` config"), file=config_file)

    @cmd.command(name="reload")
    async def reload_config_cmd(self, ctx: commands.Context, name: str):
        """Reload a config"""
        if not name:
            await ctx.reply(embed=embed_msg("You must specify a config", MsgStatus.ERROR))
            return

        try:
            config = get_config(name, False, False)
        except ConfigDoesntExistError:
            await ctx.reply(embed=embed_msg("That config doesn't exist", MsgStatus.ERROR))
            return
        except ConfigNotLoadedError:
            await ctx.reply(embed=embed_msg("That config isn't loaded", MsgStatus.ERROR))
            return

        config._load_config()
        await ctx.reply(embed=embed_msg(f"Reloaded `{name}`"))

    @cmd.command(name="set")
    async def set_config_cmd(self, ctx: commands.Context, name: str):
        """Sets the config but doesn't reload it"""
        if not name:
            await ctx.reply(embed=embed_msg("You must specify a config", MsgStatus.ERROR))
            return

        attachments = ctx.message.attachments
        if len(attachments) != 1:
            await ctx.reply(embed=embed_msg("Please send `1` file with your message", MsgStatus.ERROR))
            return

        file = attachments[0]
        path = f"./config/{name}.yml"
        await file.save(path)
        await ctx.reply(embed=embed_msg(f"Saved to `path`"))


def setup(bot):
    bot.add_cog(ConfigManager(bot))
