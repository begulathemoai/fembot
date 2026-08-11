import discord

from ...utils import auth, globals


class NoBitchesError(Exception):
    pass


@globals.tree.command(name="trigger-error")
@auth.auth(auth.PermissionLevel.ADMIN)
async def trigger_error(interaction: discord.Interaction) -> None:
    await interaction.edit_original_response(content="okay :3")
    raise NoBitchesError("erreur déclenchée par l'utilisateur")
