from trl.core.base import OptimizationRule
from trl.modules.optimizer.utils.resources import cpu_to_millicores

class ReplicaDefRule(OptimizationRule):

    name = "replica-default"
    category = "generic"

    DEFAULT_REPLICAS = 2

    def match(self, ir):
        return hasattr(ir, "resources")

    def condition(self, ir):

        return ir.replicas is None

    def action(self, ir, ctx):

        old = ir.replicas

        ir.replicas = self.DEFAULT_REPLICAS

        ctx.report.optimizations.append(
            f"[{self.name}] Replica count injected {old}  → {self.DEFAULT_REPLICAS}"
        )