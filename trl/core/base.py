# base parent class 

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class IR(ABC):
    """Marker base for all IRs emitted by the DSL (DeploymentIR, ServiceIR, HelmIR...)."""
    kind: str

class Module(ABC):
    """Every engine implements Module. Swappable with a remote client via same interface."""
    name: str

    @abstractmethod
    def process(self, ctx: "RunContext") -> None:
        ...

    async def process_async(self, ctx: "RunContext") -> None:
        return self.process(ctx)
    
class Report:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.optimizations: List[str] = []

class RemoteModuleClient(Module, ABC):
    """Drop-in replacement for Module in registry without changing callers."""
    pass
