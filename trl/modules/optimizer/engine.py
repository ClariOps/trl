from trl.core.base import Module
from trl.core.context import RunContext

class OptimizerEngine(Module):
    name = "optimizer-engine"

    def process(self, ctx: RunContext) -> None:
        for m in ctx.manifests:
            if m["kind"] != "Deployment":
                continue
            c = m["spec"]["template"]["spec"]["containers"][0]
            req = c["resources"]["requests"]

            if req["cpu"].endswith("mi") and int(req["cpu"][:-2]) < 50:
                req["cpu"] = "50mi"
                c["resources"]["limits"]["cpu"] = "50mi"

            if req["memory"].endswith("Mi") and int(req["memory"][:-2]) < 64:
                req["memory"] = "64Mi"
                c["resources"]["limits"]["memory"] = "64Mi"
