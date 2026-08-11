# contrary to v2, i'm going to separate the logic for message responses from the logic for garmin commands
import time

import discord

from ..utils import auth, globals


async def kill(message: discord.Message, time):
    """ok garmin...... kill this man :sad:"""
    if message.type == discord.MessageType.reply:
        if message.reference != None:
            if message.reference.resolved is discord.Message:
                if message.reference.resolved.author.id == globals.client.user.id:
                    await message.reply("i'm crine :sob:")
                    return False
                elif message.reference.resolved.author.guild_permissions.administrator:
                    await message.reply("Tié con toi")
                    return False
                else:
                    await message.reference.resolved.author.timeout(time)
                    return True

            elif message.reference.resolved is discord.DeletedReferencedMessage:
                await message.reply("The User Has Escaped")
            elif message.reference.cached_message:
                if message.reference.cached_message.author.id == globals.client.user.id:
                    await message.reply("i'm crine :sob:")
                    return False
                elif message.reference.cached_message.author.guild_permissions.administrator:
                    await message.reply("Tié con toi")
                    return False
                else:
                    await message.reference.cached_message.author.timeout(time)
                    return True
            else:
                msg = None
                try:
                    msg = await message.channel.fetch_message(
                        message.reference.message_id
                    )
                except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                    msg = None
                if msg:
                    if msg.author.id == globals.client.user.id:
                        await message.reply("i'm crine :sob:")
                        return False
                    elif msg.author.guild_permissions.administrator:
                        await message.reply("Tié con toi")
                        return False

                    else:
                        await msg.author.timeout(time)
                        return True
                else:
                    await message.reply("who is this :sob:")
        else:
            await message.reply(
                "cette réponse ne fait référence à aucun message (ballz ????) parce que `message.reference` vaut `"
                + str(message.reference)
                + "`"
            )
    else:
        await message.reply("ce message n'est PAS une réponse")

    return False


class GarminParser:
    token_list: list[str]
    current_token = -1
    message: discord.Message

    def consume_token(self, amount: int = 1) -> str:

        token_added = 0
        out = ""
        while (
            amount < 0 and self.current_token + token_added < len(self.token_list)
        ) or (
            token_added < amount
            and self.current_token + token_added < len(self.token_list)
        ):
            token_added += 1
            out += self.token_list[self.current_token + token_added] + " "

        self.current_token += token_added

        return out.strip()

    async def check_perms(self, perms: auth.PermissionLevel) -> bool:
        user_perms: auth.PermissionLevel = await auth.get_highest_permission(
            self.message.author, self.message.guild
        )
        if user_perms.value >= perms.value:
            return True
        else:
            self.message.reply(
                content=f"random kid :sob: (you need `{perms.name}` perms but you only have `{user_perms.name}`)"
            )
            return False

    def __init__(self, message: discord.Message) -> None:
        self.message = message
        self.token_list = message.content.lower().split()

    async def process(self) -> None:
        if self.consume_token() != "ok":
            return
        if self.consume_token() != "garmin":
            return
        match self.consume_token():
            case "edit-setting":
                if not await self.check_perms(auth.PermissionLevel.ADMIN):
                    return
                await self.message.reply(content="coming")
                return
            case "say":
                if not await self.check_perms(auth.PermissionLevel.MEMBER):
                    return
                await self.message.reply(content=self.consume_token(-1))
                return
            case "kill":
                if not await self.check_perms(auth.PermissionLevel.MOD):
                    return
                if await kill(self.message, 3600):
                    await self.message.reply(
                        "sending in firing squad....... user has been timed out for an hour."
                    )
                return
            case "triple":
                if self.consume_token(3) != "dog death barrage":
                    return
                if not await self.check_perms(auth.PermissionLevel.TRUSTED_MEMBER):
                    return
                if await kill(self.message, 60):
                    await self.message.reply(
                        "... timed out user for a minute.",
                        file=discord.File(globals.TRIPLE_DOG_DEATH_BARRAGE),
                    )
            case "stfu":
                if not await self.check_perms(auth.PermissionLevel.TRUSTED_MEMBER):
                    return
                globals.guilds[self.message.guild.id].stfu_timestamp = (
                    time.time() + 60 * 60
                )
                await self.message.reply("\\:( i'll be quiet for an hour :wilted_rose:")
                return
            case "unstfu":
                if not await self.check_perms(auth.PermissionLevel.TRUSTED_MEMBER):
                    return
                globals.guilds[self.message.guild.id].stfu_timestamp = 0
                await self.message.reply("stupit")
                return
            case "help":
                out: str = ""
                user_perms: auth.PermissionLevel = await auth.get_highest_permission(
                    self.message.author, self.message.guild
                )
                if user_perms < auth.PermissionLevel.MEMBER:
                    out += "You Are Banned From Fembot."
                if user_perms >= auth.PermissionLevel.MEMBER:
                    out += """`MEMBER` commands :
`ok garmin say <thing>`
    -> makes fembot say <thing>
`ok garmin HELP`
    -> displays this message\n\n"""
                if user_perms >= auth.PermissionLevel.TRUSTED_MEMBER:
                    out += """`TRUSTED_MEMBER` commands :
`ok garmin stfu`
    -> makes fembot not reply to messages for an hour
`ok garmin unstfu`
    -> cancels the previous command
`ok garmin triple dog death barrage`
    -> mutes the user the og message is replying to for a minute\n\n"""
                if user_perms >= auth.PermissionLevel.MOD:
                    out += """`MOD` commands :
`ok garmin kill`
    -> mutes the user the og message is replying to for an hour\n\n"""
                if user_perms >= auth.PermissionLevel.ADMIN:
                    out += """`ADMIN` commands :
`ok garmin list-settings`
    -> shows the available server settings and their values
`ok garmin edit-setting <setting> <new-value>`
    -> edits the server setting <setting> and sets it to <new-value>\n\n"""
                await self.message.reply(content=out)
                return
            case _:
                await self.message.reply(content="what")
                return
