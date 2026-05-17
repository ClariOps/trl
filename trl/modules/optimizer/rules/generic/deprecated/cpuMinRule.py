from trl.core.base import OptimizationRule
from trl.modules.optimizer.utils.resources import cpu_to_millicores
from trl.core.base import ReportEvent
class CpuMinimumRule(OptimizationRule):

    name = "cpu-minimum"
    category = "generic"
    MIN_CPU = 100

    def match(self, ir):
        return hasattr(ir, "resources")

    def condition(self, ir):

        cpu = ir.resources["requests"].get("cpu")
        value = cpu_to_millicores(cpu)

        if value is None:
            return False

        return value < self.MIN_CPU

    def action(self, ir, ctx):

        old = ir.resources["requests"]["cpu"]

        ir.resources["requests"]["cpu"] = f"{self.MIN_CPU}m"

        ctx.report.optimization(
                rule= self.name,
                engine = self.engine,
                resource=ir.name,
                message= f"CPU request ({old}) below recommended minimum → increased to {self.MIN_CPU}m to avoid throttling",
        )
          #  f"[{self.name}] {ir.name}: CPU increased {old} → {self.MIN_CPU}m"
        

        