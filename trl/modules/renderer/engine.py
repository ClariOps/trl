
from trl.core.base import Module
from trl.core.context import RunContext
import logging
logger = logging.getLogger(__name__)

class RendererEngine(Module):
    name = "renderer-engine"

    def process(self, ctx: RunContext) -> None:
        logger.info("Enter Renderer Engine:")
        ctx.manifests = [ir.to_manifest() for ir in ctx.irs]
        



