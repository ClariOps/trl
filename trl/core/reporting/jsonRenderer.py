import json

class JSONRenderer:
    def __init__(self, report, verbose=False):
        self.report = report
        self.verbose = verbose

    def render(self):
        grouped = self._group_all(self.report)

        output = {
            "status": self._derive_status(len(self.report.errors), len(self.report.warnings)),
            "summary": self._build_summary(self.report),
            "resources": grouped
        }

        return json.dumps(output, indent=2)

    def _group_all(self, report):
        from collections import defaultdict

        grouped = defaultdict(lambda: {
            "errors": [],
            "warnings": [],
            "optimizations": []
        })

        for e in report.errors:
            grouped[e.resource]["errors"].append(self._format_event(e))

        for e in report.warnings:
            grouped[e.resource]["warnings"].append(self._format_event(e))

        for e in report.optimizations:
            grouped[e.resource]["optimizations"].append(self._format_event(e))

        return grouped   
    
    def _format_event(self, e):
        return {
            "rule": e.rule,
            "severity": e.severity,
            "category": e.category
        }
    
    def _build_summary(self, report):
        return {
            "errors": len(report.errors),
            "warnings": len(report.warnings),
            "optimizations": len(report.optimizations)


        }
    def _derive_status(self, errors, warnings):
        if errors > 0:
            return "FAILED"
        return "PASSED"