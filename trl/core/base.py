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
        if not self.match(ir):
            return False

        if not self.condition(ir):
            logger.debug(f"{self.name}: not applicable (resource={ir.name})")
            return False

        logger.debug(f"{self.name}: executing (resource={ir.name})")
        self.action(ir, ctx)
        logger.debug(f"{self.name}: completed")
        return True
    
    def enabled(self, ctx):
        if ctx.opts.get("skip_rules") and self.name in ctx.opts["skip_rules"]:
            logger.debug(f"{self.name}: skipped (disabled via CLI)")
            return False

        if ctx.opts.get("allow_rules") and self.name not in ctx.opts["allow_rules"]:
            logger.debug(f"{self.name}: skipped (not in allow list)")
            return False

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
        if not self.match(ir):
            return False

        if not self.condition(ir):
            logger.debug(f"{self.name}: not applicable (resource={ir.name})")
            return False
                    
        logger.debug(f"{self.name}: executing (resource={ir.name})")
        self.validate(ir, ctx)
        logger.debug(f"{self.name}: completed")       
        return True
    
    def enabled(self, ctx):
        if ctx.opts.get("skip_rules") and self.name in ctx.opts["skip_rules"]:
            logger.debug(f"{self.name}: skipped (disabled via CLI)")
            return False

        if ctx.opts.get("allow_rules") and self.name not in ctx.opts["allow_rules"]:
            logger.debug(f"{self.name}: skipped (not in allow list)")
            return False

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
        if not self.match(ir):
            return False

        if not self.condition(ir):
            logger.debug(f"{self.name}: not applicable (resource={ir.name})")
            return False
       

        logger.debug(f"{self.name}: executing (resource={ir.name})")
        self.action(ir, ctx)
        logger.debug(f"{self.name}: completed")       
        return True
    
    def enabled(self, ctx):
        if ctx.opts.get("skip_rules") and self.name in ctx.opts["skip_rules"]:
            logger.debug(f"{self.name}: skipped (disabled via CLI)")
            return False

        if ctx.opts.get("allow_rules") and self.name not in ctx.opts["allow_rules"]:
            logger.debug(f"{self.name}: skipped (not in allow list)")
            return False

        return True
class ReportEvent:
    def __init__(self, rule, resource, message, level, engine,  category, severity, issue, impact, fix):
        self.rule = rule
        self.resource = resource
        self.message = message
        self.level = level
        self.engine = engine
        self.category = category
        self.severity = severity
        self.issue= issue
        self.impact= impact
        self.fix= fix
    def __str__(self):
        return f"[{self.rule}] {self.resource}: {self.message}"

class Report:
    def __init__(self):
        self.events = []

    def _add(self, level, engine, category, severity, rule, resource, message, issue=None, impact=None, fix=None):
       # 🚨 Enforce consistency       
        if level == "optimization":
            if not message:
                raise ValueError("Optimization event must have 'message'")
            if issue or impact or fix:
                raise ValueError("Optimization cannot use issue/impact/fix")

        else:  # warning / error
            if not issue:
                raise ValueError("Problem event must have 'issue'")
            if not fix:
                raise ValueError("Problem event must have 'fix'")
            if message:
                raise ValueError("Do not use 'message' for problem events")
            
        event = ReportEvent(
            engine=engine,
            category=category,
            severity=severity,
            level=level,
            rule=rule,
            resource=resource,
            message=message,
            issue=issue,
            impact=impact,
            fix=fix
        )
        self.events.append(event)

    def optimization(self, rule, engine, resource, message, category="generic", severity="low"):
        self._add("optimization", engine, category, severity, rule, resource, message)

    def warning(self, rule, engine, resource, message=None, issue=None, impact=None, fix=None, category="generic" , severity="low" ):
        self._add("warning", engine, category, severity, rule, resource, message, issue, impact, fix)
    def error(self, rule, engine, resource, message=None, issue=None, impact=None, fix=None, category= "generic", severity="low"):
        self._add("error", engine, category, severity, rule, resource, message, issue, impact, fix)

    @property
    def errors(self):
        return [e for e in self.events if e.level == "error"]

    @property
    def warnings(self):
        return [e for e in self.events if e.level == "warning"]

    @property
    def optimizations(self):
        return [e for e in self.events if e.level == "optimization"]

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
