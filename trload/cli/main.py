import argparse, yaml, logging, glob, os
import sys
from importlib.metadata import version, PackageNotFoundError

from trload.core.context import RunContext
from trload.app_pipelines.loader import load_user_irs

from trload.core.ir import (DeploymentIR, ServiceIR, HelmIR, IngressIR, ConfigMapIR, SecretIR, PVCIR)
from trload.modules.manifest_preparation.engine import ManifestPreparationEngine
from trload.modules.optimizer.engine import OptimizerEngine
from trload.modules.security.engine import SecurityEngine
from trload.modules.cloud.engine import CloudEngine
from trload.modules.validator.engine import ValidatorEngine
from trload.modules.renderer.engine import RendererEngine
from trload.adapters.remote import HTTPModuleClient
from trload.core.bus import ServiceBus
from trload.core.reporting.reportRenderer import ReportsRenderer
from trload.core.reporting.jsonRenderer import JSONRenderer
from trload.core.reporting.yamlRenderer import YamlRenderer

from trload.core.reporting.deprecatedRenderer import render_report
from trload.core.logconfig.config import setup_logging
from trload.cli.helper import IR_MAPPING, load_workflow, load_yaml_irs, build_opts, render_banner, valid_file




def main():
    p = argparse.ArgumentParser("trload")
    sub = p.add_subparsers(dest="cmd", required=True)
    
    try:
        __version__ = version("clariops-trload")
    except PackageNotFoundError:
        __version__ = "unknown"

    p.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    
    # on hold currently
    d = sub.add_parser("generate")
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
    d.add_argument("--output",choices=["json","yaml"])
    
    # on hold currently
    r = sub.add_parser("run")
    r.add_argument("file",type=valid_file)
    r.add_argument("--target",choices=["local", "aks"], help="Deploy to Systems")
    r.add_argument("--verbose", help="Detailed Reporting")
    r.add_argument("--helm")
    r.add_argument("--dry-run", action="store_true")
    r.add_argument("--skip-rules", action="store_true")  
    r.add_argument("--allow-rules", action="store_true")  
    r.add_argument("--output",choices=["json","yaml"])    
    
    o = sub.add_parser("optimize")
    o.add_argument("file", type=valid_file)
    o.add_argument("--target",choices=["local", "aks"], help="Deploy to Systems")
    o.add_argument("--context",help="Set Context to deploy")
    o.add_argument("--verbose", help="Detailed Reporting", action="store_true")
    o.add_argument("--dry-run", action="store_true")  
    o.add_argument("--skip-rules",action="store_true")  
    o.add_argument("--allow-rules",action="store_true")  
    o.add_argument("--apply-aks-defaults",action="store_true")
    o.add_argument("--output",choices=["json","yaml"])

    e = sub.add_parser("explain")
    e.add_argument("file", type=valid_file)
    e.add_argument("--verbose", help="Detailed Reporting",action="store_true")
    e.add_argument("--output",choices=["json","yaml"])

    f = sub.add_parser("remote")
    f.add_argument("file", type=valid_file)
    f.add_argument("--exec", required=True, dest="workflow", type=valid_file, help="Workflow definition to execute")
    f.add_argument("--target",choices=["local", "aks"], help="Deploy to Systems")
    f.add_argument("--context",help="Set Context to deploy")
    f.add_argument("--verbose", help="Detailed Reporting", action="store_true")
    f.add_argument("--dry-run", action="store_true")  
    f.add_argument("--skip-rules",action="store_true")  
    f.add_argument("--allow-rules",action="store_true")  
    f.add_argument("--output",choices=["json","yaml"])
    

    args = p.parse_args()


    #print("args response is:", args)

    #cli based
    if args.output not in ["json","yaml"]:
        setup_logging(verbose=args.verbose)
        render_banner()
    logger = logging.getLogger(__name__)

    # on hold currently
    if args.cmd == "generate":
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
                        ManifestPreparationEngine(), 
                        OptimizerEngine()],
                        parallel_checks = [ValidatorEngine() ,SecurityEngine()],
                        seq_after = [RendererEngine()] # cloudEngine() shows bugs due to ON HOLD & legacy report modules 
                        )
        logger.info("Bus Dict: {bus.__dict__}") 
        bus.run(ctx)
        logger.info(f"after run context is: {ctx.__dict__}")
        #legacy report modules 
        render_report(ctx.report, args.verbose)    
    
    # DSL based
    # on hold currently
    elif args.cmd == "run":
        irs = load_user_irs(args.file)
        logger.info(f"dsl irs are:{irs}")

        opts = build_opts(args)
       
        ctx = RunContext(irs=irs, opts= opts)
        logger.info(f"Artifacts: {ctx.artifacts}") 
        bus = ServiceBus(seq_before=[
                        #HTTPModuleClient("floyd", "http:/io.com"), 
                        ManifestPreparationEngine(), 
                        OptimizerEngine()],
                        parallel_checks = [
                        ValidatorEngine() 
                        ],
                        seq_after = [RendererEngine()] # cloudEngine() shows bugs due to ON HOLD & legacy report modules 
                        )
        logger.info(f"Bus DIct: {bus.__dict__}") 
        bus.run(ctx)
        logger.info(f"After run context is: {ctx.__dict__}")
        #legacy report module
        render_report(ctx.report, args.verbose)

    # analysis CLI
    elif args.cmd == "explain":
        user_path = args.file 
        if not args.file:
            print("file not found")
            sys.exit(1)
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
            output = renderer.render()
            print(output)
        elif args.output == "yaml":
            renderer =  YamlRenderer(ctx.manifests)
            output = renderer.render()
            print(output, end="")
            if args.verbose:
                report = ReportsRenderer(ctx.report, verbose=True)
                print(report.render(), file=sys.stderr)    

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
            output = renderer.render()
            print(output)
        elif args.output == "yaml":
            renderer =  YamlRenderer(ctx.manifests)
            output = renderer.render()
            print(output, end="")
            if args.verbose:
                report = ReportsRenderer(ctx.report, verbose=True)
                print(report.render(), file=sys.stderr)    

        else:
            renderer = ReportsRenderer(ctx.report, verbose=args.verbose) 
        
        renderer.render()

    elif args.cmd == "remote":

        user_path = args.file
        
        irs = load_yaml_irs(user_path, logger)
        
        opts = build_opts(args)
        
        if args.output not in ["json", "yaml"]:
            print("🔍 Remote workflow:", os.path.basename(user_path),"\n")
        
        ctx = RunContext(irs=irs, opts=opts)
        
        workflow = load_workflow(args.workflow)
        
        bus = ServiceBus(
            **workflow.workflow
        )
        
        bus.run(ctx)
        
        if args.output == "json":
            renderer = JSONRenderer(ctx.report)
            print(renderer.render())
        
        elif args.output == "yaml":
            renderer = YamlRenderer(ctx.manifests)
            print(renderer.render(),end="",)

        else:
            renderer = ReportsRenderer(ctx.report, verbose=args.verbose)

        renderer.render() 

if __name__ == "__main__":
    main()
