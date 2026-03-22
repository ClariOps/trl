# base parent class 

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import logging
logger = logging.getLogger(__name__)

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

    def execute(self, ir, ctx):

        if hasattr(ctx, "opts"):
            if ctx.opts.get("skip_rules"):
                if self.name in ctx.opts["skip_rules"]:
                    logger.warning(f"Initiate skip rules {self.name}")
                    return False

            if ctx.opts.get("allow_rules"):
                if self.name not in ctx.opts["allow_rules"]:
                    return False

        if not self.match(ir):
            return False

        if not self.condition(ir):
            return False

                        
        self.action(ir, ctx)
        return True    

class ValidationRule:

    name = "base-validation"

    def match(self, ir):
        return True

    def validate(self, ir, ctx):
        pass

    def execute(self, ir, ctx):

        if not self.match(ir):
            return False

        self.validate(ir, ctx)
        return True  
class ReportEvent:
    def __init__(self, rule, resource, message, level):
        self.rule = rule
        self.resource = resource
        self.message = message
        self.level = level
    def __str__(self):
        return f"[{self.rule}] {self.resource}: {self.message}"

class Report:
    def __init__(self):
        self.events = []
    
    def _add(self, level, rule, resource, message):
        event = ReportEvent(
            level=level,
            rule=rule,
            resource=resource,
            message=message
        )
        self.events.append(event)

    def optimization(self, rule, resource, message):
        self._add("optimization", rule, resource, message)

    def warning(self, rule, resource, message):
        self._add("warning", rule, resource, message)

    def error(self, rule, resource, message):
        self._add("error", rule, resource, message)

    def suggestion(self, rule, resource, message):
        self._add("suggestion", rule, resource, message)

    @property
    def errors(self):
        return [e for e in self.events if e.level == "error"]
    
    @property
    def warnings(self):
        return [e for e in self.events if e.level == "warning"]

    @property
    def optimizations(self):
        return [e for e in self.events if e.level == "optimization"]

    @property
    def suggestions(self):
        return [e for e in self.events if e.level == "suggestion"]
    
    def has_errors(self):
        return any(e.level == "error" for e in self.events)
class RemoteModuleClient(Module, ABC):
    """Drop-in replacement for Module in registry without changing callers."""
    pass
