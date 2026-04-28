from trl.core.base import OptimizationRule, ReportEvent


class MemoryLimitRule(OptimizationRule):

    name = "memory-limit-default"
    category = "generic"


    def match(self, ir):
        return hasattr(ir, "resources")

    def condition(self, ir):

        limits = ir.resources.get("limits", {})

        memory = limits.get("memory")

        return memory is None

    def action(self, ir, ctx):

        ir.resources.setdefault("limits", {})

        ir.resources["limits"]["memory"] = ir.resources["requests"]["memory"]

        ctx.report.optimization(
            rule= self.name,
            engine= self.engine,
            resource=ir.name,
            message=f"Memory limit not defined → defaulting to {ir.resources["requests"]["memory"]} to prevent excessive memory usage"
                                    
        )    
        #    f"[{self.name}] {ir.name}: Memory limit injected → {self.DEFAULT_MEMORY_LIMIT}"
        