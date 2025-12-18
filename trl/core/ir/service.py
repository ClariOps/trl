from typing import Dict, List, Optional,Any
from trl.core.base import IR

class ServiceIR(IR):
    kind = "ServiceIR"
    def __init__(self, name: str, selector: Dict[str,str], ports: List[Dict[str, int]], service_type: str = "ClusterIP",manifests: Dict[str, Any] = None):
        self.name = name
        self.selector = selector
        self.ports = ports  # [{ "port": 80, "targetPort": 80, "nodePort": 30080 }]
        self.service_type = service_type
        self.manifests = manifests or {}

    def __repr__(self):
        return f"ServiceIR(name={self.name}, type={self.service_type}, ports={self.ports})"    

    def to_manifest(self) -> Dict[str, Any]:
        return {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": self.name},
            "spec": {
                "type": self.service_type,
                "selector": self.selector,
                "ports": self.ports,
            },
        }