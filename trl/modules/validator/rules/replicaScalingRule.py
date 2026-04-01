from trl.core.base import ValidationRule, ReportEvent, RuleCategory
from trl.modules.optimizer.utils.resources import cpu_to_millicores


class ReplicaScalingSuggestionRule(ValidationRule):

    name = "replica-scaling"
    CPU_THRESHOLD = 500  # millicores
    category = RuleCategory.SCALING

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
            rule=self.name,
            resource=ir.name,
            message=f"High CPU ({ir.resources['requests'].get('cpu')}) with single replica"
        )

        ctx.report.suggestion(
            engine=self.engine,
            category=self.category,
            rule=self.name,
            resource=ir.name,
            message="Increase replicas to 2+ for better load distribution"
        )