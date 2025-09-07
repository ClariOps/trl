
from trl.core.base import Module
from trl.core.context import RunContext

class RendererEngine(Module):
    name = "renderer-engine"

    def process(self, ctx: RunContext) -> None:
        print("inside renderer....\n")
        manifests = []
        for ir in ctx.irs:
            m = ir.to_manifest()
            if m:  # HelmIR returns {}
                manifests.append(m)
        
        ctx.manifests = manifests