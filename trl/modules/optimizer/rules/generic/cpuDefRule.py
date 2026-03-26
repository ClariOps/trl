from trl.core.base import OptimizationRule

class CpuDefaultRule(OptimizationRule):

    name = "cpu-default"
    category = "generic"

    DEFAULT_CPU = "600m"

    def match(self, ir):
        return hasattr(ir, "resources")

    def condition(self, ir):

        cpu = ir.resources["requests"].get("cpu")

        return cpu is None

    def action(self, ir, ctx):

        ir.resources["requests"]["cpu"] = self.DEFAULT_CPU

        ctx.report.optimization(rule= self.name,
                        engine = self.engine,
                        resource=ir.name,
                        message= f"CPU default injected → {self.DEFAULT_CPU}"
                        )

#        f"[{self.name}] {ir.name}: CPU default injected → {self.DEFAULT_CPU}"