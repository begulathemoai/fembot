from ..utils import globals, guild_storage, logger, storage


@globals.client.event
async def on_ready():
    logger.log("fembot is starting")
    logger.log("syncing commands with discord...")
    await globals.tree.sync()
    logger.log("initializing storage...")
    storage.init()
    logger.log("creating guild-specific storage...")
    for i in globals.client.guilds:
        globals.guilds.update({i.id: guild_storage.GuildStorage(i)})
        logger.log(f"{i.name} handled (id: {i.id})")
    logger.log("fembot is ready")
    globals.ready = True
