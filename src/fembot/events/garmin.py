# contrary to v2, i'm going to separate the logic for message responses from the logic for garmin commands
import datetime
import time

import discord

from ..utils import auth, downloaders, exceptions, globals, playback, utils


async def kill(message: discord.Message, time: datetime.timedelta):
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
            amount < 0 and self.current_token + token_added + 1 < len(self.token_list)
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
            await self.message.reply(
                content=f"random kid :sob: (you need `{perms.name}` perms but you only have `{user_perms.name}`)"
            )
            return False

    def __init__(self, message: discord.Message) -> None:
        self.message = message
        self.token_list = message.content.split()

    async def process(self) -> None:
        try:
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
                    if await kill(self.message, datetime.timedelta(hours=1)):
                        await self.message.reply(
                            "sending in firing squad....... user has been timed out for an hour."
                        )
                    return
                case "triple":
                    if self.consume_token(3) != "dog death barrage":
                        return
                    if not await self.check_perms(auth.PermissionLevel.TRUSTED_MEMBER):
                        return
                    if await kill(self.message, datetime.timedelta(minutes=1)):
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
                    await self.message.reply(
                        "\\:( i'll be quiet for an hour :wilted_rose:"
                    )
                    return
                case "unstfu":
                    if not await self.check_perms(auth.PermissionLevel.TRUSTED_MEMBER):
                        return
                    globals.guilds[self.message.guild.id].stfu_timestamp = 0
                    await self.message.reply("stupit")
                    return
                case "list-aliases":
                    if not await self.check_perms(auth.PermissionLevel.TRUSTED_MEMBER):
                        return
                    out = ""
                    for i in globals.guilds[self.message.guild.id].aliases:
                        out += f"**{i}** : {utils.make_x_chars_long(globals.guilds[self.message.guild.id].aliases[i], 50)}\n"
                    await self.message.reply(
                        out if out != "" else "There are no registered aliases."
                    )
                case "add-alias":
                    if not await self.check_perms(auth.PermissionLevel.MOD):
                        return
                    name = self.consume_token()
                    if name == "":
                        await self.message.reply(
                            "no name provided for alias\n-> format should be `ok garmin add-alias <name> <content>`"
                        )
                        return
                    content = self.message.content.removeprefix(
                        "ok garmin add-alias " + name
                    ).removeprefix(" ")
                    if content == "":
                        await self.message.reply(
                            "no content provided for alias\n-> format should be `ok garmin add-alias <name> <content>`"
                        )
                        return
                    if globals.guilds[self.message.guild.id].add_alias(name, content):
                        await self.message.reply("alias added successfully")
                        return
                    else:
                        await self.message.reply("this alias was already defined")
                        return
                case "remove-alias":
                    if not await self.check_perms(auth.PermissionLevel.MOD):
                        return
                    name = self.consume_token()
                    if name == "":
                        await self.message.reply(
                            "no name provided for alias to remove\n-> format should be `ok garmin remove-alias <name>`"
                        )
                        return
                    if globals.guilds[self.message.guild.id].remove_alias(name):
                        await self.message.reply("alias removed successfully")
                        return
                    else:
                        await self.message.reply("this alias does not exist")
                        return
                case "debug-connect":
                    if not await self.check_perms(auth.PermissionLevel.TRUSTED_MEMBER):
                        return
                    voice_channel = None
                    try:
                        voice_channel = (
                            await self.message.author.fetch_voice()
                        ).channel
                    except discord.NotFound:
                        await self.message.reply("you are not in a vc")
                        return
                    if type(voice_channel) is not discord.VoiceChannel:
                        await self.message.reply(
                            "you are not in a vc (stages don't count)"
                        )
                        return
                    await globals.guilds[
                        self.message.guild.id
                    ].playback_manager.connect(voice_channel)
                    await self.message.reply("connected")
                    return
                case "debug-play":
                    if not await self.check_perms(auth.PermissionLevel.TRUSTED_MEMBER):
                        return
                    uid = self.consume_token()
                    if not globals.guilds[
                        self.message.guild.id
                    ].playback_manager.is_ready_for_playback():
                        await self.message.reply("fembot is not connected to any vc")
                        return
                    globals.guilds[self.message.guild.id].playback_manager.play(uid)
                    await self.message.reply(
                        "now playing uid `"
                        + uid
                        + f"` ({
                            globals.guilds[self.message.guild.id]
                            .playback_manager.playlist[uid]
                            .filename
                        })"
                    )
                    return
                case "debug-load":
                    if not await self.check_perms(auth.PermissionLevel.TRUSTED_MEMBER):
                        return
                    filename = self.consume_token(-1)

                    uid = globals.guilds[
                        self.message.guild.id
                    ].playback_manager.prepare(filename)
                    await self.message.reply(
                        "loaded " + filename + " as uid `" + uid + "`"
                    )
                    return
                case "debug-download":
                    if not await self.check_perms(auth.PermissionLevel.TRUSTED_MEMBER):
                        return
                    if len(self.message.attachments) == 0:
                        await self.message.reply(
                            "you have to attach an mp3 or wav file"
                        )
                        return
                    out = ""
                    for i in self.message.attachments:
                        if i.content_type not in [
                            "audio/mpeg",
                            "audio/mp3",
                            "audio/wav",
                            "audio/x-wav",
                            "audio/mpeg3",
                        ]:
                            out += f"Invalid file format. {i.content_type} is not supported by fembot.\n"
                        else:
                            downloader = downloaders.attachment.AttachmentDownloader(
                                self.message.guild, i
                            )
                            uid: str = ""
                            try:
                                uid = await downloader.download()
                            except exceptions.FileTooBigError:
                                out += "The file was too big.\n"
                            else:
                                globals.guilds[
                                    self.message.guild.id
                                ].playback_manager.prepare(
                                    uid,
                                    i.filename,
                                    playback.playback_manager_song.SourceType.ATTACHMENT,
                                    i,
                                    "",
                                    uid,
                                )
                                out += f"File downloaded as uid `{uid}`.\n"
                    await self.message.reply(out)
                    return
                case "make-trusted":
                    if not await self.check_perms(auth.PermissionLevel.MOD):
                        return
                    id: int
                    try:
                        id = int(self.consume_token())
                    except TypeError:
                        await self.message.reply("Aucun id n'a pu être lu.")
                        return
                    if globals.guilds[self.message.guild.id].add_trusted(id):
                        await self.message.reply(
                            f"L'utilisateur d'id `{id}` a été ajouté aux utilisateurs de confiance."
                        )
                        return
                    else:
                        await self.message.reply(
                            f"L'utilisateur d'id `{id}` est déjà un utilisateur de confiance."
                        )
                        return
                case "demake-trusted":
                    if not await self.check_perms(auth.PermissionLevel.MOD):
                        return
                    id: int
                    try:
                        id = int(self.consume_token())
                    except TypeError:
                        await self.message.reply("Aucun id n'a pu être lu.")
                        return
                    if globals.guilds[self.message.guild.id].remove_trusted(id):
                        await self.message.reply(
                            f"L'utilisateur d'id `{id}` a été ajouté aux utilisateurs de confiance."
                        )
                        return
                    else:
                        await self.message.reply(
                            f"L'utilisateur d'id `{id}` n'est pas un utilisateur de confiance."
                        )
                        return
                case "help":
                    out: str = ""
                    user_perms: auth.PermissionLevel = (
                        await auth.get_highest_permission(
                            self.message.author, self.message.guild
                        )
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
    -> mutes the user the og message is replying to for a minute
**the following commands are all very temporary until i make something better:**
`ok garmin debug-connect`
    -> connects fembot to the same VC as you (you have to be in a vc of course)
`ok garmin debug-load`
    -> loads a file from the guild playback folder (no you don't have any way of knowing the file names so this is useless for you)
`ok garmin debug-download`
    -> downloads all attachments and adds them to the playlist. (they have to be mp3 or wav)
`ok garmin debug-play <uid>`
    -> plays the file of uid <uid>\n\n"""
                    if user_perms >= auth.PermissionLevel.MOD:
                        out += """`MOD` commands :
`ok garmin kill`
    -> mutes the user the og message is replying to for an hour
`ok garmin add-alias <name> <content>`
    -> adds an alias named <name> with content <content> that can be called back using `.<name>`
`ok garmin remove-alias <name>`
    -> removes the alias named <name> if it exists
`ok garmin list-aliases`
    -> returns all registered aliases
`ok garmin make-trusted <id>`
    -> adds the user of id <id> to the list of trusted members.
`ok garmin demake-trusted <id>`
    -> removes the user of id <id> from the list of trusted members.\n\n"""
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
        except Exception as e:
            await self.message.reply(
                content=f"This garmin command has encountered an error\n **{type(e).__name__}**: {e!s}"
            )
            raise
