import discord

from ...utils import auth, globals


@globals.tree.command(name="pause", description="Pause la musique.")
@discord.app_commands.describe()
@auth.auth()
async def play(interaction: discord.Interaction) -> None:
    if (
        interaction.user.voice == None
        or type(interaction.user.voice.channel) != discord.VoiceChannel
    ):
        await interaction.edit_original_response(
            content="Tu n'es pas dans un salon vocal."
        )
        return
    if not globals.guilds[
        interaction.guild_id
    ].playback_manager.voice_client.is_playing():
        await interaction.edit_original_response(
            content="Aucune musique n'est en cours de lecture."
        )
        return
    globals.guilds[interaction.guild_id].playback_manager.voice_client.pause()
    await interaction.edit_original_response(content="Musique pausée.")
