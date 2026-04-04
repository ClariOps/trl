from trl.core.base import ValidationRule, RuleCategory, RuleSeverity

class NodePortExposureRule(ValidationRule):
    name = "nodeport-exposure"
    category = RuleCategory.NETWORK
    severity = RuleSeverity.MEDIUM

    def match(self, ir):
        return getattr(ir, "kind", None) == "ServiceIR"

    def condition(self, ir):
        return getattr(ir, "service_type", "").lower() == "nodeport"

    def validate(self, ir, ctx):
        ctx.report.warning(
            engine=self.engine,
            category=self.category,
            severity=self.severity,
            rule=self.name,
            resource=ir.name,
            message="Service exposed via NodePort → opens access on every node IP → increases attack surface"
        )

        ctx.report.suggestion(
            engine=self.engine,
            category=self.category,
            severity=self.severity,
            rule=self.name,
            resource=ir.name,
            message="Use ClusterIP for internal services or Ingress for controlled external access"
        )