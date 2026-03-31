from typing import Dict, List, Optional,Any
from trl.core.base import IR


class DeploymentIR(IR):
    kind = "DeploymentIR"
    def __init__(
            self,
            *,
            name: str = None, 
            image: str = None, 
            containers: List[Dict[str, Any]] = None,
            cpu: str = None, 
            memory: str = None,
            replicas: int = None, 
            ports: Optional[List[int]] = None,
            labels: Optional[Dict[str,str]] = None,
            manifest: List[Dict[str, Any]] = None):
            
        self.resources = {
            "requests": {"cpu": None, "memory": None},
            "limits": {"cpu": None, "memory": None},
        }

        if manifest:
            self._from_manifest(manifest)
        else:
            self._from_flags(
                name=name,
                image=image,
                cpu=cpu,
                memory=memory,
                replicas=replicas,
                ports=ports,
                labels=labels,
                containers=containers
            )

            
    def __repr__(self):
        return f"DeploymentIR(name={self.name}, replicas={self.replicas}, resources={self.resources}, image={self.image})"
    

    def _from_flags(self, *, name, image, cpu, memory, replicas, ports, labels):
        self.name = name
        self.image = image
        self.replicas = replicas
        self.ports = ports or []
        self.labels = labels or {"app": name}
        if cpu:
            self.resources["requests"]["cpu"] = cpu
    #        self.resources["limits"]["cpu"] = cpu

        if memory:
            self.resources["requests"]["memory"] = memory
     #       self.resources["limits"]["memory"] = memory

    def _from_manifest(self, m: Dict[str, Any]) -> None:
        metadata = m.get("metadata", {})
        spec = m.get("spec", {})
        template = spec.get("template", {})
        pod_spec = template.get("spec", {})

        self.containers = pod_spec.get("containers", [])
        container = self.containers[0] if self.containers else {}

        resources = container.get("resources", {})
    
        self.name = metadata.get("name")
        self.labels = template.get("metadata", {}).get(
            "labels", metadata.get("labels", {})
        )
        self.replicas = spec.get("replicas")
        self.image = container.get("image")
        
        
        self.ports = [
            p.get("containerPort")
            for p in container.get("ports", [])
            if p.get("containerPort") is not None
        ]
        # Canonical mapping
        self.resources["requests"] = resources.get("requests", {})
        self.resources["limits"] = resources.get("limits", {})
   
    def to_manifest(self) -> Dict[str, Any]:
        
        container = {
            "name": self.name,
            "image": self.image
        }

        if self.ports:
            container["ports"] = [
                {"containerPort": p} for p in self.ports
            ]
        resources = {}

        if any(self.resources["requests"].values()):
            resources["requests"] = {
            k: v for k, v in self.resources["requests"].items() if v
            }

        if any(self.resources["limits"].values()):
            resources["limits"] = {
            k: v for k, v in self.resources["limits"].items() if v
            }


        if resources:
            container["resources"] = resources
        
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


