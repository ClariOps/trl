import logging
from trload.core.base import Module
from trload.core.context import RunContext
from trload.modules.security.rules.latestTagRule import LatestTagRule
from trload.modules.security.rules.privilegedContainerRule import PrivilegedContainerRule
from trload.modules.security.rules.runAsRootContainer import RunAsRootRule

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
        for rule in self.rules:
            if not rule.enabled(ctx):        
                continue    
            for ir in ctx.irs:
                rule.execute(ir, ctx)       
        logger.info(f"Security check completed\n")