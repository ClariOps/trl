from trl.core.base import OptimizationRule, ReportEvent


class CpuLimitRule(OptimizationRule):

    name = "cpu-limit-default"
    category = "generic"


    def match(self, ir):
        return hasattr(ir, "resources")

    def condition(self, ir):

        limits = ir.resources.get("limits", {})

        cpu = limits.get("cpu")

        return cpu is None

    def action(self, ir, ctx):

        ir.resources.setdefault("limits", {})

        ir.resources["limits"]["cpu"] = ir.resources["requests"]["cpu"]

        ctx.report.optimization(
            rule= self.name,
            engine = self.engine,
            resource=ir.name,
            message=f"CPU limit not defined → defaulting to {ir.resources["requests"]["cpu"]} to prevent resource overuse"  
        )
            #f"[{self.name}] {ir.name}: CPU limit injected → {self.DEFAULT_CPU_LIMIT}"
        