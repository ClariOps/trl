from trl.core.base import Module
from trl.core.context import RunContext
from .parser import DeploymentIR, ServiceIR, HelmIR, IngressIR

class DeploymentEngine(Module):
    name = "deployment-engine"

    def process(self, ctx: RunContext) -> None:
        for ir in ctx.irs:
            if isinstance(ir, DeploymentIR):
                ir.kind = "deployment"
                pass
            elif isinstance(ir, ServiceIR):
                pass
            
            elif isinstance(ir, IngressIR):
                pass

            elif isinstance(ir, HelmIR):
                pass
