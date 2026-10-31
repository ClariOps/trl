import json
from pathlib import Path
from trload.adapters.remote import HTTPModuleClient
from trload.modules.renderer.engine import RendererEngine

try:
    WORKFLOW_DIR = Path(__file__).resolve().parent
except NameError:
    # Fallback if trload executes the file via exec() without setting __file__
    # We resolve it relative to the script path argument itself
    import sys
    WORKFLOW_DIR = Path(sys.argv[0]).resolve().parent

REGISTRY_PATH = WORKFLOW_DIR / "registry.json"

with open(REGISTRY_PATH) as f:
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