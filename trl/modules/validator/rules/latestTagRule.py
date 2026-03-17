
from trl.core.base import ValidationRule, ReportEvent


class LatestTagRule(ValidationRule):

    name = "latest-tag"

    def match(self, ir):
        return hasattr(ir, "image")

    def validate(self, ir, ctx):

        if ir.image.endswith(":latest"):

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
            