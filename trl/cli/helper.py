from trl.core.ir import (DeploymentIR, ServiceIR, HelmIR, IngressIR, ConfigMapIR, SecretIR, PVCIR)

IR_MAPPING = {
    "Deployment": DeploymentIR,
    "Service": ServiceIR,
    "Ingress": IngressIR,
    "ConfigMap": ConfigMapIR,
    "Secret": SecretIR,
    "PersistentVolumeClaim": PVCIR,
}


def load_yaml_irs(user_path, logger):
    import glob, os, yaml

    irs = []

    # directory vs file
    if os.path.isdir(user_path):
        search_pattern = os.path.join(user_path, "*.y*ml")
    else:
        search_pattern = user_path

    for filepath in glob.glob(search_pattern):
        with open(filepath, "r") as f:
            documents = yaml.safe_load_all(f)

            for data in documents:
                if not data or "kind" not in data:
                    continue

                kind = data.get("kind")
                ir_class = IR_MAPPING.get(kind)

                if ir_class:
                    irs.append(ir_class(manifest=data))
                else:
                    logger.warning(
                        f"No IR class defined for kind '{kind}' in {filepath}"
                    )

    return irs

def build_opts(args):
    opts = {}

    if args.target:
        opts["target"] = args.target

    if getattr(args, "context", None):
        opts["context"] = args.context

    if args.dry_run:
        opts["dry_run"] = True

    if args.skip_rules:
        opts["skip_rules"] = args.skip_rules

    if args.allow_rules:
        opts["allow_rules"] = args.allow_rules

    if getattr(args, "apply_aks_defaults", None):
        opts["apply_aks_defaults"] = True

    return opts


def render_banner():
    banner = r"""
████████╗██████╗ ██╗     
╚══██╔══╝██╔══██╗██║     
   ██║   ██████╔╝██║     
   ██║   ██╔══██╗██║     
   ██║   ██║  ██║███████╗
   ╚═╝   ╚═╝  ╚═╝╚══════╝

🚚 TRL — Pre-Deployment Intelligence System
────────────────────────────────────────────
Analyze • Optimize • Validate • Secure

"Making Kubernetes predictable before it runs"

"""
    print(banner)