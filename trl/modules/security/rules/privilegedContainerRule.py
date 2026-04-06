from trl.core.base import SecurityRule, RuleSeverity


class PrivilegedContainerRule(SecurityRule):

    name = "privileged-container"
    category = "security"
    severity = RuleSeverity.HIGH.value
    
    def match(self, ir):
        return hasattr(ir, "containers")

    def condition(self, ir):

        for c in ir.containers:
            sc = c.get("securityContext")

            if sc and sc.get("privileged") is True:
                return True

        return False

    def action(self, ir, ctx):

        for c in ir.containers:
            sc = c.get("securityContext")

            if sc and sc.get("privileged") is True:

                ctx.report.error(
                    rule=self.name,
                    engine = self.engine,
                    category = self.category,
                    severity = self.severity,
                    resource=ir.name,
                    issue=f"Container runs in privileged mode",
                    impact=f"Full host access (critical risk)",
                    fix=f"Remove privileged: true"
                )