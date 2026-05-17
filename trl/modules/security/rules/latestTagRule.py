
from trl.core.base import SecurityRule, ReportEvent


class LatestTagRule(SecurityRule):

    name = "latest-tag"
    def match(self, ir):
        return hasattr(ir, "image")
    
    def condition(self, ir):
        if not ir.image:
            return False

        # Case 1: explicit latest
        if ir.image.endswith(":latest"):
            return True

        # Case 2: no tag → implicit latest
        if ":" not in ir.image.split("/")[-1]:
            return True

        return False

    def action(self, ir, ctx):      
        ctx.report.warning(
            rule= self.name,
            engine = self.engine,
            resource=ir.name,
            issue=f"Image uses mutable tag 'latest'",
            impact=f"May lead to unpredictable deployments → increases risk of unverified changes",
            fix=f"Use a fixed version tag (e.g., v1.2.3) to ensure consistent and reproducible deployments",
        )
                 
            