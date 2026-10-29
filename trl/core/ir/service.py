from typing import Dict, List, Optional,Any
from trl.core.base import IR

class ServiceIR(IR):
    kind = "ServiceIR"
    def __init__(
        self,
        *, 
        name: str = None, 
        selector: Dict[str,str] = None, 
        ports: List[Dict[str, int]] = None, 
        service_type: str = None,
        manifest: Dict[str, Any] = None):
            
            if manifest:
                 self._from_manifest(manifest)
            else:
                self.name = name
                self.selector = selector or {}
                self.ports = ports or [] # [{ "port": 80, "targetPort": 80, "nodePort": 30080 }]
                self.service_type = service_type or "ClusterIP"
            
    def __repr__(self):
        return f"ServiceIR(name={self.name}, type={self.service_type}, ports={self.ports})"    
    
    def _from_manifest(self, m: Dict[str, Any]) -> None:
        metadata = m.get("metadata", {})
        spec = m.get("spec", {})

        ports = []
        for p in spec.get("ports", []):
            ports.append({
                "port": p.get("port"),
                "targetPort": p.get("targetPort"),
                "nodePort": p.get("nodePort"),
                "protocol": p.get("protocol", "TCP"),
            })

        self.name = metadata.get("name")
        self.selector = spec.get("selector", {})
        self.ports = ports
        self.service_type = spec.get("type", "ClusterIP")
    
    def to_manifest(self) -> Dict[str, Any]:
        ports = []
        for p in self.ports:
            port_def = {
                "port": p["port"],
                "protocol": p.get("protocol", "TCP"),
                "targetPort": p.get("targetPort", p["port"]),
            }
            if p.get("nodePort"):
                port_def["nodePort"] = p["nodePort"]
            ports.append(port_def)

        return {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": self.name},
            "spec": {
                "type": self.service_type,
                "selector": self.selector,
                "ports": ports,
            },
        }