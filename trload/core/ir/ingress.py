
from typing import Dict, List, Optional,Any
from trload.core.base import IR

class IngressIR(IR):
    kind = "IngressIR"
    
    def __init__(
        
        self, 
        *,
        name: str= None,
        rules: list = None,   # [{"host": "example.com", "paths": [{"path": "/", "service": "svc", "port": 80}]}]
        annotations: dict = None,
        manifest: dict = None,):
            
        if manifest:
            self._from_manifest(manifest)
        else:
            self.name = name
            self.rules = rules or []
            self.annotations = annotations or {}

    
    def _from_manifest(self, m: Dict[str, Any]) -> None:
        metadata = m.get("metadata", {})
        spec = m.get("spec", {})

        rules = []

        for rule in spec.get("rules", []):
            host = rule.get("host")
            paths = []

            http = rule.get("http", {})
            for p in http.get("paths", []):
                backend = p.get("backend", {}).get("service", {})

                paths.append({
                    "path": p.get("path"),
                    "service": backend.get("name"),
                    "port": backend.get("port", {}).get("number"),
                })

            rules.append({
                "host": host,
                "paths": paths,
            })

        self.name = metadata.get("name")
        self.annotations = metadata.get("annotations", {})
        self.rules = rules
     

     
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
