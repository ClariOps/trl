from trl.core.base import Module
from trl.core.context import RunContext

class CloudEngine(Module):
    name = "cloud-engine"

    def process(self, ctx: RunContext) -> None:
        cloud = ctx.opts.get("cloud")
        if not cloud:
            return

        for m in ctx.manifests:
            if m["kind"] != "Deployment":
                continue
            if cloud == "aks":
                m["spec"]["template"]["spec"].setdefault("nodeSelector", {})["kubernetes.io/arch"] = "arm64"
