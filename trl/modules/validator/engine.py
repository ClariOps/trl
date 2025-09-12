from trl.core.base import Module
from trl.core.context import RunContext

class ValidatorEngine(Module):
    name = "validator-engine"

    def process(self, ctx: RunContext) -> None:
        print("inside validator")
        for m in ctx.manifests:            
            if m["kind"] != "Deployment":
                continue
            c = m["spec"]["template"]["spec"]["containers"][0]
            if "readinessProbe" not in c:
                ctx.report.warnings.append(f"{m['metadata']['name']}: readinessProbe missing")
