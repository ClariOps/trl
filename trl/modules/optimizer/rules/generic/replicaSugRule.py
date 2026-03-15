from trl.core.base import OptimizationRule, ReportEvent
from trl.modules.optimizer.utils.resources import cpu_to_millicores


class ReplicaSuggestionRule(OptimizationRule):

    name = "replica-suggestion"
    category = "scaling"

    CPU_THRESHOLD = 500  # millicores

    def match(self, ir):
        return hasattr(ir, "resources")

    def condition(self, ir):

        cpu = ir.resources["requests"].get("cpu")

        if not cpu:
            return False

        mc = cpu_to_millicores(cpu)

        return mc > self.CPU_THRESHOLD and ir.replicas == 1

    def action(self, ir, ctx):

        ctx.report.add_optimization(
            ReportEvent(rule= self.name,
                        resource=ir.name,
                        message= f"Replica scaling suggested (1 → 2)"
                        )           
        )
        #    f"[{self.name}] {ir.name}: Replica scaling suggested (1 → 2)"
        