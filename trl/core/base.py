# base parent class

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from enum import Enum

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
    capability = None
    engine = "optimizer"
    category = "generic"

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
                    logger.debug(f"Initiate skip rules {self.name}")
                    return False

            if ctx.opts.get("allow_rules"):
                if self.name not in ctx.opts["allow_rules"]:
                    logger.debug(f"Initiate allow rules {self.name}")
                    return False

        if not self.match(ir):
            return False

        if not self.condition(ir):
            logger.debug(f"Rules not matched: {self.name}")
            return False

        logger.debug(f"Rules executing : {self.name}")
        self.action(ir, ctx)
        logger.debug(f"Rules executed : {self.name}")
        return True

class ValidationRule:

    name = "base-validation"
    engine = "validator"
    category = "generic"
    def match(self, ir):
        return True

    def condition(self, ir):
        return False

    def validate(self, ir, ctx):
        pass

    def execute(self, ir, ctx):

                        

        if hasattr(ctx, "opts"):
            if ctx.opts.get("skip_rules"):
                if self.name in ctx.opts["skip_rules"]:
                    logger.debug(f"Initiate skip rules {self.name}")
                    return False

            if ctx.opts.get("allow_rules"):
                if self.name not in ctx.opts["allow_rules"]:
                    logger.debug(f"Initiate allow rules {self.name}")
                    return False
        if not self.match(ir):
            return False

        if not self.condition(ir):
            logger.debug(f"Rules not matched: {self.name}")
            return False
                    
        logger.debug(f"Rules executing : {self.name}")
        self.validate(ir, ctx)
        logger.debug(f"Rules executed : {self.name}")        
        return True

class SecurityRule:

    name = "Security-rule"
    engine = "security"
    category = "generic"
    def match(self, ir):
        return True

    def condition(self, ir):
        return False

    def action(self, ir, ctx):
        pass

    def execute(self, ir, ctx):

 
        if hasattr(ctx, "opts"):
            if ctx.opts.get("skip_rules"):
                if self.name in ctx.opts["skip_rules"]:
                    logger.debug(f"Initiate skip rules {self.name}")
                    return False

            if ctx.opts.get("allow_rules"):
                if self.name not in ctx.opts["allow_rules"]:
                    logger.debug(f"Initiate allow rules {self.name}")
                    return False     
        if not self.match(ir):
            return False

        if not self.condition(ir):
            logger.debug(f"Rules not matched: {self.name}")
            return False
       

        logger.debug(f"Rules executing : {self.name}")
        self.action(ir, ctx)
        logger.debug(f"Rules executed : {self.name}")        
        return True

class ReportEvent:
    def __init__(self, rule, resource, message, level, engine,  category, severity):
        self.rule = rule
        self.resource = resource
        self.message = message
        self.level = level
        self.engine = engine
        self.category = category,
        self.severity = severity
    def __str__(self):
        return f"[{self.rule}] {self.resource}: {self.message}"

class Report:
    def __init__(self):
        self.events = []

    def _add(self, level, engine, category, severity, rule, resource, message):
        event = ReportEvent(
            engine=engine,
            category=category,
            severity=severity,
            level=level,
            rule=rule,
            resource=resource,
            message=message
        )
        self.events.append(event)

    def optimization(self, rule, engine, resource, message, category="generic", severity="low"):
        self._add("optimization", engine, category, severity, rule, resource, message)

    def warning(self, rule, engine, resource, message, category= "generic", severity="low"):
        self._add("warning", engine, category, severity, rule, resource, message)
    def error(self, rule, engine, resource, message, category= "generic", severity="low"):
        self._add("error", engine, category, severity, rule, resource, message)

    def suggestion(self, rule, engine, resource, message, category= "generic", severity="low"):
        self._add("suggestion", engine, category, severity, rule, resource, message)

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
    

class RuleCategory(Enum):
    SCALING = "scaling"
    SECURITY = "security"
    COST = "cost"
    RELIABILITY = "reliability"
    NETWORK = "network"


class RuleSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "HIGH"
class RemoteModuleClient(Module, ABC):
    """Drop-in replacement for Module in registry without changing callers."""
    pass
