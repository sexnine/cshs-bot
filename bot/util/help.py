from discord import commands
import discord

class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        embed = discord.Embed(color=discord.Color.yellow(), description='')
        for page in self.paginator.pages:
            embed.description += page
        await destination.send(embed=e)
