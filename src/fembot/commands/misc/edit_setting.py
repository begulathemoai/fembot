import discord

from ...utils import auth, globals


@globals.tree.command(
    name="edit-setting", description="Modifie les paramètres de fembot pour ce serveur."
)
@discord.app_commands.describe(
    pc_category="La catégorie dans laquelle les salons persos doivent être créés. [choose]",
    personal_channels_enabled="Si le système de salons persos devrait être activé. [0=N,1=Y,2=noop]",
    no_ping_replies_enabled="Si fembot devrait répondre quand on l'appelle. [0=N,1=Y,2=noop]",
    unprompted_replies_enabled="Si fembot peut répondre même sans qu'on l'appelle. [0=N,1=Y,2=noop]",
    le_kirk="charlie krik",
)
@auth.auth(auth_level=auth.PermissionLevel.ADMIN)
async def edit_setting(
    interaction: discord.Interaction,
    pc_category: discord.CategoryChannel = None,
    personal_channels_enabled: int = 2,
    no_ping_replies_enabled: int = 2,
    unprompted_replies_enabled: int = 2,
    le_kirk: int = 2,
):
    out = ""
    if pc_category != None:
        globals.guilds[
            interaction.guild_id
        ].new_personal_channel_category_id = pc_category.id
        out += "**OK** - Paramètre `pccategory` modifié pour ce serveur.\n"
        out += f"=> la catégorie dans laquelle les salons persos sont créés a été définie à <#{pc_category.id}>.\n"
    if personal_channels_enabled != 2:
        globals.guilds[interaction.guild_id].personal_channels_enabled = bool(
            personal_channels_enabled
        )
        out += (
            "**OK** - Paramètre `personal_channels_enabled` modifié pour ce serveur.\n"
        )
        if bool(personal_channels_enabled):
            out += "=> les commandes de création et de modification de salon personnel sont accessibles sur ce serveur\n"
        else:
            out += "=> les commandes de création et de modification de salon personnel ne sont plus accessibles sur ce serveur\n"
    if no_ping_replies_enabled != 2:
        globals.guilds[interaction.guild_id].no_ping_replies_enabled = bool(
            no_ping_replies_enabled
        )
        out += "**OK** - Paramètre `no_ping_replies_enabled` modifié pour ce serveur.\n"
        if bool(no_ping_replies_enabled):
            out += "=> fembot répondra si on l'appelle ou le mentionne directement\n"
        else:
            out += "=> fembot ne répondra pas même si on l'appelle directement\n"
    if unprompted_replies_enabled != 2:
        globals.guilds[interaction.guild_id].unprompted_no_ping_replies_enabled = bool(
            unprompted_replies_enabled
        )
        out += (
            "**OK** - Paramètre `unprompted_replies_enabled` modifié pour ce serveur.\n"
        )
        if bool(unprompted_replies_enabled):
            out += '=> fembot répondra de lui-même à certains messages (comme "kirk" ou "yuri")\n'
        else:
            out += "=> fembot ne répondra pas que si on l'appelle directement\n"
    if le_kirk != 2:
        globals.guilds[interaction.guild_id].enable_the_kirk = bool(le_kirk)
        out += "**OK** - Paramètre `le_kirk` modifié pour ce serveur.\n"
        if bool(le_kirk):
            out += '=> fembot répondra avec des copypastas à tout message contenant "kirk" et acceptera les commandes kirk.\n'
        else:
            out += '=> fembot ne répondra pas aux messages contenant "kirk" et n\'acceptera pas les commandes kirk.\n'
    if out == "":
        out = "**ERREUR** - Aucun paramètre n'a été modifié"
    else:
        globals.guilds[interaction.guild_id].update_storage()

    await interaction.edit_original_response(content=out)
