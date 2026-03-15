from trl.core.base import OptimizationRule, ReportEvent

class MemoryDefaultRule(OptimizationRule):

    name = "memory-default"
    category = "generic"

    DEFAULT_MEMORY = "128Mi"

    def match(self, ir):
        return hasattr(ir, "resources")

    def condition(self, ir):

        mem = ir.resources["requests"].get("memory")

        return mem is None

    def action(self, ir, ctx):

        ir.resources["requests"]["memory"] = self.DEFAULT_MEMORY

        ctx.report.add_optimization(
            ReportEvent(rule= self.name,
                        resource=ir.name,
                        message= f"Memory default injected → {self.DEFAULT_MEMORY}"
                        )        
        )
        #    f"[{self.name}] {ir.name}: Memory default injected → {self.DEFAULT_MEMORY}"
        