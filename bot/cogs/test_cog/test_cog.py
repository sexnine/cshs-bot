from discord.ext import commands
import discord
from bot.util.util import random_id
from bot.util.config import get_config
from bot.util.models import User
from datetime import datetime
import pytz


class TestCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = get_config("test")
        self.bruh = self.config.data.get("bruh")

    @commands.command(name="test")
    async def test_cmd(self, ctx: commands.Context):
        await ctx.reply(f"{self.bruh} {random_id()}")

    @commands.command(name="givexp")
    async def test2_cmd(self, ctx: commands.Context, xp: int):
        user, was_created = await User.get_or_create(id=ctx.author.id, defaults={"xp": xp})
        if not was_created:
            user.xp = user.xp + xp
            await user.save()
        await ctx.reply(f"your xp is now {user.xp}")

    @commands.is_owner()
    @commands.command(name="count_msgs")
    async def count_msgs_cmd(self, ctx: commands.Context, after: int):
        time = datetime.utcfromtimestamp(after).replace(tzinfo=pytz.UTC)
        print(time.strftime("%m/%d/%Y, %H:%M:%S"))
        print(time.tzinfo)

        guild = ctx.guild
        channels = guild.channels
        message_counts = {}
        for channel in channels:
            if channel.type != discord.ChannelType.text:
                # print(f"Ignoring {channel.name} because it's not a text channel")
                continue
            print(f"Counting messages from #{channel.name}")
            try:
                async for message in channel.history(after=time, limit=None):
                    if message.author.bot:
                        continue

                    # print(f"counting message: {message.content} from {message.author.name}")
                    user_id = message.author.id
                    if user_id in message_counts:
                        message_counts[user_id] += 1
                    else:
                        message_counts[user_id] = 1
            except Exception:
                print(f"Failed counting from #{channel.name}")
            else:
                print(f"Finished counting from #{channel.name}")
        print("Finished counting")

        output = "user,count\n"
        for user, count in message_counts.items():
            output += f"{user},{count}\n"

        with open("out.csv", "w") as f:
            f.write(output)
        print("Finished writing")

        await ctx.message.add_reaction("👌")



def setup(bot):
    bot.add_cog(TestCog(bot))
