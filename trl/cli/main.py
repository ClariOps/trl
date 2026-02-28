import argparse, yaml, logging

from trl.core.context import RunContext
from trl.app_pipelines.loader import load_user_irs

from trl.core.ir import (DeploymentIR, ServiceIR, HelmIR, IngressIR, ConfigMapIR, SecretIR, PVCIR)
from trl.modules.deployment.engine import DeploymentEngine
from trl.modules.optimizer.engine import OptimizerEngine
from trl.modules.security.engine import SecurityEngine
from trl.modules.cloud.engine import CloudEngine
from trl.modules.validator.engine import ValidatorEngine
from trl.modules.renderer.engine import RendererEngine
from trl.adapters.remote import HTTPModuleClient
from trl.core.bus import ServiceBus
from trl.core.reporting.renderer import render_report
from trl.core.logconfig.config import setup_logging


def main():
    p = argparse.ArgumentParser("trl")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("deploy")
    d.add_argument("--name")
    d.add_argument("--cpu")
    d.add_argument("--memory")
    d.add_argument("--image")
    d.add_argument("--helm")

    r = sub.add_parser("run")
    r.add_argument("file")
    r.add_argument("--target",choices=["local", "aks"], help="Deploy to Systems")

    r.add_argument("--helm")

    o = sub.add_parser("optimize")
    o.add_argument("file")
    o.add_argument("--target",choices=["local", "aks"], help="Deploy to Systems")
    o.add_argument("--context",help="Set Context to deploy")
    o.add_argument("--verbose", help="Detailed Reporting")
    args = p.parse_args()
    print("args response is:", args)

    #cli based
    setup_logging(verbose=args.verbose)
    logger = logging.getLogger(__name__)


    if args.cmd == "deploy":
        irs = []
        if args.helm:
            irs.append(HelmIR(args.helm))
        else:
            if not all([args.name, args.cpu, args.memory, args.image]):
                raise SystemExit("Missing required flags: --name --cpu --memory --image or use --helm")
            irs.append(DeploymentIR(name=args.name, image=args.image, cpu=args.cpu, memory=args.memory))
    
        ctx = RunContext(irs=irs, opts= {"helm": args.helm, "out_dir":"dist"})
        logger.info("Enter main module:", ctx.artifacts) 
        bus = ServiceBus(seq_before=[
                        #HTTPModuleClient("floyd", "http:/io.com"), 
                        DeploymentEngine(), 
                        OptimizerEngine()],
                        parallel_checks = [ValidatorEngine() ,SecurityEngine()],
                        seq_after = [CloudEngine()]
                        )
        print(bus.__dict__) 
        bus.run(ctx)
        print("after run context is: ",ctx.__dict__)

        render_report(ctx.report)    
    # DSL based
    
    elif args.cmd == "run":
        irs = load_user_irs(args.file)
        print("dsl irs are:", irs )

        opts = {}
        if args.target:
            opts["target"] = args.target

        if args.target != "local" and args.context:
            opts["context"] = args.context            
   
        ctx = RunContext(irs=irs, opts= opts)
        print("\nArtifacts:", ctx.artifacts) 
        bus = ServiceBus(seq_before=[
                        #HTTPModuleClient("floyd", "http:/io.com"), 
                        DeploymentEngine(), 
                        OptimizerEngine()],
                        parallel_checks = [
                        ValidatorEngine() ,SecurityEngine()],
                        seq_after = [RendererEngine(),CloudEngine()]
                        )
        print(bus.__dict__) 
        bus.run(ctx)
        print("after run context is: ",ctx.__dict__)

        if ctx.report.errors or ctx.report.warnings:
            print("Report:", {"errors": ctx.report.errors, "warnings": ctx.report.warnings})    

    # yaml based

    elif args.cmd == "optimize":
        irs = []
        data = {}
        with open(args.file, "r") as f:
            data = yaml.safe_load(f)
        
        logger.info("Enter main module, Yaml data")
        irs = []
        #irs.append(DeploymentIR(name="XX", image="XX", cpu="XX", memory="XX", manifests=data))
        #irs.append(ServiceIR(name="XX", selector="XX", ports="XX", service_type="XX", manifests=data))
        #irs.append(IngressIR(name="XX", rules="XX", annotations="XX", manifests=data))
        #irs.append(ConfigMapIR(name="XX",data="XX", manifests=data))
        #irs.append(SecretIR(name="XX",data="XX", manifests=data))
        #irs.append(PVCIR(name="XX", size="XX", access_modes="XX", storage_class="XX", manifests=data))
        
        irs.append(DeploymentIR(manifest=data))
        #irs.append(ServiceIR(manifest=data))
        
        #irs.append(IngressIR(manifest=data))
        #irs.append(ConfigMapIR(manifest=data))
        #irs.append(SecretIR(manifest=data)) 
        #irs.append(PVCIR(manifest=data))
    
        opts = {}
        if args.target:
            opts["target"] = args.target

        if args.target != "local" and args.context:
            opts["context"] = args.context            
        
        ctx = RunContext(irs=irs, opts=opts)
        bus = ServiceBus(seq_before=[
                        #HTTPModuleClient("floyd", "http:/io.com"), 
                        OptimizerEngine()],
                        parallel_checks = [],
                        #[ValidatorEngine() ,SecurityEngine()],
                        seq_after = [RendererEngine(), CloudEngine()]
                        )
        bus.run(ctx)

        render_report(ctx.report, args.verbose)

if __name__ == "__main__":
    main()
