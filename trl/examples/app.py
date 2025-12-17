from trl.dsl import deployment, pvc



#api = deployment(
#    "api", cpu="120mi", memory="96Mi", image="myorg/api:1.0" , replicas=2, ports=[5000]
#)

pvc(
    name="mongo-dsl-pvc",
    storage="5Gi",
    storage_class="standard"
)
