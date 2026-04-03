from trl.core.base import ValidationRule, RuleCategory, RuleSeverity

class NodePortExposureRule(ValidationRule):
    name = "nodeport-exposure"
    category = RuleCategory.NETWORK
    severity = RuleSeverity.MEDIUM

    def match(self, ir):
        return getattr(ir, "kind", None) == "Service"

    def condition(self, ir):
        return getattr(ir, "service_type", "").lower() == "nodeport"

    def validate(self, ir, ctx):
        ctx.report.warning(
            engine=self.engine,
            category=self.category,
            severity=self.severity,
            rule=self.name,
            resource=ir.name,
            message="Service exposed via NodePort → external access risk"
        )

        ctx.report.suggestion(
            engine=self.engine,
            category=self.category,
            severity=self.severity,
            rule=self.name,
            resource=ir.name,
            message="Use ClusterIP or Ingress for controlled exposure"
        )