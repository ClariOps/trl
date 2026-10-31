from trload.core.base import ValidationRule, ReportEvent, RuleCategory, RuleSeverity
from trload.modules.optimizer.utils.resources import cpu_to_millicores


class ReplicaScalingSuggestionRule(ValidationRule):

    name = "replica-scaling"
    CPU_THRESHOLD = 499  # millicores
    category = RuleCategory.SCALING.value
    severity = RuleSeverity.MEDIUM.value
    def match(self, ir):
        return hasattr(ir, "resources")

    def condition(self, ir):

        cpu = ir.resources["requests"].get("cpu")

        if not cpu:
            return False

        mc = cpu_to_millicores(cpu)

        return mc > self.CPU_THRESHOLD and (ir.replicas is None or ir.replicas == 1)

    def validate(self, ir, ctx):

        ctx.report.warning(
            engine=self.engine,
            category=RuleCategory.SCALING.value,
            severity=self.severity,
            rule=self.name,
            resource=ir.name,
            issue=f"High CPU request ({ir.resources['requests'].get('cpu')}) with single replica",
            impact="Creates single point of failure under load",
            fix="Increase replicas [2+] to improve availability and distribute traffic"    
        )

