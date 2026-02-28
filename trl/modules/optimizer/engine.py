from trl.core.base import Module
from trl.core.context import RunContext
from trl.core.ir import DeploymentIR, ServiceIR, PVCIR, SecretIR, ConfigMapIR, IngressIR

class OptimizerEngine(Module):
    name = "optimizer-engine"

    def process(self, ctx: RunContext) -> None:
        print("Processing optimizition........\n")
        for ir in ctx.irs:
   
            if isinstance(ir, DeploymentIR):

                if ir.cpu is None:

                    ir.cpu = "100m"
                    ctx.report.optimizations.append(f"{ir.name}: cpu defaulted to {ir.cpu}" )
                if ir.memory is None:
                    ir.memory = "64Mi"
                    ctx.report.optimizations.append(f"{ir.name}: memory defaulted to {ir.memory}" )

            elif isinstance(ir, ServiceIR):
                print("inside serviceIR")
    
                for p in ir.ports:
                    if p["port"] == 80:
                        p["port"] = 8020
                        p["targetPort"] = 8020
                        ir.name = "nginx-v2-service"

            elif isinstance(ir, IngressIR):
                pass            
            elif isinstance(ir, ConfigMapIR):
                pass
            elif isinstance(ir, SecretIR):
                pass

            elif isinstance(ir, PVCIR):
                # Default access mode
                if not ir.access_modes:
                    ir.access_modes = ["ReadWriteOnce"]
                # Default storage size
                ir.storage = "1Gi"
            print("in optimize ir: ", ir.__dict__)