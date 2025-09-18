
from pykube import HTTPClient, KubeConfig, Deployment
from trl.core.base import Module
from trl.core.context import RunContext
import logging
logger = logging.getLogger(__name__)
  
class CloudEngine(Module):
    name = "cloud-engine"
    def process(self, ctx: RunContext) -> None:
        cloud = ctx.opts.get("cloud")
        if not cloud:
            print("inside cloud exit1")
            return
        
        logger.info(f"Deploying to AKS...")
        try:
            kube_client = self._get_aks_client(ctx)
            
            self._deploy_manifest(kube_client, ctx.manifests)
            
            logger.info("Successfully deployed all manifests to AKS")
        
        except Exception as e:
            error_msg = f"Failed to deploy to AKS: {e}"
            logger.error(error_msg)
            ctx.report.errors.append(error_msg)

                

    def _get_aks_client(self, ctx: RunContext):
        config = KubeConfig.from_file()
        target_context = ctx.opts.get("context")

        if not target_context:
            available_contexts = list(config.contexts.keys())
            raise Exception(f"Context '{target_context}' not found. Available contexts: {available_contexts}")
        config.set_current_context(target_context)
        logger.info(f"Using context: {target_context}")
            
        return HTTPClient(config)       
        
    def _deploy_manifest(self, kube_client, manifest):
        kind = manifest.get("kind")
        name = manifest["metadata"]["name"]
        if kind == "Deployment":
            # for time being cloud value can be set here 
                # will replace by independent engine for cloud optimization         
            
            #manifest["spec"]["template"]["spec"].setdefault("nodeSelector", {})["kubernetes.io/arch"] = "arm64"
            
            #         
            deployment = Deployment(kube_client, manifest)
            deployment.create()
            logger.info(f"Deployed Deployment: {name}")
