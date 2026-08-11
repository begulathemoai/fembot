import functools
from enum import Enum
from typing import Any

import discord

from . import globals


class PermissionLevel(Enum):
    BOT_BANNED = -10
    SERVER_BANNED = -5
    MEMBER = 0
    TRUSTED_MEMBER = 5
    MOD = 10
    ADMIN = 15
    SERVER_OWNER = 20
    BOT_OWNER = 25

    def __eq__(self, __value: object) -> bool:
        if type(__value) is PermissionLevel:
            return self.value == __value.value
        elif type(__value) is int:
            return self.value == __value
        else:
            raise TypeError(
                f"PermissionLevel can't be compared with {type(__value).__name__}"
            )

    def __gt__(self, __value: object) -> bool:
        if type(__value) is PermissionLevel:
            return self.value > __value.value
        elif type(__value) is int:
            return self.value > __value
        else:
            raise TypeError(
                f"PermissionLevel can't be compared with {type(__value).__name__}"
            )

    def __ge__(self, __value: object) -> bool:
        if type(__value) is PermissionLevel:
            return self.value >= __value.value
        elif type(__value) is int:
            return self.value >= __value
        else:
            raise TypeError(
                f"PermissionLevel can't be compared with {type(__value).__name__}"
            )

    def __le__(self, __value: object) -> bool:
        if type(__value) is PermissionLevel:
            return self.value <= __value.value
        elif type(__value) is int:
            return self.value <= __value
        else:
            raise TypeError(
                f"PermissionLevel can't be compared with {type(__value).__name__}"
            )

    def __lt__(self, __value: object) -> bool:
        if type(__value) is PermissionLevel:
            return self.value < __value.value
        elif type(__value) is int:
            return self.value < __value
        else:
            raise TypeError(
                f"PermissionLevel can't be compared with {type(__value).__name__}"
            )


async def get_highest_permission(
    member: discord.Member | discord.User, guild: discord.Guild
) -> PermissionLevel:
    if member.id == globals.owner_id:
        return PermissionLevel.BOT_OWNER
    elif member.id == guild.owner_id:
        return PermissionLevel.SERVER_OWNER
    elif (
        type(member) is discord.Member
        and member.guild_permissions.administrator
        or (
            type(member) is discord.User
            and (await guild.fetch_member(member.id)).guild_permissions.administrator
        )
    ):
        return PermissionLevel.ADMIN
    elif (
        type(member) is discord.Member
        and member.guild_permissions.manage_messages
        or (
            type(member) is discord.User
            and (await guild.fetch_member(member.id)).guild_permissions.manage_messages
        )
    ):
        return PermissionLevel.MOD
    elif member.id in globals.bot_banned_users:
        return PermissionLevel.BOT_BANNED
    else:
        return PermissionLevel.MEMBER


def auth(
    auth_level: PermissionLevel = PermissionLevel.MEMBER, ephemeral: bool | None = None
):
    def actual_decorator(func):
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any):
            interaction: discord.Interaction

            if (
                "interaction" in kwargs
                and type(kwargs["interaction"]) is discord.Interaction
            ):
                interaction = kwargs["interaction"]
            elif len(args) > 0 and type(args[0]) is discord.Interaction:
                interaction = args[0]
            else:
                raise TypeError(
                    'Une interaction Discord devrait être fournie soit en premier argument, soit en keyword argument de nom "interaction".'
                )

            if not globals.is_guild_allowed(interaction.guild_id):
                await interaction.response.send_message(
                    "cette instance de fembot n'est pas disponible sur ce serveur",
                    ephemeral=True,
                )
                return True

            user_level: PermissionLevel = await get_highest_permission(
                interaction.user, interaction.guild
            )
            if user_level == PermissionLevel.BOT_BANNED:
                await interaction.response.send_message(
                    "Tu es banni de cette instance de fembot. Envoie un DM à son owner si tu penses que c'est une erreur.",
                    ephemeral=True,
                )
                return True
            elif user_level == PermissionLevel.SERVER_BANNED:
                await interaction.response.send_message(
                    "Ce serveur t'a enlevé l'accès à fembot. Contacte l'owner si tu penses que c'est une erreur.",
                    ephemeral=True,
                )
                return True
            elif user_level.value < auth_level.value:
                await interaction.response.send_message(
                    f"Tu n'as pas les permissions requises pour pouvoir exécuter cette commande. Permissions requises : {auth_level.name}; Permissions actuelles : {user_level.name}",
                    ephemeral=True,
                )
                return True
            elif not globals.ready:
                await interaction.response.send_message(
                    "fembot est encore en cours de lancement, merci d'attendre...",
                    ephemeral=True,
                )
                return True

            actual_ephemeral: bool = False
            if ephemeral is bool:
                actual_ephemeral = ephemeral

            if (
                ephemeral == None
                and "ephemeral" in kwargs
                and type(kwargs["ephemeral"]) is bool
            ):
                actual_ephemeral = kwargs["ephemeral"]

            await interaction.response.send_message(
                "Commande authentifiée...", ephemeral=actual_ephemeral
            )

            try:
                out = await func(*args, **kwargs)
            except Exception as e:
                err_out = (
                    f"fembot a rencontré une erreur :\n**{type(e).__name__}** : {e!s}"
                )
                if globals.owner_id != -1:
                    err_out += f"\n-# ||<@{globals.owner_id}>||"
                else:
                    err_out += "\n-# ||no owner id specified||"
                await interaction.edit_original_response(content=err_out)
                raise
            return out

        return wrapper

    return actual_decorator
