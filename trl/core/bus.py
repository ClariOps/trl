import logging
import asyncio
from typing import List
from .base import Module
from .context import RunContext

logger = logging.getLogger(__name__)
class ServiceBus:
    def __init__(self, seq_before: List[Module],parallel_checks: List[Module], seq_after: List[Module]):
        self.seq_before = seq_before
        self.parallel_checks = parallel_checks
        self.seq_after = seq_after

    def run(self, ctx: RunContext) -> RunContext:
        for m in self.seq_before:
            m.process(ctx)

        if self.parallel_checks:
            async def run_parallel():
                await asyncio.gather(*[m.process_async(ctx) for m in self.parallel_checks])
            asyncio.run(run_parallel())

        if len(ctx.report.errors):
            logger.error("❌ Safety Gatekeeper: High-severity errors detected. Halting pipeline. Deployment aborted.")
            return
        
        for m in self.seq_after:
            m.process(ctx)
            
        return ctx
