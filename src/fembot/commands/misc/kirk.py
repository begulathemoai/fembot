import discord

from ...utils import auth, globals, storage, utils


@globals.tree.command(name="kirk", description="le kirk")
@discord.app_commands.describe(text="kirky message")
@auth.auth(auth_level=auth.PermissionLevel.ADMIN)
async def kirk(interaction: discord.Interaction, text: str) -> None:
    if not globals.guilds[interaction.guild_id].enable_the_kirk:
        await interaction.edit_original_response(
            content="kirky messages are disabled on this server :wilted_rose:"
        )
        return
    if utils.regex_checker(text, [globals.NWORD_REGEX, globals.NWORD_REGEX_BUT_FRENCH]):
        await interaction.edit_original_response(content="no")
    else:
        storage.add_kirky_message(text, interaction.guild_id)
        await interaction.edit_original_response(content="fait")
