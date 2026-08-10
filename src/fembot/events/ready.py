from ..utils import globals, logger, storage


@globals.client.event
async def on_ready():
    await globals.tree.sync()
    storage.init()
    logger.log("fembot is ready")
    globals.ready = True
