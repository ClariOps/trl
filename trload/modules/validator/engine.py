import logging
from trload.core.base import Module
from trload.core.context import RunContext

from trload.modules.validator.rules.replicaScalingRule import ReplicaScalingSuggestionRule
from trload.modules.validator.rules.overProvisioningRule import OverProvisioningRule
from trload.modules.validator.rules.underProvisioningRule import UnderProvisioningRule
from trload.modules.validator.rules.noReadinessProbe import ReadinessProbeMissingRule
from trload.modules.validator.rules.noLivenessProbe import NoLivenessProbeRule
from trload.modules.validator.rules.nodePortWarning import NodePortExposureRule


logger = logging.getLogger(__name__)


class ValidatorEngine(Module):
    name = "validator-engine"
    #logger.info("Initializing Validator ... ")

    def __init__(self):
        self.rules = [
            ReplicaScalingSuggestionRule(), 
            OverProvisioningRule(),
            UnderProvisioningRule(),
            ReadinessProbeMissingRule(),
            NoLivenessProbeRule(),
            NodePortExposureRule()
        ]

    def process(self, ctx: RunContext) -> None:
        logger.info(f"Initializing Validator ...")
        
        for rule in self.rules:
            if not rule.enabled(ctx):
                continue
            
            for ir in ctx.irs:    
                rule.execute(ir, ctx)

        logger.info(f"Validator completed\n")