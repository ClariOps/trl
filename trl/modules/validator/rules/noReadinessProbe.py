from trl.core.base import ValidationRule, RuleCategory, RuleSeverity


class ReadinessProbeMissingRule(ValidationRule):

    name = "no-readiness-probe"
    category = RuleCategory.RELIABILITY
    severity = RuleSeverity.MEDIUM

    def match(self, ir):
        return hasattr(ir, "containers")
   
    def condition(self, ir):
        for c in ir.containers or []:
            if not c.get("readinessProbe"):
                return True
        return False

    def validate(self, ir, ctx):
        ctx.report.warning(
            engine=self.engine,
            category=self.category,
            severity=self.severity,
            rule=self.name,
            resource=ir.name,
            message="Missing readiness probe → traffic may hit unready pods"
        )

        ctx.report.suggestion(
            engine=self.engine,
            category=self.category,
            severity=self.severity,
            rule=self.name,
            resource=ir.name,
            message="Define readinessProbe to control traffic flow"
        )