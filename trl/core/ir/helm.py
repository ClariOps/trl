from typing import Dict, List, Optional,Any
from trl.core.base import IR

class HelmIR(IR):
    kind = "HelmIR"
    def __init__(self, chart_path: str):
        self.chart_path = chart_path

