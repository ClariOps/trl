from typing import Dict, List, Optional,Any
from trload.core.base import IR
import base64

class SecretIR(IR):
    kind = "SecretIR"

    def __init__(
        self,
        *,
        name: str = None,
        data: Dict[str, str] = None,                 # plaintext key-value (DSL mode)
        secret_type: str = "Opaque",
        manifest: dict = None,

    ):   
        if manifest:
           self._from_manifest(manifest)
        else:
            
            if not name or data is None:
                raise ValueError("name and data are required when manifest is not provided")    
            
            self.name = name
            self.data = data                    # plaintext in DSL mode
            self.secret_type = secret_type
            

    def __repr__(self):
        return f"SecretIR(name={self.name}, type={self.secret_type}, keys={list(self.data.keys())})"

    def _from_manifest(self, m: dict):
        self.name = m["metadata"]["name"]
        self.secret_type = m.get("type", "Opaque")
        
        if "stringData" in m:
            self.data = m["stringData"]
        else:
        # decode base64 → plaintext
            self.data = {
            k: base64.b64decode(v).decode()
            for k, v in m.get("data", {}).items()
            }
            
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
    
