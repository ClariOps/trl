from trl.core.base import OptimizationRule, ReportEvent
from trl.modules.optimizer.utils.resources import memory_to_mi

class MemoryMinimumRule(OptimizationRule):

    name = "memory-minimum"
    category = "generic"

    MIN_MEMORY = 128

    def match(self, ir):
        return hasattr(ir, "resources")

    def condition(self, ir):

        mem = ir.resources["requests"].get("memory")
        value = memory_to_mi(mem)

        if value is None:
            return False

        return value < self.MIN_MEMORY

    def action(self, ir, ctx):

        old = ir.resources["requests"]["memory"]

        ir.resources["requests"]["memory"] = f"{self.MIN_MEMORY}Mi"

        ctx.report.optimization(
            rule= self.name,
            resource=ir.name,
            message= f"Memory increased {old} → {self.MIN_MEMORY}Mi"
                                   
        )
        
        #    f"[{self.name}] {ir.name}: Memory increased {old} → {self.MIN_MEMORY}Mi"
        #)
