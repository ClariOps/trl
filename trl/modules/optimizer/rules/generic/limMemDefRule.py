from trl.core.base import OptimizationRule


class MemoryLimitRule(OptimizationRule):

    name = "memory-limit-default"
    category = "generic"

    DEFAULT_MEMORY_LIMIT = "512Mi"

    def match(self, ir):
        return hasattr(ir, "resources")

    def condition(self, ir):

        limits = ir.resources.get("limits", {})

        memory = limits.get("memory")

        return memory is None

    def action(self, ir, ctx):

        ir.resources.setdefault("limits", {})

        ir.resources["limits"]["memory"] = self.DEFAULT_MEMORY_LIMIT

        ctx.report.optimizations.append(
            f"[{self.name}] Memory limit injected → {self.DEFAULT_MEMORY_LIMIT}"
        )