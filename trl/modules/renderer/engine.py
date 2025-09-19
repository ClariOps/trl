
from trl.core.base import Module
from trl.core.context import RunContext

class RendererEngine(Module):
    name = "renderer-engine"

    def process(self, ctx: RunContext) -> None:
        print("inside renderer....\n")
        manifests = []
        for ir in ctx.irs:
            if not ir.manifests:   
                m = ir.to_manifest()
                if m:  
                    manifests.append(m)
            else:   # bypassing optimizer
                print("in pre manifest")
                manifests = ir.manifests                  
        ctx.manifests = manifests




