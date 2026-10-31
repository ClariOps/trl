from typing import Dict, List, Optional,Any
from trload.core.base import IR

class HelmIR(IR):
    kind = "HelmIR"
    def __init__(self, chart_path: str):
        self.chart_path = chart_path

