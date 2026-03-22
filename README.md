
# truckoverload V1
Infrastructure automation.

---

### Usage Examples

#### Domain Specific Language (DSL)
Run automation scripts defined in Python:
> `trl run ./trl/examples/app.py --target=local --verbose=true`

#### Optimizer
Run the optimization engine for your application:
> `trl optimize ./trl/examples/app.yaml --target=local --verbose=true`

#### Command Line Interface (CLI)
Deploy applications directly via command line arguments:
> `trl deploy --name="nginx-app" --cpu="120m" --memory="64Mi" --image="nginx:latest" --target=local --verbose=True --dry-run=True`


#### For Allow Rules/ Skip Rules
Run Automation scripts via command line arguments:
> `trl optimize ./trl/examples/app.yaml --target=local  --skip-rules cpu-minimum --allow-rule cpu-default`



---

**Powered by [KinetixCore Labs ]**