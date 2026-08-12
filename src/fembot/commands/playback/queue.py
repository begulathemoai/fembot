import discord

from ...utils import auth, downloaders, exceptions, globals, playback


@globals.tree.command(
    name="queue", description="Ajoute un fichier mp3/wav dans la file d'attente."
)
@discord.app_commands.describe(file="Le fichier à ajouter.")
@auth.auth()
async def queue(
    interaction: discord.Interaction, file: discord.Attachment = None
) -> None:
    if file != None:
        await interaction.edit_original_response(
            content="Running in attachment mode..."
        )
        if file.content_type not in [
            "audio/mpeg",
            "audio/mp3",
            "audio/wav",
            "audio/x-wav",
            "audio/mpeg3",
        ]:
            await interaction.edit_original_response(
                content="No supported file format found."
            )
            return

        dl: downloaders.attachment.AttachmentDownloader = (
            downloaders.attachment.AttachmentDownloader(interaction.guild, file)
        )
        uid: str = ""
        try:
            uid = await dl.download()
        except exceptions.FileTooBigError:
            await interaction.edit_original_response(
                content="This file is too big to download"
            )
            return
        globals.guilds[interaction.guild_id].playback_manager.prepare(
            uid,
            file.filename,
            playback.playback_manager_song.SourceType.ATTACHMENT,
            file,
            "",
            uid,
        )
        await interaction.edit_original_response(
            content=f"`{file.filename}` was downloaded and placed at rank {globals.guilds[interaction.guild_id].playback_manager.playlist[uid].rank}."
        )
        return
    else:
        await interaction.edit_original_response(
            content="No supported download type found."
        )
