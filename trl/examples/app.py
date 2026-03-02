from trl.dsl import deployment, pvc



api = deployment(
   "nginxdsl-dep", cpu="120m", memory="9Mi", image="nginx:latest" , replicas=2, ports=[5000]
)

# pvc(
#     name="mongo-dsl-pvc",
#     storage="5Gi",
#     storage_class="standard"
# )
