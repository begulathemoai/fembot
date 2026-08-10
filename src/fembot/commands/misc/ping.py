import discord

from ...utils import auth, globals


@globals.tree.command(name="ping")
@auth.auth()
async def ping(interaction: discord.Interaction) -> None:
    await interaction.edit_original_response(content="pong :bangbang:")
