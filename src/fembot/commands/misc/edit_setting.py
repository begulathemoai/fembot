import discord

from ...utils import auth, globals


@globals.tree.command(name="edit-setting")
@auth.auth(auth_level=auth.PermissionLevel.ADMIN)
async def edit_setting(
    interaction: discord.Interaction,
    pccategory: discord.CategoryChannel = None,
    disablepcs: int = 2,
    reply: int = 2,
    reply_unprompted: int = 2,
):
    out = ""
    if pccategory != None:
        globals.guilds[
            str(interaction.guild_id)
        ].new_personal_channel_category_id = pccategory.id
        out += "**OK** - Paramètre `pccategory` modifié pour ce serveur.\n"
        out += f"=> la catégorie dans laquelle les salons persos sont créés a été définie à <#{pccategory}>.\n"
    if disablepcs != 2:
        globals.guilds[str(interaction.guild_id)].personal_channels_enabled = not bool(
            disablepcs
        )
        out += "**OK** - Paramètre `disablepcs` modifié pour ce serveur.\n"
        if bool(reply):
            out += "=> les commandes de création et de modification de salon personnel ne sont plus accessibles sur ce serveur\n"
        else:
            out += "=> les commandes de création et de modification de salon personnel sont de nouveau accessibles sur ce serveur\n"
    if reply != 2:
        globals.guilds[str(interaction.guild_id)].no_ping_replies_enabled = bool(reply)
        out += "**OK** - Paramètre `reply` modifié pour ce serveur.\n"
        if bool(reply):
            out += "=> fembot répondra si on l'appelle ou le mentionne directement\n"
        else:
            out += "=> fembot ne répondra pas même si on l'appelle directement\n"
    if reply_unprompted != 2:
        globals.guilds[
            str(interaction.guild_id)
        ].unprompted_no_ping_replies_enabled = bool(reply_unprompted)
        out += "**OK** - Paramètre `reply_unprompted` modifié pour ce serveur.\n"
        if bool(reply_unprompted):
            out += '=> fembot répondra de lui-même à certains messages (comme "kirk" ou encore "yuri")\n'
        else:
            out += "=> fembot ne répondra pas que si on l'appelle directement\n"
    if out == "":
        out = "**ERREUR** - Aucun paramètre n'a été modifié"
    else:
        globals.guilds[str(interaction.guild_id)].update_storage()

    await interaction.edit_original_response(content=out)
