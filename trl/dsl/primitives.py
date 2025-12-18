from typing import Dict, List, Optional
from trl.core.ir import (DeploymentIR, ServiceIR, HelmIR, PVCIR)

__DSL_IRS__: List[object] = []

def _emit(ir):
    __DSL_IRS__.append(ir)
    return ir

def deployment(name: str, *, cpu: str, memory: str, image: str, replicas: int = 1,
               ports: Optional[List[int]] = None, labels: Optional[Dict[str,str]] = None) -> DeploymentIR:
    return _emit(DeploymentIR(name=name, image=image, cpu=cpu, memory=memory,
                              replicas=replicas, ports=ports, labels=labels))

def service(name: str, *, selector: Dict[str,str], port: int, type: str = "ClusterIP") -> ServiceIR:
    return _emit(ServiceIR(name=name, selector=selector, port=port, type=type))

def pvc(
    name: str,
    *,
    storage: str,
    access_modes: Optional[list[str]] = None,
    storage_class: Optional[str] = None
) -> PVCIR:
    return _emit(
        PVCIR(
            name=name,
            storage=storage,
            access_modes=access_modes,
            storage_class=storage_class
        )
    )


def helm_chart(path: str) -> HelmIR:
    return _emit(HelmIR(chart_path=path))


