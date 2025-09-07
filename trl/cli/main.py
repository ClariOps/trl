import argparse

from trl.core.context import RunContext
from trl.app_pipelines.loader import load_user_irs

from trl.modules.deployment.parser import DeploymentIR, HelmIR
from trl.modules.deployment.engine import DeploymentEngine
from trl.modules.optimizer.engine import OptimizerEngine
from trl.modules.security.engine import SecurityEngine
from trl.modules.cloud.engine import CloudEngine
from trl.modules.validator.engine import ValidatorEngine
from trl.adapters.remote import HTTPModuleClient
from trl.core.bus import ServiceBus

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
    r.add_argument("--helm")


    args = p.parse_args()
    print("args response is:", args)

    if args.cmd == "deploy":
        irs = []
        if args.helm:
            irs.append(HelmIR(args.helm))
        else:
            if not all([args.name, args.cpu, args.memory, args.image]):
                raise SystemExit("Missing required flags: --name --cpu --memory --image or use --helm")
            irs.append(DeploymentIR(name=args.name, image=args.image, cpu=args.cpu, memory=args.memory))
        #print("irs dict: ", irs[0].__repr__)    
        ctx = RunContext(irs=irs, opts= {"helm": args.helm, "out_dir":"dist"})
        print("Artifacts:", ctx.artifacts) 
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

        if ctx.report.errors or ctx.report.warnings:
            print("Report:", {"errors": ctx.report.errors, "warnings": ctx.report.warnings})
    elif args.cmd == "run":
        irs = load_user_irs(args.file)
        print("dsl irs are:", irs )

        ctx = RunContext(irs=irs, opts= {"helm": args.helm, "out_dir":"dist"})
        print("\nArtifacts:", ctx.artifacts) 
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
    

if __name__ == "__main__":
    main()
