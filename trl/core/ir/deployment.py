from typing import Dict, List, Optional,Any
from trl.core.base import IR


class DeploymentIR(IR):
    kind = "DeploymentIR"
    def __init__(
            self,
            *,
            name: str = None, 
            image: str = None, 
            cpu: str = None, 
            memory: str = None,
            replicas: int = 1, 
            ports: Optional[List[int]] = None,
            labels: Optional[Dict[str,str]] = None,
            manifest: List[Dict[str, Any]] = None):
        if manifest:
            self._from_manifest(manifest)
        else:
            self.name = name
            self.image = image
            self.cpu = cpu
            self.memory = memory
            self.replicas = replicas
            self.ports = ports or []
            self.labels = labels or {"app": name}    
            
    def __repr__(self):
        return f"DeploymentIR(name={self.name}, replicas={self.replicas}, cpu={self.cpu}, memory={self.memory}, image={self.image})"
    
    def _from_manifest(self, m: Dict[str, Any]) -> None:
        metadata = m.get("metadata", {})
        spec = m.get("spec", {})
        template = spec.get("template", {})
        pod_spec = template.get("spec", {})

        containers = pod_spec.get("containers", [])
        container = containers[0] if containers else {}

        resources = container.get("resources", {})
        requests = resources.get("requests", {})

        self.name = metadata.get("name")
        self.labels = template.get("metadata", {}).get(
            "labels", metadata.get("labels", {})
        )
        self.replicas = spec.get("replicas", 1)
        self.image = container.get("image")

        self.ports = [
            p.get("containerPort")
            for p in container.get("ports", [])
            if p.get("containerPort") is not None
        ]

        self.cpu = requests.get("cpu")
        self.memory = requests.get("memory")   
   
   
    def to_manifest(self) -> Dict[str, Any]:
        
        container = {
            "name": self.name,
            "image": self.image,
        }

        if self.ports:
            container["ports"] = [
                {"containerPort": p} for p in self.ports
            ]

        if self.cpu or self.memory:
            container["resources"] = {
                "requests": {},
                "limits": {},
            }
            if self.cpu:
                container["resources"]["requests"]["cpu"] = self.cpu
                container["resources"]["limits"]["cpu"] = self.cpu
            if self.memory:
                container["resources"]["requests"]["memory"] = self.memory
                container["resources"]["limits"]["memory"] = self.memory
        
        
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
                                "containers": [container]
                            }
                        }
                    }
            }    


