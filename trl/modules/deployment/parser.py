from typing import Dict, List, Optional
from trl.core.base import IR

class DeploymentIR(IR):
    kind = "DeploymentIR"
    def __init__(self, name: str, image: str, cpu: str, memory: str,
                 replicas: int = 1, ports: Optional[List[int]] = None,
                 labels: Optional[Dict[str,str]] = None):
        self.name = name
        self.image = image
        self.cpu = cpu
        self.memory = memory
        self.replicas = replicas
        self.ports = ports or []
        self.labels = labels or {"app": name}
    def __repr__(self):
        return f"DeploymentIR(name={self.name}, replicas={self.replicas}, cpu={self.cpu}, memory={self.memory}, image={self.image})"
class ServiceIR(IR):
    kind = "ServiceIR"
    def __init__(self, name: str, selector: Dict[str,str], port: int, type: str = "ClusterIP"):
        self.name = name
        self.selector = selector
        self.port = port
        self.type = type

class HelmIR(IR):
    kind = "HelmIR"
    def __init__(self, chart_path: str):
        self.chart_path = chart_path
