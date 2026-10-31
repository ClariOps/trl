from trload.core.base import ValidationRule, RuleCategory, RuleSeverity

class NodePortExposureRule(ValidationRule):
    name = "nodeport-exposure"
    category = RuleCategory.NETWORK.value
    severity = RuleSeverity.MEDIUM.value

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
            issue="Service exposed via NodePort → opens access on every node IP",
            impact="Increases attack surface → may lead to unauthorized access",
            fix="Use ClusterIP for internal services or Ingress for controlled external access"
        )

 