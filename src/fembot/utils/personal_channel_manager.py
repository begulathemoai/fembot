import discord


class PersonalChannelManager:
    guild: discord.Guild

    def __init__(self, guild: discord.Guild) -> None:
        self.guild = guild
