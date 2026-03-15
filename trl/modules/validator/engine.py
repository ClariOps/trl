import logging
from trl.core.base import Module
from trl.core.context import RunContext

from trl.modules.validator.rules.latestTagRule import LatestTagRule
logger = logging.getLogger(__name__)


class ValidatorEngine(Module):
    name = "validator-engine"
    logger.info("Initializing Validator ... ")

    def __init__(self):
        self.rules = [LatestTagRule()]

    def process(self, ctx: RunContext) -> None:
        logger.info(f"Initializing Validator ...")
        for ir in ctx.irs:
            for rule in self.rules:
                if rule.match(ir):
                    rule.validate(ir, ctx)        
            # if m["kind"] != "Deployment":
            #     continue
            # c = m["spec"]["template"]["spec"]["containers"][0]
            # if "readinessProbe" not in c:
            #     ctx.report.warnings.append(f"{m['metadata']['name']}: readinessProbe missing")
        logger.info(f"Validator completed")