from trl.core.base import Module
from trl.core.context import RunContext

class SecurityEngine(Module):
    name = "security-engine"

    def process(self, ctx: RunContext) -> None:
        for m in ctx.manifests:
            if m["kind"] != "Deployment":
                continue
            pod_sc = m["spec"]["template"]["spec"].setdefault("securityContext", {})
            pod_sc.setdefault("runAsNonRoot", True)
            c = m["spec"]["template"]["spec"]["containers"][0]
            c.setdefault("securityContext", {}).setdefault("readOnlyRootFilesystem", True)
