from collections import defaultdict



class ReportsRenderer:
    def __init__(self, report, verbose=False):
        self.report = report
        self.verbose = verbose


    def render(self):
        grouped = self._group_all()
        print("\n")
        for resource, sections in grouped.items():
            print("━" * 50) 
            print(f"\n📦 Resource: {resource}\n")
         
            # Errors
            for e in sections["errors"]:
                self._render_event(e, "Errors")

            # Warnings
            for e in sections["warnings"]:
                self._render_event(e, "Warnings")

            # Optimizations
            for e in sections["optimizations"]:
                self._render_event(e, "Optimizations")
        
        self._print_footer()

    def _print_footer(self):
        print("━" * 50) 
        print(f"\n📊 Summary\n"
              f"Errors: {len(self.report.errors)}\t"
              f"Warnings: {len(self.report.warnings)}\t"
              f"Optimizations: {len(self.report.optimizations)}\n")

        
        status = "FAILED" if self.report.errors else "PASSED"
        icon = "❌" if self.report.errors else "✔"

        print(icon, f"Status: {status}")
        if self.report.errors:
            print("💡 Fix issues before they reach your cluster")
        total = self._total_issues()
 
   

    def _render_event(self, e, title):        
        print(f"{self._icon(title)} {e.severity.upper()}: {e.rule}")

        if self.verbose:     
            if e.level == "optimization":
                print(f"\nChange: {e.message}")
                print(f"Engine: {e.engine}")
            else:
                print(f"\nIssue : {e.issue}")

                if getattr(e, "impact", None):
                    print(f"Impact: {e.impact}")

                if getattr(e, "fix", None):
                    print(f"Fix   : {e.fix}")
         
        
                print(f"Engine: {e.engine}")
                print(f"Category: {e.category}")       
        print()
    def _print_summary(self):
        print("━" * 50) 
        print("📊 Summary")
        print("━" * 50) 

        errors = len(self.report.errors)
        warnings = len(self.report.warnings)
        optimizations = len(self.report.optimizations)

        print(f"Errors        : {errors}")
        print(f"Warnings      : {warnings}")
        print(f"Optimizations : {optimizations}")

        total = self._total_issues()

        print("━" * 50) 
        print(f"Total Issues    : {total}")

        status = "FAILED" if errors else "PASSED"
        icon = "❌" if errors else "✔"

        print(f"\nStatus: {icon} {status}")
    
    
    def _total_issues(self):
        return (
            len(self.report.errors)
            + len(self.report.warnings)
            + len(self.report.optimizations)
        )
    
    def _icon(self, title):
        if title.upper() == "ERRORS":
            return "❌"
        elif title.upper() == "WARNINGS":
            return "⚠"
        else:
            return "💡"
        
    def _group_all(self):
        from collections import defaultdict

        grouped = defaultdict(lambda: {
            "errors": [],
            "warnings": [],
            "optimizations": []
        })

        for e in self.report.errors:
            grouped[e.resource]["errors"].append(e)

        for e in self.report.warnings:
            grouped[e.resource]["warnings"].append(e)

        for e in self.report.optimizations:
            grouped[e.resource]["optimizations"].append(e)

        return grouped