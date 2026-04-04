from trl.core.base import ValidationRule, RuleCategory, RuleSeverity


class NoLivenessProbeRule(ValidationRule):
    name = "no-liveness-probe"
    category = RuleCategory.RELIABILITY
    severity = RuleSeverity.MEDIUM

    def match(self, ir):
        return hasattr(ir, "containers")

    def condition(self, ir):
        for c in ir.containers or []:
            if not c.get("livenessProbe"):
                return True
        return False

    def validate(self, ir, ctx):
        ctx.report.warning(
            engine=self.engine,
            category=self.category,
            severity=self.severity,
            rule=self.name,
            resource=ir.name,
            message="Liveness probe not defined → container failures may not be detected → pods may remain unhealthy"
        )

        ctx.report.suggestion(
            engine=self.engine,
            category=self.category,
            severity=self.severity,
            rule=self.name,
            resource=ir.name,
            message="Define livenessProbe to enable automatic detection and recovery of failed containers"
        )