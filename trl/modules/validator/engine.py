import logging
from trl.core.base import Module
from trl.core.context import RunContext

from trl.modules.validator.rules.replicaScalingRule import ReplicaScalingSuggestionRule
from trl.modules.validator.rules.overProvisioningRule import OverProvisioningRule
from trl.modules.validator.rules.underProvisioningRule import UnderProvisioningRule


logger = logging.getLogger(__name__)


class ValidatorEngine(Module):
    name = "validator-engine"
    logger.info("Initializing Validator ... ")

    def __init__(self):
        self.rules = [
            ReplicaScalingSuggestionRule(), 
            OverProvisioningRule(),
            UnderProvisioningRule()
        ]

    def process(self, ctx: RunContext) -> None:
        logger.info(f"Initializing Validator ...")
        for ir in ctx.irs:
            for rule in self.rules:
                rule.execute(ir, ctx)

        logger.info(f"Validator completed\n")