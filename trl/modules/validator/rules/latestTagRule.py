
from trl.core.base import ValidationRule


class LatestTagRule(ValidationRule):

    name = "latest-tag"

    def match(self, ir):
        return hasattr(ir, "image")

    def validate(self, ir, ctx):

        if ir.image.endswith(":latest"):

            ctx.report.warnings.append(
                f"[{self.name}] {ir.name} uses 'latest' tag"
            )