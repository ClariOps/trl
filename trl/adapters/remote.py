from trl.core.base import RemoteModuleClient
from trl.core.context import RunContext

class HTTPModuleClient(RemoteModuleClient):
    def __init__(self, name: str, endpoint: str):
        self.name = name
        self.endpoint = endpoint

    def process(self, ctx: RunContext) -> None:
        raise NotImplementedError("Implement HTTP call to remote engine here")