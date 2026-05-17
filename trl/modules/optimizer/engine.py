from trl.core.base import Module
from trl.core.context import RunContext
from trl.core.ir import DeploymentIR, ServiceIR, PVCIR, SecretIR, ConfigMapIR, IngressIR
from trl.modules.optimizer.rules.generic.cpuDefRule import CpuDefaultRule
from trl.modules.optimizer.rules.generic.memDefRule import MemoryDefaultRule
from trl.modules.optimizer.rules.generic.limCpuDefRule import CpuLimitRule
from trl.modules.optimizer.rules.generic.limMemDefRule import MemoryLimitRule
from trl.modules.optimizer.rules.generic.replicaDefRule import ReplicaDefRule




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
            