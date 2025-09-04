import argparse
from trl.modules.deployment.parser import DeploymentIR, HelmIR
from trl.core.context import RunContext
def main():
    p = argparse.ArgumentParser("trl")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("deploy")
    d.add_argument("--name")
    d.add_argument("--cpu")
    d.add_argument("--memory")
    d.add_argument("--image")
    d.add_argument("--helm")

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
if __name__ == "__main__":
    main()
