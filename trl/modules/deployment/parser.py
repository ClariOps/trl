from typing import Dict, List, Optional,Any
from trl.core.base import IR

class DeploymentIR(IR):
    kind = "DeploymentIR"
    def __init__(self, name: str, image: str, cpu: str, memory: str,
                 replicas: int = 1, ports: Optional[List[int]] = None,
                 labels: Optional[Dict[str,str]] = None,
                 manifests: List[Dict[str, Any]] = None):
        self.name = name
        self.image = image
        self.cpu = cpu
        self.memory = memory
        self.replicas = replicas
        self.ports = ports or []
        self.labels = labels or {"app": name}    
        self.manifests = manifests or []
    def __repr__(self):
        return f"DeploymentIR(name={self.name}, replicas={self.replicas}, cpu={self.cpu}, memory={self.memory}, image={self.image})"
    def to_manifest(self) -> Dict[str, Any]:
        return {
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "metadata": {"name": self.name, "labels": self.labels},
                    "spec": {
                        "replicas": self.replicas,
                        "selector": {"matchLabels": self.labels},
                        "template": {
                            "metadata": {"labels": self.labels},
                            "spec": {
                                "containers": [{
                                    "name": self.name,
                                    "image": self.image,
                                    "ports": [{"containerPort": p} for p in self.ports],
                                    "resources": {
                                        "requests": {"cpu": self.cpu, "memory": self.memory},
                                        "limits": {"cpu": self.cpu, "memory": self.memory},
                                    }
                                }]
                            }
                        }
                    }
            }    
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


class IngressIR(IR):
    kind = "IngressIR"
    
    def __init__(self, name: str,
        rules: list,   # [{"host": "example.com", "paths": [{"path": "/", "service": "svc", "port": 80}]}]
        annotations: dict = None,
        manifests: dict = None,):
            
            self.name = name
            self.rules = rules
            self.annotations = annotations or {}
            self.manifests = manifests or {}
    
    def __repr__(self):
        return f"IngressIR(name={self.name}, rules={self.rules})"
    
    def to_manifest(self):
        return {
            "apiVersion": "networking.k8s.io/v1",
            "kind": "Ingress",
            "metadata": {
                "name": self.name,
                "annotations": self.annotations,
            },
            "spec": {
                "rules": [
                    {
                        "host": rule["host"],
                        "http": {
                            "paths": [
                                {
                                    "path": p["path"],
                                    "pathType": "Prefix",
                                    "backend": {
                                        "service": {
                                            "name": p["service"],
                                            "port": {"number": p["port"]},
                                        }
                                    },
                                }
                                for p in rule["paths"]
                            ]
                        },
                    }
                    for rule in self.rules
                ]
            },
        }

class ConfigMapIR(IR):
    kind = "ConfigMapIR"

    def __init__(
        self,
        name: str,
        data: dict,
        manifests: dict = None,
    ):
        self.name = name
        self.data = data                  # key-value pairs
        self.manifests = manifests or {}
        
    def __repr__(self):
        return f"ConfigMapIR(name={self.name}, keys={list(self.data.keys())})"

    def to_manifest(self) -> dict:
        return {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "name": self.name
            },
            "data": self.data
        }

class HelmIR(IR):
    kind = "HelmIR"
    def __init__(self, chart_path: str):
        self.chart_path = chart_path

