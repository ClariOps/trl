from trl.core.base import Module
from trl.core.context import RunContext
from .parser import DeploymentIR, ServiceIR, HelmIR

class DeploymentEngine(Module):
    name = "deployment-engine"

    def process(self, ctx: RunContext) -> None:
        print("inside context")
        for ir in ctx.irs:
            if isinstance(ir, DeploymentIR):
                print("ir name is ", ir.name)