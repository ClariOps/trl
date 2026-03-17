from trl.core.base import Module
from trl.core.context import RunContext
from trl.core.ir import DeploymentIR, ServiceIR, PVCIR, SecretIR, ConfigMapIR, IngressIR
from trl.modules.optimizer.rules.generic.cpuMinRule import CpuMinimumRule
from trl.modules.optimizer.rules.generic.cpuDefRule import CpuDefaultRule
from trl.modules.optimizer.rules.generic.memMinRule import MemoryMinimumRule
from trl.modules.optimizer.rules.generic.memDefRule import MemoryDefaultRule
from trl.modules.optimizer.rules.generic.limCpuDefRule import CpuLimitRule
from trl.modules.optimizer.rules.generic.limMemDefRule import MemoryLimitRule
from trl.modules.optimizer.rules.generic.replicaDefRule import ReplicaDefRule
from trl.modules.optimizer.rules.generic.replicaSugRule import ReplicaSuggestionRule
from trl.modules.optimizer.rules.generic.cpuRatioRule import CpuLimitRatioRule



import logging
logger = logging.getLogger(__name__)

class OptimizerEngine(Module):
    name = "optimizer-engine"
    def __init__(self):
        self.rules = [
            CpuMinimumRule(),
            CpuDefaultRule(),
            MemoryMinimumRule(),
            MemoryDefaultRule(),
            CpuLimitRule(),
            MemoryLimitRule(),
            ReplicaDefRule(),
            ReplicaSuggestionRule(),
            CpuLimitRatioRule()
        ]

    def process(self, ctx: RunContext) -> None:
        logger.info("Initializing optimizer ........")
        logger.info(f"{len(ctx.irs)} resources loaded")

        for ir in ctx.irs:
            for rule in self.rules:
                rule.execute(ir, ctx)
               
                logger.debug(f"Rules matched : {rule.name}")

            logger.debug(f"Optimize IR Data: {ir.__dict__}")
                        
        logger.info("Optimizer completed") 
            