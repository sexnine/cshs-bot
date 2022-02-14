import discord

from discord.ext.commands import DefaultHelpCommand

def can_handle(ctx, permission: str):
    """ Checks if bot has permissions or is in DMs right now """
    return isinstance(ctx.channel, discord.DMChannel) or getattr(ctx.channel.permissions_for(ctx.guild.me), permission)
       
class HelpFormat(DefaultHelpCommand):
    def get_destination(self, no_pm: bool = False):
        if no_pm:
            return self.context.channel
        else:
            return self.context.author
    
    async def send_error_message(self, error):
        destination = self.get_destination(no_pm=True)
        await destination.send(error)
    
    async def send_command_help(self, command):
        self.add_command_formatting(command)
        self.paginator.close_page()
        await self.send_pages(no_pm=True)
    
    async def send_pages(self, no_pm: bool = False):
        try:
            if can_handle(self.context, "add_reactions"):
                await self.context.message.add_reaction(chr(0x2709))
        except discord.Forbidden:
            pass
        
        try:
            destination = self.get_destination(no_pm=no_pm)
            for page in self.paginator.pages:
                await destination.send(page)
        except discord.discord.Forbidden:
            destination = self.get_destination(no_pm=True)
            await destination.send("Couldn't send help to you due to blocked DMs...")