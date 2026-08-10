from ..utils import globals, logger


@globals.client.event
async def on_ready():
    await globals.tree.sync()
    logger.log("fembot is ready")
    globals.ready = True
