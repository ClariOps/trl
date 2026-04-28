from trl.core.base import SecurityRule, RuleSeverity


class RunAsRootRule(SecurityRule):

    name = "run-as-root"
    category = "security"
    
    severity= RuleSeverity

    def match(self, ir):
        return hasattr(ir, "containers") and len(ir.containers) > 0

    def condition(self, ir):
        # Trigger if ANY container matches
        for c in ir.containers:
            sc = c.get("securityContext", {})

            # Case 1: explicit root
            if sc.get("runAsUser") == 0:
                return True

            # Case 2: missing user
            if "runAsUser" not in sc:
                return True

        return False

    def action(self, ir, ctx):
        resource = ir.name
        for c in ir.containers:
            sc = c.get("securityContext", {})

            name = c.get("name", "unknown")

            if sc.get("runAsUser") == 0: 
                ctx.report.error(
                    rule=self.name,
                    engine=self.engine,
                    category=self.category,
                    resource=resource,
                    severity=self.severity.HIGH.value,
                    issue=f"Container '{resource}/{name}' runs as root (UID 0)",
                    impact="Increases risk of container escape and privilege escalation",
                    fix="Set securityContext.runAsUser to a non-root UID (e.g., 1000)"
                )
            elif "runAsUser" not in sc:
                ctx.report.error(
                    rule=self.name,
                    engine=self.engine,
                    category=self.category,
                    resource=resource,
                    severity=self.severity.MEDIUM.value,
                    issue=f"Container '{resource}/{name}' does not define runAsUser",
                    impact="Defaults to root user, increasing security risk",
                    fix="Explicitly set securityContext.runAsUser to a non-root UID"
                )

   
