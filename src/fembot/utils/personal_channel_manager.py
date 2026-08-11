import discord

__all__ = ("PersonalChannelManager",)


class PersonalChannelManager:
    guild: discord.Guild

    new_personal_channel_category_id: int = 0

    overwrite: discord.PermissionOverwrite = discord.PermissionOverwrite(
        read_messages=True,
        manage_channels=True,
        manage_permissions=True,
        manage_webhooks=True,
        create_instant_invite=True,
        send_messages=True,
        send_messages_in_threads=True,
        send_polls=True,
        create_private_threads=True,
        create_public_threads=True,
        embed_links=True,
        attach_files=True,
        add_reactions=True,
        use_external_emojis=True,
        use_external_stickers=True,
        mention_everyone=True,
        manage_messages=True,
        manage_threads=True,
        read_message_history=True,
        send_tts_messages=True,
        send_voice_messages=True,
        create_polls=True,
        use_external_apps=True,
        use_application_commands=True,
        use_embedded_activities=True,
    )

    def __init__(self, guild: discord.Guild) -> None:
        self.guild = guild
