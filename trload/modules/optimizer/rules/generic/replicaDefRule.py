from trload.core.base import OptimizationRule, ReportEvent
from trload.modules.optimizer.utils.resources import cpu_to_millicores

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

        ctx.report.optimization(
            rule= self.name,
            engine = self.engine,
            resource=ir.name,
            message=f"Replica count not defined → defaulting to [{self.DEFAULT_REPLICAS}] to improve availability"                                  
        )
       #     f"[{self.name}] {ir.name}: Replica count injected {old}  → {self.DEFAULT_REPLICAS}"
       
        