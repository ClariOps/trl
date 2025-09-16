
from trl.core.base import Module
from trl.core.context import RunContext

from pykube import Deployment, HTTPClient, KubeConfig
import yaml

class RendererEngine(Module):
    name = "renderer-engine"

    def process(self, ctx: RunContext) -> None:
        print("inside renderer....\n")
        manifests = []
        local = False
        for ir in ctx.irs:
            if not ir.manifests:   
                m = ir.to_manifest()
                if m:  
                    manifests.append(m)
            else:   # bypassing optimizer
                print("in pre manifest")
                manifests = ir.manifests
                local     = ir.local                    
        ctx.manifests = manifests

        if local:
            print("i am in local") 
            config = KubeConfig.from_file()
            api = HTTPClient(config)

            deployment = Deployment(api,ctx.manifests)
            deployment.create()
            print(f"Deployed {deployment.name} successfully!")


