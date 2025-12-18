
from typing import Dict, List, Optional,Any
from trl.core.base import IR

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
