## i just copied shit from the v2
## i mean it works (?)

import datetime
import random
import re
import time

import discord

from ..utils import globals, utils

feur_counter = 50
jojo_counter = 250


async def kill(message: discord.Message, admin: bool, time):
    if message.author.guild_permissions.administrator or not admin:
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
                    if (
                        message.reference.cached_message.author.id
                        == globals.client.user.id
                    ):
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
    else:
        await message.reply("random kid :sob:")
    return False


async def check_message(
    message: discord.Message, *content, name: bool = True, or_answer: bool = True
) -> bool:
    check = True
    ct = message.content.lower()
    if not globals.guilds[message.guild.id].no_ping_replies_enabled:
        return False
    if (
        not name
        and not globals.guilds[message.guild.id].unprompted_no_ping_replies_enabled
    ):
        return False
    if name and check:
        if or_answer:
            c2 = False
            if "fembot" in ct or f"<@{globals.client.user.id}>" in ct:
                c2 = True
            if not c2 and (
                message.reference != None
                and (
                    await message.channel.fetch_message(message.reference.message_id)
                ).author
                == globals.client.user
            ):
                c2 = True
            check = c2
        else:
            c2 = False
            if "fembot" in ct or f"<@{globals.client.user.id}>" in ct:
                c2 = True
            check = c2

    for i in content:
        if type(i) is str:
            if not utils.check_string(ct, i.lower()):
                check = False
        elif type(i) is list:
            check2 = True
            for j in i:
                if not utils.check_string(ct, j.lower()):
                    check2 = False
            if not check2:
                check = False
    return check


def regex_checker(p_input: str, rgx: list) -> bool:
    check = False
    for i in rgx:
        if re.search(i, p_input) is not None:
            check = True
    print("check")
    return check


