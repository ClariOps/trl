
from trl.core.base import ValidationRule, ReportEvent


class LatestTagRule(ValidationRule):

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

    def validate(self, ir, ctx):

       

        ctx.report.warning(
            rule= self.name,
            resource=ir.name,
            message= f"Uses Image tag as 'latest' "
        )
        ctx.report.suggestion(
            rule= self.name,
            resource=ir.name,
            message= f"Change tag  ('latest' → v1)"
        )                    
            