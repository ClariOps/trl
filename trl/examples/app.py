from trl.dsl import deployment, optimize



api = deployment(
    "api", cpu="120mi", memory="96Mi", image="myorg/api:1.0" , replicas=2, ports=[5000]
)
optimize(api)