from trl.core.base import Module
from trl.core.context import RunContext
from trl.core.ir import DeploymentIR, ServiceIR, PVCIR, SecretIR, ConfigMapIR, IngressIR
import logging
logger = logging.getLogger(__name__)

class OptimizerEngine(Module):
    name = "optimizer-engine"

    def process(self, ctx: RunContext) -> None:
        logger.info("Processing optimizition........\n")
        for ir in ctx.irs:
   
            if isinstance(ir, DeploymentIR):


                req = ir.resources["requests"]

                if not req.get("cpu"):
                    req["cpu"] = "100m"
                    ir.resources["limits"]["cpu"] = "100m"

                    ctx.report.optimizations.append(f"[default-resource] {ir.name}: cpu defaulted to 100m")
                if not req.get("memory"):
                    req["memory"] = "64Mi"
                    ir.resources["limits"]["memory"] = "64Mi"

                    ctx.report.optimizations.append(f"[default-resource] {ir.name}: memory defaulted to 100m")
                        
                
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
            logger.debug(f"Optimize IR Data: {ir.__dict__}")