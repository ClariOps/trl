
from trl.core.base import Module
from trl.core.context import RunContext

class RendererEngine(Module):
    name = "renderer-engine"

    def process(self, ctx: RunContext) -> None:
        print("inside renderer....\n")
        ctx.manifests = [ir.to_manifest() for ir in ctx.irs]
        



