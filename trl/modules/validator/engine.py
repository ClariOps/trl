import logging
from trl.core.base import Module
from trl.core.context import RunContext

logger = logging.getLogger(__name__)

class ValidatorEngine(Module):
    name = "validator-engine"
    logger.info(f"Enter Validator: ")
    def process(self, ctx: RunContext) -> None:
        logger.info(f"Enter Validator: Ok")
        for m in ctx.manifests:            
            if m["kind"] != "Deployment":
                continue
            c = m["spec"]["template"]["spec"]["containers"][0]
            if "readinessProbe" not in c:
                ctx.report.warnings.append(f"{m['metadata']['name']}: readinessProbe missing")
