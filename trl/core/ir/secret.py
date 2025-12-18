from typing import Dict, List, Optional,Any
from trl.core.base import IR
import base64

class SecretIR(IR):
    kind = "SecretIR"

    def __init__(
        self,
        name: str,
        data: dict,                 # plaintext key-value (DSL mode)
        secret_type: str = "Opaque",
        manifests: dict = None,
        from_user_yaml: bool = False,
    ):
        self.name = name
        self.data = data                    # plaintext in DSL mode
        self.secret_type = secret_type
        self.manifests = manifests or {}

    def __repr__(self):
        return f"SecretIR(name={self.name}, type={self.secret_type}, keys={list(self.data.keys())})"

    def to_manifest(self) -> dict:
        encoded_data = {
            k: base64.b64encode(v.encode()).decode()
            for k, v in self.data.items()
        }

        return {
            "apiVersion": "v1",
            "kind": "Secret",
            "metadata": {
                "name": self.name
            },
            "type": self.secret_type,
            "data": encoded_data
        }
    
