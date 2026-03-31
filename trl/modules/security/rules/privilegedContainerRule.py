from trl.core.base import SecurityRule


class PrivilegedContainerRule(SecurityRule):

    name = "privileged-container"
    category = "security"
    
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
                    resource=ir.name,
                    message=f"Container '{c.get("name")}' is running in privileged mode → high security risk"
                )