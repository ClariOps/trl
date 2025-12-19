from typing import Dict, List, Optional,Any
from trl.core.base import IR

class ConfigMapIR(IR):
    kind = "ConfigMapIR"

    def __init__(
        self,
        *,
        name: str = None,
        data: dict = None,
        manifest: dict = None,
    ):
        if manifest:
            self._from_manifest(manifest)
        else:        
            self.name = name
            self.data = data                  # key-value pairs
    
        
    def __repr__(self):
        return f"ConfigMapIR(name={self.name}, keys={list(self.data.keys())})"

    def _from_manifest(self, m: dict):
        self.name = m["metadata"]["name"]
        self.data = m.get("data")
       
    def to_manifest(self) -> dict:
        return {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "name": self.name
            },
            "data": self.data
        }
