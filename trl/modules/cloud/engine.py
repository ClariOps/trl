
import sys
from pykube import HTTPClient, KubeConfig, Deployment, Service, Ingress, ConfigMap, Secret, PersistentVolumeClaim
from trl.core.base import Module
from trl.core.context import RunContext
import logging
logger = logging.getLogger(__name__)
  
class CloudEngine(Module):
    name = "cloud-engine"
    def process(self, ctx: RunContext) -> None:

        if ctx.opts.get("dry_run"):
            logger.info("Dry-run enabled, skipping deployment")
            return
        
        if len(ctx.report.errors):
            logger.warning("Errors Found, skipping deployment")
            return
        target = ctx.opts.get("target")
        if not target:
            ctx.report.add_warning("No deployment target, exit 1")        
            logger.warning("No deployment target, exit 1")
            return

        logger.info(f"Deploying to AKS...")
        try:
            kube_client = self._get_aks_client(ctx, target)
            for manifest in ctx.manifests:
                self._deploy_manifest(kube_client, manifest, ctx.opts, target)
            
            logger.info("Successfully deployed all manifests to AKS")
        
        except Exception as e:
            error_msg = f"Failed to deploy to AKS: {e}"
            logger.error(error_msg)
            ctx.report.add_error(error_msg)

                

    def _get_aks_client(self, ctx: RunContext, target: str):
        config = KubeConfig.from_file()
        if target == "local":
            if "minikube" in config.contexts:
                config.set_current_context("minikube")
                logger.info("Using hardcoded minikube context for local deployment")
            else:
                available_contexts = list(config.contexts.keys())
                raise Exception(f"minikube context not found. Available contexts: {available_contexts}")
        
        # Cloud targets use explicit context (required)
        elif target in ["aks", "gke", "eks"]:
            target_context = ctx.opts.get("context")
            if not target_context:
                raise Exception(f"Context is required for {target.upper()} deployment. Use --context <context-name>")
            
            if target_context not in config.contexts:
                available_contexts = list(config.contexts.keys())
                raise Exception(f"Context '{target_context}' not found. Available contexts: {available_contexts}")
            
            config.set_current_context(target_context)
            logger.info(f"Using {target.upper()} context: {target_context}")
        

        return HTTPClient(config)       
        
    def _deploy_manifest(self, kube_client, manifest, opts, target: str):
        kind = manifest.get("kind")
        name = manifest["metadata"]["name"]
        
        if kind == "Deployment":
            if target == "aks" and opts.get("apply_aks_defaults"):
            # for time being cloud value can be set here 
                # will replace by independent engine for cloud optimization         
                spec = manifest["spec"]["template"]["spec"]
                spec.setdefault("nodeSelector", {})
                spec["nodeSelector"]["kubernetes.io/arch"] = "amd64"
                logger.warning(
                    f"[cloud-default] Applied AKS nodeSelector to Deployment: {name}"
                )                #    
                     
            deployment = Deployment(kube_client, manifest)
            deployment.create()
            logger.info(f"Deployed Deployment: {name}")
        
        elif kind == "Service":
            # Add Service deployment logic
            service = Service(kube_client, manifest)
            service.create()
            logger.info(f"Deployed Service: {name}")

        elif kind =="Ingress":
            ingress = Ingress(kube_client, manifest)
            ingress.create()
            logger.info(f"Deployed Ingress: {name}")

        elif kind =="ConfigMap":
            configmap = ConfigMap(kube_client, manifest)
            configmap.create()
            logger.info(f"Deployed ConfigMap: {name}")

        elif kind =="Secret":
            secret = Secret(kube_client, manifest)
            secret.create()
            logger.info(f"Deployed Secret: {name}")
        
        elif kind == "PersistentVolumeClaim":
            pvc = PersistentVolumeClaim(kube_client, manifest)
            pvc.create()
            logger.info(f"Deployed persistent volume: {name}")
            