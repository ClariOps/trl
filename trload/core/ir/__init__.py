from trload.core.base import IR

from .deployment import DeploymentIR
from .service import ServiceIR
from .ingress import IngressIR
from .configmap import ConfigMapIR
from .secret import SecretIR
from .pvc import PVCIR
from .helm import HelmIR

__all__ = [
    "IR",
    "DeploymentIR",
    "ServiceIR",
    "IngressIR",
    "ConfigMapIR",
    "SecretIR",
    "PVCIR",
    "HelmIR",
]
