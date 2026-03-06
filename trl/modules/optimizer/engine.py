from trl.core.base import Module
from trl.core.context import RunContext
from trl.core.ir import DeploymentIR, ServiceIR, PVCIR, SecretIR, ConfigMapIR, IngressIR
from trl.modules.optimizer.rules.generic.cpuMinRule import CpuMinimumRule
from trl.modules.optimizer.rules.generic.cpuDefRule import CpuDefaultRule
from trl.modules.optimizer.rules.generic.memMinRule import MemoryMinimumRule
from trl.modules.optimizer.rules.generic.memDefRule import MemoryDefaultRule


import logging
logger = logging.getLogger(__name__)

class OptimizerEngine(Module):
    name = "optimizer-engine"
    def __init__(self):
        self.rules = [
            CpuMinimumRule(),
            CpuDefaultRule(),
            MemoryMinimumRule(),
            MemoryDefaultRule()
        ]

    def process(self, ctx: RunContext) -> None:
        logger.info("Processing optimizition........\n")

        
        for ir in ctx.irs:
            for rule in self.rules:
                if not rule.match(ir):
                    continue
                if not rule.condition(ir):
                    continue
                rule.action(ir, ctx)
                logger.debug(f"Optimizer Current Rules are: {rule}")
                
            
#           req = ir.resources["requests"]

            # if not req.get("cpu"):
            #     req["cpu"] = "100m"
            #     ir.resources["limits"]["cpu"] = "100m"

            #     ctx.report.optimizations.append(f"[default-resource] {ir.name}: cpu defaulted to 100m")
            # if not req.get("memory"):
            #     req["memory"] = "64Mi"
            #     ir.resources["limits"]["memory"] = "64Mi"

            #     ctx.report.optimizations.append(f"[default-resource] {ir.name}: memory defaulted to 100m")
                        
 
            logger.debug(f"Optimize IR Data: {ir.__dict__}")