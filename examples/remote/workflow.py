import json

from trl.adapters.remote import HTTPModuleClient
from trl.modules.renderer.engine import RendererEngine

with open("examples/remote/registry.json") as f:
    registry = json.load(f)


optimizer = registry["X092@jjj"]
validator = registry["Y481@abc"]
security = registry["Z481@abc"]

workflow = {
    "seq_before": [
        HTTPModuleClient(
            name=optimizer["name"],
            endpoint=optimizer["endpoint"],
        )
    ],

    "parallel_checks": [],

    "seq_after": [
        HTTPModuleClient(
            name=validator["name"],
            endpoint=validator["endpoint"],
        ),
        HTTPModuleClient(
            name=security["name"],
            endpoint=security["endpoint"],
        ),
        RendererEngine()
        
    ],
}