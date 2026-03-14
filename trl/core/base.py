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

class OptimizationRule:
    name = "rule"
    category = "generic"
    capability = None

    def match(self, ir):
        if self.capability and ir.capability != self.capability:
            return False
        return True

    def condition(self, ir):
        return False

    def action(self, ir, ctx):
        pass    

class ValidationRule:

    name = "base-validation"

    def match(self, ir):
        return True

    def validate(self, ir, ctx):
        pass


class Report:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.optimizations: List[str] = []
        self.suggestions: List[str] = []
    
    def add_error(self, msg):
        self.errors.append(msg)

    def add_warning(self, msg):
        self.warnings.append(msg)

    def add_optimization(self, msg):
        self.optimizations.append(msg)
    
    def add_suggestion(self, msg):
        self.suggestions.append(msg)

    def has_errors(self):
        return len(self.errors) > 0

class RemoteModuleClient(Module, ABC):
    """Drop-in replacement for Module in registry without changing callers."""
    pass
