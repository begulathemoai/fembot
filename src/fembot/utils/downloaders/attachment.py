import discord

from ...utils import exceptions, globals, storage


class AttachmentDownloader:
    guild: discord.Guild
    attachment: discord.Attachment

    def __init__(self, guild: discord.Guild, attachment: discord.Attachment) -> None:
        self.guild = guild
        self.attachment = attachment

    async def download(self) -> str:
        if self.attachment.size > globals.individual_song_size_limit:
            raise exceptions.FileTooBigError(
                f"The file was of size {self.attachment.size} while the maximum for this instance of fembot is {globals.individual_song_size_limit}."
            )
        filename = globals.guilds[self.guild.id].playback_manager.gen_and_reserve_uid()
        await self.attachment.save(
            storage.get_playback_storage_path(self.guild.id) + "/" + filename
        )
        return filename