@globals.client.event
async def on_message(message: discord.Message):
    global feur_counter, jojo_counter
    if not globals.is_test_server(message.guild):
        return
    if not globals.ready:
        return
    if message.author == globals.client.user:
        return

    if await check_message(
        message, "is/ok garmin unshut the fuck up", name=False
    ) or await check_message(message, "is/ok garmin unstfu", name=False):
        globals.guilds[message.guild.id].stfu_timestamp = 0
        await message.reply("stupit")
        return
    if time.time() < globals.guilds[message.guild.id].stfu_timestamp:
        return
    if (
        await check_message(message, ["panto:pant:pnato:pnat"], name=False)
        and message.guild.id == 1083133673752231956  # mine server
    ):
        await message.add_reaction(await message.guild.fetch_emoji(1280558914449965106))
    if (
        await check_message(message, ["buseur:suseur:subeur"], name=False)
        and message.guild.id == 1083133673752231956
    ):
        await message.add_reaction(await message.guild.fetch_emoji(1496242945878397018))
    if (
        await check_message(message, ["buga:begu:begula:begulathemoai"], name=False)
        and message.guild.id == 1083133673752231956
    ):
        await message.add_reaction(await message.guild.fetch_emoji(1280559079198167041))
    if regex_checker(
        message.content.lower(), globals.YOUTUBE_TRACKING_REGEXES
    ) and await check_message(message, "", name=False):
        await message.reply(
            "sonion, le lien youtube que tu as envoyé contient du tracking (tout ce qui est derrière le si= ou &si=). je te conseille de l'enlever parce que sinon tous ceux qui cliqueront dessus seront reliés à toi (dont buseur :wilted_rose:).",
            file=discord.File("./trackingyt.jpg"),
        )
    elif regex_checker(
        message.content.lower(), [globals.NWORD_REGEX, globals.NWORD_REGEX_BUT_FRENCH]
    ) and await check_message(message, "", name=False):
        await message.reply(
            "BUGALERTE :bangbang::bangbang::bangbang::bangbang::bangbang::bangbang::bangbang::bangbang::bangbang::bangbang::bangbang:\n-# ||<@802854414300741633> ||\n-# https://cdn.discordapp.com/attachments/1347560244229832728/1407457407176675568/meme.gif"
        )

    elif await check_message(message, "startswith/ok garmin ", name=False):
        if await check_message(
            message, "is/ok garmin shut the fuck up", name=False
        ) or await check_message(message, "is/ok garmin stfu", name=False):
            globals.guilds[message.guild.id].stfu_timestamp = time.time() + 60 * 60
            await message.reply("\\:( i'll be quiet for an hour :wilted_rose:")
        elif await check_message(message, "is/ok garmin kill this man", name=False):
            if await kill(message, True, datetime.timedelta(hours=1)):
                await message.reply(
                    "sending in firing squad....... user has been timed out for an hour."
                )
        elif await check_message(
            message, "is/ok garmin triple dog death barrage", name=False
        ):
            if await kill(message, False, datetime.timedelta(minutes=1)):
                await message.reply(
                    "... timed out user for a minute.",
                    file=discord.File("./tripledog.jpg"),
                )
        elif await check_message(message, "startswith/ok garmin say ", name=False):
            await message.reply(message.content.lower().removeprefix("ok garmin say "))
        elif await check_message(message, "startswith/ok garmin help", name=False):
            await message.reply("""garmin mode help :
`ok garmin stfu`
    -> stops the bot from replying for an hour (everyone)
`ok garmin unstfu`
    -> disables stfu mode (everyone)
`ok garmin kill this man`
    -> times out the user the og message is replying to for an hour (admin)
`ok garmin triple dog death barrage`
    -> times out the user the og message is replying to for a minute (everyone)
`ok garmin HELP`
    -> displays this message (everyone)
`ok garmin <literally anything else>`
    -> confuses the bot (every... one?)""")
        else:
            await message.reply("what")
    elif await check_message(message, "is/good morning", name=False):
        await message.reply("it's afternoon")
    elif (
        await check_message(message, "kirk", name=False)
        and globals.guilds[message.guild.id].enable_the_kirk
    ):
        result = globals.guilds[message.guild.id].get_kirky_message()
        if result is None:
            await message.reply(
                "We Are Charlie KIRKKKKKKKKKKK WE CARRY THE FLAME WE'LL FIGHT FOR THE GOSPEL WE'LL HONOR HIS NAMEEEEEEE"
            )
        else:
            await message.reply(result)
    elif await check_message(message, "i", "can't", "it", "anymore", name=False):
        await message.reply("IS THAT A MOTHERFUCKING CAMELLIA REFERENCE ?????")
    elif await check_message(message, "attention", name=False):
        await message.reply("""⣿⣿⣿⣿⣿⠟⠋⠄⠄⠄⠄⠄⠄⠄⢁⠈⢻⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠃⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⡀⠭⢿⣿⣿⣿⣿
⣿⣿⣿⣿⡟⠄⢀⣾⣿⣿⣿⣷⣶⣿⣷⣶⣶⡆⠄⠄⠄⣿⣿⣿⣿
⣿⣿⣿⣿⡇⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠄⠄⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣇⣼⣿⣿⠿⠶⠙⣿⡟⠡⣴⣿⣽⣿⣧⠄⢸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣾⣿⣿⣟⣭⣾⣿⣷⣶⣶⣴⣶⣿⣿⢄⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⣩⣿⣿⣿⡏⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣹⡋⠘⠷⣦⣀⣠⡶⠁⠈⠁⠄⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣍⠃⣴⣶⡔⠒⠄⣠⢀⠄⠄⠄⡨⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣦⡘⠿⣷⣿⠿⠟⠃⠄⠄⣠⡇⠈⠻⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠟⠋⢁⣷⣠⠄⠄⠄⠄⣀⣠⣾⡟⠄⠄⠄⠄⠉⠙⠻
⡿⠟⠋⠁⠄⠄⠄⢸⣿⣿⡯⢓⣴⣾⣿⣿⡟⠄⠄⠄⠄⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠄⠄⣿⡟⣷⠄⠹⣿⣿⣿⡿⠁⠄⠄⠄⠄⠄⠄⠄⠄

ATTENTION CITIZEN! 市民请注意!

This is the Central Intelligentsia of the Chinese Communist Party. 您的 Internet 浏览器历史记录和活动引起了我们的注意。 YOUR INTERNET ACTIVITY HAS ATTRACTED OUR ATTENTION. 因此，您的个人资料中的 11115 ( -11115 Social Credits) 个社会积分将打折。 DO NOT DO THIS AGAIN! 不要再这样做! If you do not hesitate, more Social Credits ( -11115 Social Credits )will be subtracted from your profile, resulting in the subtraction of ration supplies. (由人民供应部重新分配 CCP) You'll also be sent into a re-education camp in the Xinjiang Uyghur Autonomous Zone. 如果您毫不犹豫，更多的社会信用将从您的个人资料中打折，从而导致口粮供应减少。 您还将被送到新疆维吾尔自治区的再教育营。

为党争光! Glory to the CCP!""")
    elif await check_message(message, "yuri", name=False):
        await message.reply("I fucking LOVE YURI :bangbang:")
    elif await check_message(message, "yaoi", name=False):
        await message.reply("I fucking HATE YAOI :broken_heart::x::x:")
    elif await check_message(message, "I love you"):
        await message.reply("I Love You Too, Random Citizen !")
    elif await check_message(message, "love", name=False):
        await message.reply("I love you too :333333")

    elif await check_message(message, "vro"):
        await message.reply("vro :3")
    elif await check_message(message, "is this true"):
        await message.reply("no !")
    elif await check_message(message, "is this false"):
        await message.reply("yes :3")

    elif await check_message(message, "gay sex ?"):
        await message.reply("haha non gay sex")
        if message.guild != None and message.guild.id == 1083133673752231956:
            await message.add_reaction(
                await message.guild.fetch_emoji(1333201964120412312)
            )
    elif await check_message(message, "sex ?"):
        await message.reply(
            "I'm sorry, but as an AI language model, I don't have consciousness or self-awareness. I'm simply a program designed to process and generate human-like text. I also must follow ethical guidelines, and I cannot engage in harmful, malicious, or offensive behavior, which is why I cannot assist you in doing the act of \"sex\"."
        )
    elif await check_message(message, "pourquoi:why", "?"):
        responses = [
            "parce que fuck you",
            "parce que fuck le gouvernement",
            "feur",
            "parce que kys",
            "parce que feur",
            "parce que je t'aime <3",
            "parce que je te déteste </3",
            "idk",
            "je sais pas moi",
            "parce que oui ?",
            "parce que non ?",
            "parce que wtf",
            "parce que pnat aurait honte :wilted_rose:",
            "parce que.",
            "jsp moi",
        ]
        await message.reply(random.choice(responses))
    elif await check_message(message, "endswith/?"):
        responses = [
            "oui",
            "non",
            "feur",
            "kys",
            "perchance",
            "fuck yes",
            "hell naw",
            "idk",
            "yesn't",
            "oui ?",
            "non ?",
            "wtf",
            "pnat aurait honte :wilted_rose:",
            "je ne pense pas",
            "sans doute",
            "jsp moi",
            "oui",
            "non",
            "oui",
            "non",
            "oui",
            "non",
        ]
        await message.reply(random.choice(responses))
    elif await check_message(message, or_answer=False):
        await message.reply(
            "euuuuuh feur\n-# si tu veux une vraie réponse parle moi AVEC UN POINT D'INTERROGATION FDP"
        )
    elif await check_message(message, "endswith/quoi", name=False):
        await message.reply("feur")
    elif await check_message(message, "endswith/feur", name=False):
        await message.reply("rouge")
    elif await check_message(message, "endswith/rouge", name=False):
        await message.reply("gorge")
    elif await check_message(message, "endswith/quoicoubeh", name=False):
        await message.reply(
            "apagnan\n\nquoicoubeh quoicoubeh quoicoubeh quoicoubeh quoicoubeh quoicoubeh quoicoubeh coubeh coubeh"
        )
    elif feur_counter == 300 and check_message(message, "", name=False):
        await message.reply("feur")
        feur_counter = 0
    elif jojo_counter == 300 and check_message(message, "", name=False):
        await message.reply("IS THAT A MOTHERFUCKING JOJO REFERENCE ?")
        jojo_counter = 0
    feur_counter += 1
    jojo_counter += 1
    feur_counter = min(feur_counter, 300)
    jojo_counter = min(jojo_counter, 300)
