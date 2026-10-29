from typing import Any, Dict, List, Optional
from .base import IR, Report

class RunContext:
    """Shared state through the pipeline; engines communicate only via ctx."""
    def __init__(self, *, irs: Optional[List[IR]] = None, report=None, opts: Optional[Dict[str, Any]] = None):
        self.irs: List[IR] = irs or []
        self.opts: Dict[str, Any] = opts or {}
        self.report= report or Report()
        self.manifests: List[Dict[str, Any]] = []
        self.artifacts: Dict[str, Any] = {}
