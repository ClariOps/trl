from trl.core.base import SecurityRule


class RunAsRootRule(SecurityRule):

    name = "run-as-root"
    category = "security"

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

        for c in ir.containers:
            sc = c.get("securityContext", {})

            name = c.get("name", "unknown")

            if sc.get("runAsUser") == 0:
                ctx.report.warning(
                    rule=self.name,
                    engine=self.engine,
                    category=self.category,
                    resource=ir.name,
                    message=f"Container '{name}' is running as root user (UID 0)"
                )

                ctx.report.suggestion(
                    rule=self.name,
                    engine=self.engine,
                    category=self.category,
                    resource=ir.name,
                    message=f"Set runAsUser to non-root (e.g., 1000) for container '{name}'"
                )

            # 🟡 Missing user (soft signal)
            elif "runAsUser" not in sc:
                ctx.report.suggestion(
                    rule=self.name,
                    engine=self.engine,
                    category=self.category,
                    resource=ir.name,
                    message=f"Container '{self.name}' does not define runAsUser → defaults to root"
                )