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

class ReportEvent:
    def __init__(self, rule, resource, message):
        self.rule = rule
        self.resource = resource
        self.message = message
    def __str__(self):
        return f"[{self.rule}] {self.resource}: {self.message}"

class Report:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.optimizations: List[str] = []
        self.suggestions: List[str] = []
    
    def add_error(self, event):
        self.errors.append(event)

    def add_warning(self, event):
        self.warnings.append(event)

    def add_optimization(self, event):
        self.optimizations.append(event)
    
    def add_suggestion(self, event):
        self.suggestions.append(event)

    def has_errors(self):
        return len(self.errors) > 0

class RemoteModuleClient(Module, ABC):
    """Drop-in replacement for Module in registry without changing callers."""
    pass
