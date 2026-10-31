from typing import Dict, List, Optional,Any
from trload.core.base import IR


class PVCIR(IR):
    kind = "PVCIR"

    def __init__(
        self,
        *,
        name: str = None,
        storage: str = None,                         # "1Gi", "5Gi"
        access_modes: list = None,         # ["ReadWriteOnce"]
        storage_class: str = None,         # "standard"
        manifest: dict = None
    ):
        if manifest:
            self._from_manifest(manifest)
        else:
            self.name = name
            self.storage = storage
            self.access_modes = access_modes or ["ReadWriteOnce"]
            self.storage_class = storage_class
  
    def __repr__(self):
        return f"PVCIR(name={self.name}, size={self.storage}, access={self.access_modes})"
   

    def _from_manifest(self, m: dict):
        self.name = m["metadata"]["name"]
        self.storage = m["spec"]["resources"]["requests"]["storage"]
        self.access_modes = m["spec"].get("accessModes", ["ReadWriteOnce"])
        self.storage_class = m["spec"].get("storageClassName")

    def to_manifest(self) -> dict:
        manifest = {
            "apiVersion": "v1",
            "kind": "PersistentVolumeClaim",
            "metadata": {
                "name": self.name
            },
            "spec": {
                "accessModes": self.access_modes,
                "resources": {
                    "requests": {
                        "storage": self.storage
                    }
                }
            }
        }

        if self.storage_class:
            manifest["spec"]["storageClassName"] = self.storage_class

        return manifest   
    