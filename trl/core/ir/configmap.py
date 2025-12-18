from typing import Dict, List, Optional,Any
from trl.core.base import IR

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
