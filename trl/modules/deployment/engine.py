from trl.core.base import Module
from trl.core.context import RunContext
from .parser import DeploymentIR, ServiceIR, HelmIR

class DeploymentEngine(Module):
    name = "deployment-engine"

    def process(self, ctx: RunContext) -> None:
        for ir in ctx.irs:
            if isinstance(ir, DeploymentIR):
                ctx.manifests.append({
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "metadata": {"name": ir.name, "labels": ir.labels},
                    "spec": {
                        "replicas": ir.replicas,
                        "selector": {"matchLabels": ir.labels},
                        "template": {
                            "metadata": {"labels": ir.labels},
                            "spec": {
                                "containers": [{
                                    "name": ir.name,
                                    "image": ir.image,
                                    "ports": [{"containerPort": p} for p in ir.ports],
                                    "resources": {
                                        "requests": {"cpu": ir.cpu, "memory": ir.memory},
                                        "limits": {"cpu": ir.cpu, "memory": ir.memory},
                                    }
                                }]
                            }
                        }
                    }
                })
            elif isinstance(ir, ServiceIR):
                ctx.manifests.append({
                    "apiVersion": "v1",
                    "kind": "Service",
                    "metadata": {"name": ir.name},
                    "spec": {
                        "type": ir.type,
                        "selector": ir.selector,
                        "ports": [{"port": ir.port, "targetPort": ir.port}],
                    }
                })
            elif isinstance(ir, HelmIR):
                pass
