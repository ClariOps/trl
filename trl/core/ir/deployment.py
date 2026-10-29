from typing import Dict, List, Optional,Any
from trl.core.base import IR
from copy import deepcopy

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
        self.containers = containers or []   
        self.resources = {
            "requests": {"cpu": None, "memory": None},
            "limits": {"cpu": None, "memory": None},
        }

        if manifest is not None:
            self._from_manifest(manifest)
        else:
            self._from_flags(
                name=name,
                image=image,
                cpu=cpu,
                memory=memory,
                replicas=replicas,
                ports=ports,
                labels=labels
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
        self.manifest = deepcopy(m)

        metadata = self.manifest.get("metadata", {})
        spec = self.manifest.get("spec", {})
        template = spec.get("template", {})
        pod_spec = template.get("spec", {})

        # Preserve complete container definitions, including securityContext,
        # env, probes, volumeMounts, and other fields not modeled by the IR.
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

        self.resources["requests"] = deepcopy(resources.get("requests", {}))
        self.resources["limits"] = deepcopy(resources.get("limits", {}))

            
    def to_manifest(self) -> Dict[str, Any]:
        if hasattr(self, "manifest"):
            # Start with the complete original manifest.
            manifest = deepcopy(self.manifest)

            metadata = manifest.setdefault("metadata", {})
            spec = manifest.setdefault("spec", {})
            template = spec.setdefault("template", {})
            template_metadata = template.setdefault("metadata", {})
            pod_spec = template.setdefault("spec", {})

            metadata["name"] = self.name

            if self.labels is not None:
                metadata["labels"] = deepcopy(self.labels)
                template_metadata["labels"] = deepcopy(self.labels)
                spec.setdefault("selector", {})["matchLabels"] = deepcopy(
                    self.labels
                )

            # Reflect current IR state, including optimizer changes.
            if self.replicas is not None:
                spec["replicas"] = self.replicas

            containers = deepcopy(self.containers)

            if containers:
                container = containers[0]

                if self.name is not None:
                    container["name"] = self.name

                if self.image is not None:
                    container["image"] = self.image

                if self.ports:
                    container["ports"] = [
                        {"containerPort": port}
                        for port in self.ports
                    ]

                # Update modeled resources while preserving unrelated resource
                # keys and the rest of the container configuration.
                resources = deepcopy(container.get("resources", {}))

                for resource_type in ("requests", "limits"):
                    current = self.resources.get(resource_type, {})
                    existing = resources.get(resource_type, {})

                    if current:
                        existing.update({
                            key: value
                            for key, value in current.items()
                            if value is not None
                        })
                        resources[resource_type] = existing

                if resources:
                    container["resources"] = resources

                pod_spec["containers"] = containers

            return manifest

        # Fallback for DeploymentIR instances created from CLI flags.
        container = {"name": self.name, "image": self.image}

        if self.ports:
            container["ports"] = [
                {"containerPort": port} for port in self.ports
            ]

        resources = {}
        for resource_type in ("requests", "limits"):
            values = {
                key: value
                for key, value in self.resources.get(resource_type, {}).items()
                if value is not None
            }
            if values:
                resources[resource_type] = values

        if resources:
            container["resources"] = resources

        return {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": self.name,
                "labels": self.labels,
            },
            "spec": {
                "replicas": self.replicas,
                "selector": {"matchLabels": self.labels},
                "template": {
                    "metadata": {"labels": self.labels},
                    "spec": {"containers": [container]},
                },
            },
        }        
        
        
    
    
    

