from trl.dsl import deployment



api = deployment(
    "api", image="myorg/api:1.0", cpu="120mi", memory="96Mi", replicas=2, ports=[4000]
)
