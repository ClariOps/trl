# reporting/renderer.py

def render_report(report, verbose=True):
    if verbose:
        _render_details(report)
    _render_summary(report)

def _render_summary(report):
    total_errors = len(report.errors)
    total_warnings = len(report.warnings)
    total_opts = len(report.optimizations)

    total = total_errors + total_warnings + total_opts


    print("\n" + "─" * 48)
    print("Truck Overload Summary")
    print("─" * 48)

    print(f"Optimizations : {total_opts}")
    print(f"Warnings      : {total_warnings}")
    print(f"Errors        : {total_errors}")
    print(f"Total Issues  : {total}")
    if report.has_errors():
        print("\nStatus: FAILED")
    else:
        print("\nStatus: SUCCESS")

    print("─" * 48 + "\n")

def _render_details(report):
    sections = {
        "Errors": report.errors,
        "Warnings": report.warnings,
        "Optimizations": report.optimizations,
        "Suggestions": report.suggestions,
    }

    active = {k: v for k, v in sections.items() if v}
    if not active:
        return

    print("\n[REPORT]")
    print("-" * 40)

    for title, items in active.items():
        print(f"\n{title}:")
        for item in items:
            _print_item(item)

LEVEL_ICON = {
    "optimization": "💡",
    "warning": "⚠",
    "error": "❌",
    "suggestion": "👉"
}

def _print_item(item):
    icon = LEVEL_ICON.get(item.level.lower(), "•")

    print(f"  {icon} {item.rule}")
    print(f"     Resource : {item.resource}")
    print(f"     Message  : {item.message}")