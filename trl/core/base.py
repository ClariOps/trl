# base parent class 

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class IR(ABC):
    """Marker base for all IRs emitted by the DSL (DeploymentIR, ServiceIR, HelmIR...)."""
    kind: str

