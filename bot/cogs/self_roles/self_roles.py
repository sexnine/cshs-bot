import discord
from discord.ext import commands
from bot.util.config import get_config


class SelfRoles(commands.Cog):
    def __init__(self, bot: discord.Bot):
        print("self_roles")
        self.bot = bot
        print("self_roles")
        self.config = get_config("self_roles")
        print("self_roles")

    @commands.guild_only()
    @commands.is_owner()
    @commands.command(name="sendrolepicker")
    async def send_role_picker_cmd(self, ctx: commands.Context) -> None:
        view = discord.ui.View()
        interaction_id = self.config.get("role_picker_interaction_id")
        view.add_item(discord.ui.Button(label="📜 Let's choose them", style=discord.ButtonStyle.success, custom_id=interaction_id))

        embed = discord.Embed(title="Self-Assignable Roles",
                              description="Tell us a bit about you with some custom roles :)")

        await ctx.send(embed=embed, view=view)

    async def role_picker_interaction(self, interaction: discord.Interaction):
        async def apply_remove_roles(user: discord.Member, apply: list, remove: list):
            user_role_ids = [role.id for role in user.roles]

            for role_id in apply:
                if role_id not in user_role_ids:
                    await user.add_roles(user.guild.get_role(role_id))
            for role_id in remove:
                if role_id in user_role_ids:
                    await user.remove_roles(user.guild.get_role(role_id))

        async def process_response(i: discord.Interaction, roles: dict):
            user = i.user
            user_selection = i.data.get("values")

            apply_roles = []
            remove_roles = []
            for role_id in roles.keys():
                if role_id in user_selection:
                    apply_roles.append(int(role_id))
                else:
                    remove_roles.append(int(role_id))

            await apply_remove_roles(user, apply_roles, remove_roles)
            await i.response.pong()

        view = discord.ui.View()

        selects = []
        current_user_roles = [str(role.id) for role in interaction.user.roles]
        for role_type, role_options in self.config.data.get("assignable_roles").items():
            select_options = []
            cannot_set_another_default_option = False

            for role_id, info in role_options.get("roles").items():
                default_option = False

                if role_id in current_user_roles and not cannot_set_another_default_option:
                    default_option = True
                    if role_options.get("single_value"):
                        cannot_set_another_default_option = True

                select_option = discord.SelectOption(label=info.get("label") or role_options.get("default_label"),
                                                     description=info.get("description") or role_options.get("default_description"),
                                                     emoji=info.get("emoji") or role_options.get("default_emoji"),
                                                     default=default_option,
                                                     value=role_id)
                select_options.append(select_option)

            if role_options.get("none_option"):
                select_option = discord.SelectOption(label="None", description="Select this and only this to have no roles for this option", emoji="🚫", value="none")

                select_options.append(select_option)

            select = discord.ui.Select(placeholder=role_options.get("placeholder"),
                                       options=select_options,
                                       max_values=1 if role_options.get("single_value") else len(select_options))

            async def gen_callback(ri: dict):
                async def cb(inter: discord.Interaction):
                    await process_response(inter, ri)
                return cb

            select.callback = await gen_callback(self.config.data.get("assignable_roles").get(role_type).get("roles"))
            selects.append(select)

        for select_obj in selects:
            view.add_item(select_obj)

        await interaction.response.send_message("**📜 Choose your roles**", view=view, ephemeral=True)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.data["custom_id"] == self.config.data.get("role_picker_interaction_id"):
            await self.role_picker_interaction(interaction)


def setup(bot: discord.Bot):
    bot.add_cog(SelfRoles(bot))
