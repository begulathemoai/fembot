import discord

from ...utils import auth, globals


@globals.tree.command(
    name="stop", description="Arrête la musique et efface la file d'attente."
)
@discord.app_commands.describe()
@auth.auth()
async def stop(interaction: discord.Interaction) -> None:
    if not globals.guilds[
        interaction.guild_id
    ].playback_manager.voice_client.is_connected():
        await interaction.edit_original_response(
            content="le bot n'est même pas connecté :wilted_rose:"
        )
    await globals.guilds[interaction.guild_id].playback_manager.stop()

    await interaction.edit_original_response(
        content="Musique arrêtée et file d'attente effacée."
    )
