from trload.core.base import Module
from trload.core.context import RunContext
from trload.core.ir import DeploymentIR, ServiceIR, PVCIR, SecretIR, ConfigMapIR, IngressIR
from trload.modules.optimizer.rules.generic.cpuDefRule import CpuDefaultRule
from trload.modules.optimizer.rules.generic.memDefRule import MemoryDefaultRule
from trload.modules.optimizer.rules.generic.limCpuDefRule import CpuLimitRule
from trload.modules.optimizer.rules.generic.limMemDefRule import MemoryLimitRule
from trload.modules.optimizer.rules.generic.replicaDefRule import ReplicaDefRule




import logging
logger = logging.getLogger(__name__)

class OptimizerEngine(Module):
    name = "optimizer-engine"
    def __init__(self):
        self.rules = [
            CpuDefaultRule(),
            MemoryDefaultRule(),
            CpuLimitRule(),
            MemoryLimitRule(),
            ReplicaDefRule(),

        ]

    def process(self, ctx: RunContext) -> None:
        logger.info("Initializing optimizer ........")
        logger.info(f"{len(ctx.irs)} resources loaded")

        for rule in self.rules:
            if not rule.enabled(ctx):        
                continue    
            for ir in ctx.irs:
                rule.execute(ir, ctx)
           
                        
        logger.info("Optimizer completed\n") 
            