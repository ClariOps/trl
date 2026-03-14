
from trl.core.base import ValidationRule


class LatestTagRule(ValidationRule):

    name = "latest-tag"

    def match(self, ir):
        return hasattr(ir, "image")

    def validate(self, ir, ctx):

        if ir.image.endswith(":latest"):

            ctx.report.add_warning(
                f"[{self.name}] {ir.name} uses 'latest' tag"
            )
            ctx.report.add_suggestion(
                f"[{self.name}] {ir.name}: Use Tag  versioning system v1.0, v1.1 .."   
            )