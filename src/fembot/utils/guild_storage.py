import discord

from . import storage


class GuildStorage:
    guild: discord.Guild
    stfu_timestamp: int = 0
    # TODO
    # playback_manager: PlaybackManager
    # TODO
    # personal_channel_manager: PersonalChannelManager
    no_ping_replies_enabled: bool = False
    unprompted_no_ping_replies_enabled: bool = False

    # does nothing but getting ready for impl
    personal_channels_enabled: bool = False
    new_personal_channel_category_id: int = 0

    def __init__(self, guild: discord.Guild) -> None:
        self.guild = guild
        if not storage.has_guild(guild.id):
            storage.add_guild(guild.id)
        else:
            data = storage.get_guild(guild.id)
            if "new_channel_category_id" in data:
                self.new_personal_channel_category_id = data["new_channel_category_id"]
            if "personal_channels_enabled" in data:
                self.personal_channels_enabled = bool(data["personal_channels_enabled"])
            if "no_ping_replies_enabled" in data:
                self.no_ping_replies_enabled = bool(data["no_ping_replies_enabled"])
            if "unprompted_no_ping_replies_enabled" in data:
                self.unprompted_no_ping_replies_enabled = bool(
                    data["unprompted_no_ping_replies_enabled"]
                )

    def update_storage(self) -> None:
        storage.set_guild(
            self.guild.id,
            "new_channel_category_id",
            self.new_personal_channel_category_id,
        )
        storage.set_guild(
            self.guild.id,
            "personal_channels_enabled",
            int(self.personal_channels_enabled),
        )
        storage.set_guild(
            self.guild.id,
            "no_ping_replies_enabled",
            int(self.no_ping_replies_enabled),
        )
        storage.set_guild(
            self.guild.id,
            "unprompted_no_ping_replies_enabled",
            int(self.unprompted_no_ping_replies_enabled),
        )
