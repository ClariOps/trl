import argparse, yaml, logging, glob, os

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
from trl.core.reporting.reportRenderer import ReportsRenderer
from trl.core.reporting.jsonRenderer import JSONRenderer
from trl.core.reporting.yamlRenderer import YamlRenderer

from trl.core.reporting.deprecatedRenderer import render_report
from trl.core.logconfig.config import setup_logging
from trl.cli.helper import IR_MAPPING, load_yaml_irs, build_opts, render_banner


def main():
    p = argparse.ArgumentParser("trl")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("deploy")
    d.add_argument("--name")
    d.add_argument("--cpu")
    d.add_argument("--memory")
    d.add_argument("--image")
    d.add_argument("--helm")

    d.add_argument("--target",choices=["local", "aks"], help="Deploy to Systems")
    d.add_argument("--verbose", help="Detailed Reporting")
    d.add_argument("--dry-run", action="store_true")
    d.add_argument("--skip-rules", action="store_true")  
    d.add_argument("--allow-rules", action="store_true")  

    r = sub.add_parser("run")
    r.add_argument("file")
    r.add_argument("--target",choices=["local", "aks"], help="Deploy to Systems")
    r.add_argument("--verbose", help="Detailed Reporting")
    r.add_argument("--helm")
    r.add_argument("--dry-run", action="store_true")
    r.add_argument("--skip-rules", action="store_true")  
    r.add_argument("--allow-rules", action="store_true")  
    
    o = sub.add_parser("optimize")
    o.add_argument("file")
    o.add_argument("--target",choices=["local", "aks"], help="Deploy to Systems")
    o.add_argument("--context",help="Set Context to deploy")
    o.add_argument("--verbose", help="Detailed Reporting", action="store_true")
    o.add_argument("--dry-run", action="store_true")  
    o.add_argument("--skip-rules",action="store_true")  
    o.add_argument("--allow-rules",action="store_true")  
    o.add_argument("--apply-aks-defaults",action="store_true")
    o.add_argument("--output",choices=["json","yaml"])

    e = sub.add_parser("explain")
    e.add_argument("file")
    e.add_argument("--verbose", help="Detailed Reporting",action="store_true")
    e.add_argument("--output",choices=["json","yaml"])

    args = p.parse_args()


    #print("args response is:", args)

    #cli based
    if args.output not in ["json","yaml"]:
        setup_logging(verbose=args.verbose)
        render_banner()
    logger = logging.getLogger(__name__)


    if args.cmd == "deploy":
        irs = []
        # if args.helm:
        #     irs.append(HelmIR(args.helm))
        # else:
        if not all([args.name, args.cpu, args.memory, args.image]):
            raise SystemExit("Missing required flags: --name --cpu --memory --image or use --helm")
        irs.append(DeploymentIR(name=args.name, image=args.image, cpu=args.cpu, memory=args.memory))
        
        opts = build_opts(args)
       
        ctx = RunContext(irs=irs, opts= opts)
        logger.info(f"Enter main module: {ctx.artifacts}") 
        bus = ServiceBus(seq_before=[
                        #HTTPModuleClient("floyd", "http:/io.com"), 
                        DeploymentEngine(), 
                        OptimizerEngine()],
                        parallel_checks = [ValidatorEngine() ,SecurityEngine()],
                        seq_after = [RendererEngine(),CloudEngine()]
                        )
        logger.info("Bus Dict: {bus.__dict__}") 
        bus.run(ctx)
        logger.info(f"after run context is: {ctx.__dict__}")

        render_report(ctx.report, args.verbose)    
    # DSL based
    
    elif args.cmd == "run":
        irs = load_user_irs(args.file)
        logger.info(f"dsl irs are:{irs}")

        opts = build_opts(args)
       
        ctx = RunContext(irs=irs, opts= opts)
        logger.info(f"Artifacts: {ctx.artifacts}") 
        bus = ServiceBus(seq_before=[
                        #HTTPModuleClient("floyd", "http:/io.com"), 
                        DeploymentEngine(), 
                        OptimizerEngine()],
                        parallel_checks = [
                        ValidatorEngine() 
                        ],
                        seq_after = [RendererEngine(),CloudEngine()]
                        )
        logger.info(f"Bus DIct: {bus.__dict__}") 
        bus.run(ctx)
        logger.info(f"After run context is: {ctx.__dict__}")

        render_report(ctx.report, args.verbose)

    # yaml based
    elif args.cmd == "explain":
        user_path = args.file 
        irs = load_yaml_irs(user_path, logger)
        opts = {}
        if args.output not in ["json", "yaml"]:
            print("🔍 Analyzing:",os.path.basename(user_path), "\n")
        #logger.info("Analyzing kubernetes resources ...") 
        
        # security rules       
        # opts = {
        #     "allow_rules": ["run-as-root", "privileged-container"],     
        #     "skip_rules": ["latest-tag"]
        # }
        
        ctx = RunContext(irs=irs, opts=opts)
        bus = ServiceBus(seq_before=[
                            ],
                        parallel_checks = [
                            ValidatorEngine() ,SecurityEngine()],
                        seq_after = [RendererEngine()]
                        )
              
        bus.run(ctx)
        if args.output == "json":
            renderer = JSONRenderer(ctx.report)
        elif args.output == "yaml":
            renderer =  YamlRenderer(ctx.manifests, verbose=args.verbose)                       
        else:
            renderer = ReportsRenderer(ctx.report, verbose=args.verbose) 
        
    

        renderer.render()


    elif args.cmd == "optimize":
        
        user_path = args.file 

        irs = load_yaml_irs(user_path, logger)

        opts = build_opts(args)       
        if args.output not in ["json","yaml"]:
            print("🔍 Analyzing:",os.path.basename(user_path),"\n")
        # explicit default cloud settings
        
        logger.info(f"args, {args}")

        ctx = RunContext(irs=irs, opts=opts)
        bus = ServiceBus(seq_before=[
                        #HTTPModuleClient("floyd", "http:/io.com"), 
                        OptimizerEngine()],
                        parallel_checks = 
                        [ValidatorEngine() ,SecurityEngine()],
                        seq_after = [RendererEngine(), CloudEngine()]
                        )
        bus.run(ctx)
        if args.output == "json":
            renderer = JSONRenderer(ctx.report)
        elif args.output == "yaml":
            renderer =  YamlRenderer(ctx.manifests, verbose=args.verbose)                       
        else:
            renderer = ReportsRenderer(ctx.report, verbose=args.verbose) 
        
        renderer.render()
        
if __name__ == "__main__":
    main()
