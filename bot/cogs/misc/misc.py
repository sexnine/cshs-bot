from dis import dis
import discord
import time

from discord.ext import commands
from bot.util import config


class Misc(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        self.config = config.get_config("misc")

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """ Pong! """
        before = time.monotonic()
        before_ws = int(round(self.bot.latency * 1000, 1))
        message = await ctx.send("🏓 Pong")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 WS: {before_ws}ms  |  REST: {int(ping)}ms")

    @commands.command()
    async def echo(self, ctx: commands.Context, *, content: str):
        """ echo! """
        embed = discord.Embed(title=content, color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.errors.MissingRequiredArgument) or isinstance(err, commands.errors.BadArgument):
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send_help(helper)
        
        elif isinstance(err, commands.errors.CommandOnCooldown):
            await ctx.send(f"This command is on cooldown... try again in {err.retry_after:.2f}")
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = self.config.get("guildid")
        welcome_channel = self.bot.get_channel(self.config.get("welcome_channel"))
        rules_channel = self.bot.get_channel(self.config.get("rules_channel"))

        if member.bot or guild != member.guild.id:
            if member.bot:
                role = self.bot.get_roles(self.config.get("bot_role"))
                member.add_roles(role)
            return

        value = f"Welcome {member.mention} to {member.guild.name}' Discord server! Check out our rules over at {rules_channel.mention} and have a nice stay!"
        await welcome_channel.send(value)

    @commands.command(aliases=["gh"])
    async def github(self, ctx: commands.Context):
        embed = discord.Embed(description="**[Github](https://github.com/sexnine/cshs-bot)**")
        await ctx.send(embed=embed)
        
    @commands.command()
    async def virus(self, ctx: commands.Context, file_hash: str = None):
        if file_hash is None:
            try:
                attachment = ctx.message.attachments[0]
                url = attachment.url
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=url) as data:
                        data = await data.read()
                byte_data = bytes(data)
                hashed_data = hashlib.sha256(byte_data).hexdigest()
                file_hash = hashed_data
            except IndexError:
                await ctx.send("Send a hash or file to detect for malware!")
        if re.search(r"^[A-Za-z0-9]{32}$", file_hash):
            hash_type = 'md5_hash'
        elif re.search(r"^[A-Za-z0-9]{64}$", file_hash):
            hash_type = 'sha256_hash'
        else:
            await ctx.send("This isn't a valid hash! Use SHA256 or MD5 instead.")
            return
    
        msg = await ctx.send("Checking database...")
        data = {hash_type: file_hash}
        async with aiohttp.ClientSession() as session:
            async with session.post(url="https://urlhaus-api.abuse.ch/v1/payload/", data=data) as data:
                data = await data.json()
        if data["query_status"] == "ok":
            embed = discord.Embed(title="Warning!", description="This program has a virus!", color=0xFF0000)
            sha256_hash = data["sha256_hash"]
            md5_hash = data["md5_hash"]
            embed.add_field(name="Hashes", value=f"""
            SHA256 Hash: {sha256_hash}
            MD5 Hash: {md5_hash}""")
            virustotal = data["virustotal"]
            result = virustotal["result"]
            percent = virustotal["percent"]
            file_size = int(data["file_size"])
            embed.add_field(name="Virustotal Info", value=f"""
            Result: {result}
            Percentage: {percent}
            Link: https://virustotal.com/gui/file/{sha256_hash}/detection
            File size: {round(file_size / 1024, 2)}KB
            """)
        elif data["query_status"] == "no_results":
            embed = discord.Embed(title="No results", description="No results appear in the database. It still could be a virus though!")
        else:
            embed = discord.Embed(title="Error", description="Something went wrong.")
        await msg.edit(content=None, embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))
