from trload.core.base import ValidationRule, RuleCategory, RuleSeverity


class ReadinessProbeMissingRule(ValidationRule):

    name = "no-readiness-probe"
    category = RuleCategory.RELIABILITY.value
    severity = RuleSeverity.MEDIUM.value

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
            issue="Readiness probe not defined",
            impact="Traffic may be routed to unready pods → potential request failures",
            fix="Define readinessProbe to ensure traffic is only sent to healthy pods"
        )

