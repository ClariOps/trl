class ReportsRenderer:
    def __init__(self, report, verbose=False):
        self.report = report
        self.verbose = verbose

    def render(self):
        
        self._render_section("Errors", self.report.errors, "❌")
        self._render_section("Warnings", self.report.warnings, "⚠")
        self._render_section("Optimizations", self.report.optimizations, "💡")
        self._print_summary()
        self._print_footer()

    def _print_footer(self):
        total = self._total_issues()
        print(f"Found {total} issues "
              f"({len(self.report.errors)} errors, "
              f"{len(self.report.warnings)} warnings, "
              f"{len(self.report.optimizations)} optimizations)\n")

    def _render_section(self, title, items, icon):
        if not items:
            return
        print("-" * 40)
        print(f"{icon} {title} ({len(items)})")
        print("-" * 40)

        for e in items:
            self._render_event(e)

    def _render_event(self, e):        
        print(f"[{e.severity.upper()}] {e.rule}")
        print(f"Resource: {e.resource}")

        if e.level == "optimization":
            print(f"Change   : {e.message}")
        else:
            print(f"Issue : {e.issue}")

            if getattr(e, "impact", None):
                print(f"Impact: {e.impact}")

            if getattr(e, "fix", None):
                print(f"Fix   : {e.fix}")
         
        if self.verbose:
            print(f"Engine: {e.engine}")
            print(f"Category: {e.category}")

        print()

    def _print_summary(self):
        print("-" * 40)
        print("Summary")
        print("-" * 40)

        print(f"Errors        : {len(self.report.errors)}")
        print(f"Warnings      : {len(self.report.warnings)}")
        print(f"Optimizations : {len(self.report.optimizations)}")

        total = self._total_issues()
        print("-" * 40)
        print(f"Total Issues  : {total}")

        status = "FAILED" if self.report.errors else "PASSED"
        icon = "❌" if self.report.errors else "✔"

        print(f"\nStatus: {icon} {status}")

    def _total_issues(self):
        return (
            len(self.report.errors)
            + len(self.report.warnings)
            + len(self.report.optimizations)
        )