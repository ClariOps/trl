import asyncio
from typing import List
from .base import Module
from .context import RunContext

class ServiceBus:
    def __init__(self, seq_before: List[Module]):
        self.seq_before = seq_before
        
    def run(self, ctx: RunContext) -> RunContext:
        print("inside bus1")
        for m in self.seq_before:
            m.process(ctx)


        return ctx
