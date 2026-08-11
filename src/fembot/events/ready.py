from ..utils import globals, guild_storage, logger, storage


@globals.client.event
async def on_ready():
    await globals.tree.sync()
    storage.init()
    for i in globals.client.guilds:
        globals.guilds.update({i.id: guild_storage.GuildStorage(i)})
    logger.log("fembot is ready")
    globals.ready = True
