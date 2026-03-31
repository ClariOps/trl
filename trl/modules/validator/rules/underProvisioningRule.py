from trl.core.base import ValidationRule, RuleCategory
from trl.modules.optimizer.utils.resources import cpu_to_millicores, memory_to_mi


class UnderProvisioningRule(ValidationRule):

    name = "under-provisioning"
    category = RuleCategory.RELIABILITY.value

    MIN_CPU = 100       # 100m
    MIN_MEMORY = 128    # 128Mi

    def match(self, ir):
        return hasattr(ir, "resources")

    def condition(self, ir):

        requests = ir.resources.get("requests", {})

        cpu = requests.get("cpu")
        memory = requests.get("memory")

        if not cpu and not memory:
            return False

        cpu_mc = cpu_to_millicores(cpu) if cpu else None
        mem_mb = memory_to_mi(memory) if memory else None

        low_cpu = cpu_mc is not None and cpu_mc <= self.MIN_CPU
        low_mem = mem_mb is not None and mem_mb <= self.MIN_MEMORY

        return low_cpu or low_mem

    def validate(self, ir, ctx):

        requests = ir.resources.get("requests", {})

        cpu = requests.get("cpu")
        memory = requests.get("memory")

        issues = []

        if cpu and cpu_to_millicores(cpu) <= self.MIN_CPU:
            issues.append(f"CPU request too low ({cpu})")

        if memory and memory_to_mi(memory) <= self.MIN_MEMORY:
            issues.append(f"Memory request too low ({memory})")

        msg = ", ".join(issues)

        ctx.report.warning(
            category=self.category,
            rule=self.name,
            engine=self.engine,
            resource=ir.name,
            message=f"Under-provisioning detected → {msg}"
        )

        ctx.report.suggestion(
            category=self.category,
            rule=self.name,
            engine=self.engine,
            resource=ir.name,
            message="Increase resource requests to avoid throttling and instability"
        )