import os
import random

import discord

from ...utils import exceptions, storage
from . import playback_manager_song


class PlaybackManager:
    guild: discord.Guild
    playlist: dict[str, playback_manager_song.PlaybackManagerSong]
    current_uid: str = ""
    current_song: playback_manager_song.PlaybackManagerSong = None
    next_up_uid: str = ""
    next_up_song: playback_manager_song.PlaybackManagerSong = None
    voice_client: discord.VoiceClient = None
    audio_source: discord.FFmpegOpusAudio = None
    max_rank: int = 0
    reserved_uids: list[str]

    def __init__(self, guild: discord.Guild) -> None:
        self.guild = guild
        self.playlist = {}
        self.reserved_uids = []

    def is_ready_for_playback(self) -> bool:
        return self.voice_client != None and self.voice_client.is_connected()

    async def connect(self, vc: discord.VoiceChannel):
        self.voice_client = await vc.connect(self_deaf=True, reconnect=True)

    def gen_and_reserve_uid(self):
        def uid():
            return (
                random.choice(
                    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345789_-"
                )
                + random.choice(
                    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345789_-"
                )
                + random.choice(
                    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345789_-"
                )
            )

        new_uid = uid()
        while new_uid in self.reserved_uids:
            new_uid = uid()
        self.reserved_uids.append(new_uid)
        return new_uid

    def prepare(
        self,
        filename: str,
        pretty_name: str = "",
        type: playback_manager_song.SourceType = playback_manager_song.SourceType.OTHER,
        ref=None,
        url: str = "",
        uid: str = "",
    ) -> str:
        new_uid: str
        if uid == "":
            new_uid = self.gen_and_reserve_uid()
        else:
            new_uid = uid
        self.reserved_uids.append(new_uid)
        rank = self.max_rank + 1
        self.max_rank = self.max_rank + 1
        new_pbm = playback_manager_song.PlaybackManagerSong(
            filename, pretty_name, type, ref, url, new_uid, rank
        )
        self.playlist[new_uid] = new_pbm

        self.refresh_playlist()
        return new_uid

    def refresh_playlist(self):
        if self.current_song == None:
            return
        cur_rank = self.current_song.rank
        was_set: bool = False
        for i in self.playlist:
            if self.playlist[i].rank == cur_rank + 1:
                self.next_up_song = self.playlist[i]
                self.next_up_uid = i
                was_set = True
                break
        if not was_set:
            self.next_up_song = None
            self.next_up_uid = ""

    def play(self, uid: str) -> bool:
        if not self.is_ready_for_playback():
            raise exceptions.NotConnectedError(
                "This PlaybackManager is not connected to any voice channel."
            )
        if uid not in self.playlist:
            raise ValueError("No such uid was found.")

        full_path: str = (
            storage.get_playback_storage_path(self.guild.id)
            + "/"
            + self.playlist[uid].filename
        )
        if not os.path.exists(full_path):
            raise OSError(f"No file named {self.playlist[uid].filename} was found.")
        self.audio_source = discord.FFmpegOpusAudio(full_path)
        self.current_uid = uid
        self.current_song = self.playlist[uid]
        self.refresh_playlist()
        if self.voice_client.is_playing():
            self.voice_client.stop()
        self.voice_client.play(self.audio_source, after=self.after_play_callback)

    async def stop(self):

        if self.voice_client.is_playing():
            self.voice_client.stop()
        if self.voice_client.is_connected():
            await self.voice_client.disconnect()
        self.playlist.clear()
        self.max_rank = 0
        self.current_song = None
        self.current_uid = ""
        self.next_up_song = None
        self.next_up_uid = ""
        storage.clear_playback_folder(self.guild.id)

    def after_play_callback(self, error: Exception) -> None:
        if self.next_up_uid != "":
            self.play(self.next_up_uid)
