from trl.core.base import OptimizationRule, ReportEvent
from trl.modules.optimizer.utils.resources import cpu_to_millicores


class CpuLimitRatioRule(OptimizationRule):

    name = "cpu-limit-ratio"
    category = "resources"

    LIMIT_RATIO = 2

    def match(self, ir):
        return hasattr(ir, "resources")

    def condition(self, ir):

        req = ir.resources.get("requests", {}).get("cpu")
        lim = ir.resources.get("limits", {}).get("cpu")

        if not req or not lim:
            return False

        req_mc = cpu_to_millicores(req)
        lim_mc = cpu_to_millicores(lim)

        return lim_mc <= req_mc

    def action(self, ir, ctx):

        req = ir.resources["requests"]["cpu"]
        req_mc = cpu_to_millicores(req)

        new_limit = req_mc * self.LIMIT_RATIO

        old = ir.resources["limits"]["cpu"]

        ir.resources["limits"]["cpu"] = f"{new_limit}m"

        ctx.report.add_optimization(
            ReportEvent(rule= self.name,
                        resource=ir.name,
                        message= f"CPU limit adjusted {old} → {new_limit}m"
                        )            
        )

        #    f"[{self.name}] {ir.name}: CPU limit adjusted {old} → {new_limit}m"
         