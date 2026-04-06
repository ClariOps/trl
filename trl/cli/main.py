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

    d.add_argument("--target",choices=["local", "aks"], help="Deploy to Systems")
    d.add_argument("--verbose", help="Detailed Reporting")
    d.add_argument("--dry-run")
    d.add_argument("--skip-rules")  
    d.add_argument("--allow-rules")  

    r = sub.add_parser("run")
    r.add_argument("file")
    r.add_argument("--target",choices=["local", "aks"], help="Deploy to Systems")
    r.add_argument("--verbose", help="Detailed Reporting")
    r.add_argument("--helm")
    r.add_argument("--dry-run")
    r.add_argument("--skip-rules")  
    r.add_argument("--allow-rules")  


    o = sub.add_parser("optimize")
    o.add_argument("file")
    o.add_argument("--target",choices=["local", "aks"], help="Deploy to Systems")
    o.add_argument("--context",help="Set Context to deploy")
    o.add_argument("--verbose", help="Detailed Reporting")
    o.add_argument("--dry-run")  
    o.add_argument("--skip-rules")  
    o.add_argument("--allow-rules")  


    e = sub.add_parser("explain")
    e.add_argument("file")
    e.add_argument("--verbose", help="Detailed Reporting")

    args = p.parse_args()


    #print("args response is:", args)

    #cli based
    setup_logging(verbose=args.verbose)
    logger = logging.getLogger(__name__)


    if args.cmd == "deploy":
        irs = []
        # if args.helm:
        #     irs.append(HelmIR(args.helm))
        # else:
        if not all([args.name, args.cpu, args.memory, args.image]):
            raise SystemExit("Missing required flags: --name --cpu --memory --image or use --helm")
        irs.append(DeploymentIR(name=args.name, image=args.image, cpu=args.cpu, memory=args.memory))
        
        opts = {}
        if args.target:
            opts["target"] = args.target

        if args.target != "local" and args.context:
            opts["context"] = args.context    
        
        if args.dry_run:
            opts["dry_run"] = args.dry_run

        if args.skip_rules:
            opts["skip_rules"]= args.skip_rules
            logger.info(f"Skip: rule is {opts} ")

    
        if args.allow_rules:
            opts["allow_rules"]= args.allow_rules
            logger.info(f"Allowed Only: rule is {opts} ")

       
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

        opts = {}
        if args.target:
            opts["target"] = args.target

        if args.target != "local" and args.context:
            opts["context"] = args.context            
        
        if args.dry_run:
            opts["dry_run"] = args.dry_run

        if args.skip_rules:
            opts["skip_rules"]= args.skip_rules
            logger.info(f"Skip: rule is {opts} ")

    
        if args.allow_rules:
            opts["allow_rules"]= args.allow_rules
            logger.info(f"Allowed Only: rule is {opts} ")

       
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
        irs = []
        user_path = args.file 

        # 2. Check if the user gave a directory or a specific file
        if os.path.isdir(user_path):
        # If it's a folder, look for all .yaml and .yml files inside
            search_pattern = os.path.join(user_path, "*.y*ml")
        else:
        # If it's a specific file, just use that
            search_pattern = user_path

        IR_MAPPING = {
            "Deployment": DeploymentIR,
            "Service": ServiceIR,
            "Ingress": IngressIR,
            "ConfigMap": ConfigMapIR,
            "Secret": SecretIR,
            "PersistentVolumeClaim": PVCIR,
        }

        for filepath in glob.glob(search_pattern):
            with open(filepath, "r") as f:
            # 3. Use safe_load_all to handle multi-document YAML files
                documents = yaml.safe_load_all(f)
            
                for data in documents:
                    if not data or "kind" not in data:
                        continue
                
                # 4. Dispatch to the correct IR class based on 'kind'
                    kind = data.get("kind")
                    ir_class = IR_MAPPING.get(kind)
                
                    if ir_class:
                        irs.append(ir_class(manifest=data))
                    else:
                        logger.warning(f"Warning: No IR class defined for kind '{kind}' in {filepath}")

        if args.verbose:
            logger.setLevel("DEBUG")
        else:
            logger.setLevel("INFO")

        logger.info("Analyzing kubernetes resources ...") 
        logger.debug(f"yaml data: {data}")

        # security rules       
        # opts = {
        #     "allow_rules": ["run-as-root", "privileged-container"],     
        #     "skip_rules": ["latest-tag"]
        # }
        opts = {}

        ctx = RunContext(irs=irs, opts=opts)
        bus = ServiceBus(seq_before=[
                            ],
                        parallel_checks = [
                            ValidatorEngine() ,SecurityEngine()],
                        seq_after = [RendererEngine()]
                        )
              
        bus.run(ctx)



        renderer = ReportsRenderer(ctx.report, args.verbose) 
        renderer.render()


    elif args.cmd == "optimize":
        irs = []
        user_path = args.file 

        # 2. Check if the user gave a directory or a specific file
        if os.path.isdir(user_path):
        # If it's a folder, look for all .yaml and .yml files inside
            search_pattern = os.path.join(user_path, "*.y*ml")
        else:
        # If it's a specific file, just use that
            search_pattern = user_path

        IR_MAPPING = {
            "Deployment": DeploymentIR,
            "Service": ServiceIR,
            "Ingress": IngressIR,
            "ConfigMap": ConfigMapIR,
            "Secret": SecretIR,
            "PersistentVolumeClaim": PVCIR,
        }

        for filepath in glob.glob(search_pattern):
            with open(filepath, "r") as f:
            # 3. Use safe_load_all to handle multi-document YAML files
                documents = yaml.safe_load_all(f)
            
                for data in documents:
                    if not data or "kind" not in data:
                        continue
                
                # 4. Dispatch to the correct IR class based on 'kind'
                    kind = data.get("kind")
                    ir_class = IR_MAPPING.get(kind)
                
                    if ir_class:
                        irs.append(ir_class(manifest=data))
                    else:
                        logger.warning(f"Warning: No IR class defined for kind '{kind}' in {filepath}")

        
        #logger.info(f"yaml data: {data}")

        opts = {}
        if args.target:
            opts["target"] = args.target

        if args.target != "local" and args.context:
            opts["context"] = args.context  


        logger.info(f"check arg target: {args.target}")

        if args.dry_run:
            opts["dry_run"]= args.dry_run
        if args.skip_rules:
            opts["skip_rules"]= args.skip_rules
            logger.info(f"Skip: rule is {opts} ")

    
        if args.allow_rules:
            opts["allow_rules"]= args.allow_rules
            logger.info(f"Allowed Only: rule is {opts} ")
        
        if args.verbose:
            logger.setLevel("DEBUG")
        else:
            logger.setLevel("INFO")

   
        ctx = RunContext(irs=irs, opts=opts)
        bus = ServiceBus(seq_before=[
                        #HTTPModuleClient("floyd", "http:/io.com"), 
                        OptimizerEngine()],
                        parallel_checks = 
                        [ValidatorEngine() ,SecurityEngine()],
                        seq_after = [RendererEngine(), CloudEngine()]
                        )
        bus.run(ctx)
        renderer = ReportsRenderer(ctx.report, verbose=args.verbose) 
        renderer.render()
        
if __name__ == "__main__":
    main()
