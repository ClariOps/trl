from trl.core.base import Module
from trl.core.context import RunContext
from trl.core.ir import DeploymentIR, ServiceIR, PVCIR

class OptimizerEngine(Module):
    name = "optimizer-engine"

    def process(self, ctx: RunContext) -> None:
        print("Processing optimizition........\n")
        for ir in ctx.irs:
            print("in optimize ir: ", ir.__dict__)
            if isinstance(ir, DeploymentIR):
                # Direct IR mutation
                cpu_val = int(ir.cpu.replace("mi", ""))
                mem_val = int(ir.memory.replace("Mi", ""))

                if cpu_val < 200:
                    ir.cpu = "100mi"
                if mem_val < 128:
                    ir.memory = "64Mi"
            
            elif isinstance(ir, ServiceIR):
                print("inside serviceIR")
                if not ir.ports:
                    ir.ports = [{"port": 8010, "targetPort": 80}]
                if ir.service_type not in ["ClusterIP", "NodePort", "LoadBalancer"]:
                    ir.service_type = "ClusterIP"
            
            elif isinstance(ir, PVCIR):
                # Default access mode
                if not ir.access_modes:
                    ir.access_modes = ["ReadWriteOnce"]
                # Default storage size
                ir.storage = "1Gi"