from trl.core.base import Module
from trl.core.context import RunContext
from .parser import DeploymentIR, ServiceIR, HelmIR

class DeploymentEngine(Module):
    name = "deployment-engine"

    def process(self, ctx: RunContext) -> None:
        for ir in ctx.irs:
            if isinstance(ir, DeploymentIR):
                ir.kind = "deployment"
                pass
            elif isinstance(ir, ServiceIR):
                ctx.manifests.append({
                    "apiVersion": "v1",
                    "kind": "Service",
                    "metadata": {"name": ir.name},
                    "spec": {
                        "type": ir.type,
                        "selector": ir.selector,
                        "ports": [{"port": ir.port, "targetPort": ir.port}],
                    }
                })
            elif isinstance(ir, HelmIR):
                pass
