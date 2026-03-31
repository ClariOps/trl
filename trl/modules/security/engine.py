import logging
from trl.core.base import Module
from trl.core.context import RunContext
from trl.modules.security.rules.latestTagRule import LatestTagRule
from trl.modules.security.rules.privilegedContainerRule import PrivilegedContainerRule
from trl.modules.security.rules.runAsRootContainer import RunAsRootRule

logger = logging.getLogger(__name__)

class SecurityEngine(Module):
    name = "security-engine"
    def __init__(self):
        self.rules = [
            LatestTagRule(),
            PrivilegedContainerRule(),
            RunAsRootRule()
        ]
    def process(self, ctx: RunContext) -> None:
        logger.info(f"Initializing Security check ...")
        for ir in ctx.irs:
            for rule in self.rules:
                rule.execute(ir, ctx)
                
        logger.info(f"Security check completed\n")