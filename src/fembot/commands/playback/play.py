import discord

from ...utils import auth, globals


@globals.tree.command(name="play", description="Joue une musique de la file d'attente.")
@discord.app_commands.describe(
    rank="La position dans la file d'attente de la musique à jouer."
)
@auth.auth()
async def play(interaction: discord.Interaction, rank: int = 1) -> None:
    if (
        interaction.user.voice == None
        or type(interaction.user.voice.channel) != discord.VoiceChannel
    ):
        interaction.edit_original_response(content="Tu n'es pas dans un salon vocal.")
        return
    if (
        not globals.guilds[
            interaction.guild_id
        ].playback_manager.is_ready_for_playback()
        or globals.guilds[interaction.guild_id].playback_manager.voice_client.channel
        != interaction.user.voice.channel
    ):
        await globals.guilds[interaction.guild_id].playback_manager.connect(
            interaction.user.voice.channel
        )
        await interaction.edit_original_response(content="Connection au salon vocal...")
    elif (
        rank == 1
        and globals.guilds[
            interaction.guild_id
        ].playback_manager.voice_client.is_paused()
    ):
        globals.guilds[interaction.guild_id].playback_manager.voice_client.resume()
        await interaction.edit_original_response(content="Reprise de la musique...")
        return
    for i in globals.guilds[interaction.guild_id].playback_manager.playlist:
        if (
            globals.guilds[interaction.guild_id].playback_manager.playlist[i].rank
            == rank
        ):
            globals.guilds[interaction.guild_id].playback_manager.play(i)
            await interaction.edit_original_response(
                content=f"Lancement de `{globals.guilds[interaction.guild_id].playback_manager.playlist[i].pretty_name}`..."
            )
            return

    await interaction.edit_original_response(
        content=f"Il n'y a pas de musique au rang {rank}. Utilise `/queue` pour en rajouter !"
    )
