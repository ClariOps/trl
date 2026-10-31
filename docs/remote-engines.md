
# Remote Engine Composition

TRL includes an experimental remote engine composition example.

It demonstrates how independent engines can run in separate processes and be invoked through HTTP as part of a user-defined workflow.

The purpose of this example is to demonstrate **engine independence, remote invocation, and workflow composition**.

It is not a production-ready distributed execution platform.

---

## 1. What This Demonstrates

In a traditional local workflow, engines execute within the same TRL process.

The remote example demonstrates another arrangement:

```text
                 TRL Workflow
                      |
                      v
              HTTPModuleClient
                      |
                      v
              Remote Optimizer
                      |
                      v
              HTTPModuleClient
                      |
                      v
              Remote Validator
                      |
                      v
              HTTPModuleClient
                      |
                      v
              Remote Security
                      |
                      v
               Local Renderer
                      |
                      v
                    Output
```

Each remote engine runs as a separate Python process.

The workflow invokes the engines through their HTTP endpoints.

The engine's responsibility remains independent of its invocation mechanism.

---

## 2. Example Structure

The repository contains:

```text
examples/
└── remote/
    ├── optimizer_server.py
    ├── validator_server.py
    ├── security_server.py
    ├── registry.json
    └── workflow.py
```

The implementation is located in:

```text
trl/
└── adapters/
    └── remote/
        ├── client.py
        └── server.py
```

### Component responsibilities

| File | Responsibility |
|---|---|
| `optimizer_server.py` | Starts the remote Optimizer |
| `validator_server.py` | Starts the remote Validator |
| `security_server.py` | Starts the remote Security engine |
| `registry.json` | Stores the example engine endpoint mappings |
| `workflow.py` | Defines the workflow composition |
| `client.py` | Implements HTTP-based engine invocation |
| `server.py` | Hosts an engine and handles HTTP requests |

---

## 3. Requirements

Clone the repository and install its dependencies:

```bash
git clone https://github.com/ClariOps/trl.git
cd trl
pip install -r requirements.txt
```

Run the following commands from the repository root.

The example workflow loads its registry through a relative file path:

```text
examples/remote/registry.json
```

---

## 4. Start the Remote Engines

Start each engine server in a separate terminal.

### Terminal 1 — Optimizer

```bash
python examples/remote/optimizer_server.py
```

The server listens on:

```text
http://127.0.0.1:9001/process
```

### Terminal 2 — Validator

```bash
python examples/remote/validator_server.py
```

The server listens on:

```text
http://127.0.0.1:9002/process
```

### Terminal 3 — Security

```bash
python examples/remote/security_server.py
```

The server listens on:

```text
http://127.0.0.1:9003/process
```

Each script starts the corresponding engine using the shared `serve()` implementation.

The server receives HTTP POST requests at `/process`.

Keep these processes running while executing the workflow.

---

## 5. Registry Configuration

The example uses:

```text
examples/remote/registry.json
```

Its current configuration is:

```json
{
    "X092@jjj": {
        "name": "optimizer",
        "endpoint": "http://127.0.0.1:9001/process"
    },
    "Y481@abc": {
        "name": "validator",
        "endpoint": "http://127.0.0.1:9002/process"
    },
    "Z481@abc": {
        "name": "security",
        "endpoint": "http://127.0.0.1:9003/process"
    }
}
```

The workflow reads this file and uses the configured endpoints to construct its HTTP clients.

**Important:** This is a static JSON registry used by the example. It is not a dynamic service-discovery or automatic engine-registration system.

---

## 6. Workflow Definition

The workflow is defined in:

```text
examples/remote/workflow.py
```

Its composition is:

```python
workflow = {
    "seq_before": [
        HTTPModuleClient(...)
    ],

    "parallel_checks": [],

    "seq_after": [
        HTTPModuleClient(...),
        HTTPModuleClient(...),
        RendererEngine()
    ],
}
```

The three remote clients represent:

1. Optimizer
2. Validator
3. Security

The Renderer runs locally.

The workflow therefore combines remote and local engine instances.

### Execution order

```text
Input Manifest
      |
      v
   Load IR
      |
      v
  seq_before
      |
      v
Remote Optimizer
      |
      v
parallel_checks
      |
      v
Empty in current example
      |
      v
   seq_after
      |
      v
Remote Validator
      |
      v
Remote Security
      |
      v
Local Renderer
      |
      v
    Output
```

The `parallel_checks` list is currently empty.

Therefore, this example demonstrates sequential remote composition, not parallel remote execution.

---

## 7. Execute the Workflow

Open another terminal from the repository root.

Run:

```bash
trl remote ./examples/demo/bad.yaml \
  --exec ./examples/remote/workflow.py
```

The command:

1. Loads the Kubernetes manifest.
2. Converts supported resources into IR.
3. Loads the Python workflow definition.
4. Creates the ServiceBus using the workflow configuration.
5. Executes the workflow.
6. Renders the selected output.

### JSON report

```bash
trl remote ./examples/demo/bad.yaml \
  --exec ./examples/remote/workflow.py \
  --output=json
```

### YAML manifest output

```bash
trl remote ./examples/demo/bad.yaml \
  --exec ./examples/remote/workflow.py \
  --output=yaml
```

### Verbose reporting

```bash
trl remote ./examples/demo/bad.yaml \
  --exec ./examples/remote/workflow.py \
  --verbose
```

---

## 8. How Remote Invocation Works

The remote communication mechanism is implemented by two components.

### HTTPModuleClient

Location:

```text
trl/adapters/remote/client.py
```

The client:

1. Receives the current RunContext.
2. Serializes the IR resources into JSON-compatible data.
3. Serializes the options and report.
4. Sends an HTTP POST request to the configured endpoint.
5. Checks the HTTP response.
6. Deserializes the returned IR and report.
7. Updates the current context.

The request contains:

```json
{
    "irs": [],
    "opts": {},
    "report": {}
}
```

The IR entries contain the resource kind and its Kubernetes manifest.

### Remote server

Location:

```text
trl/adapters/remote/server.py
```

The server:

1. Receives the HTTP POST request.
2. Reads the JSON payload.
3. Deserializes the supported IR resources.
4. Reconstructs the RunContext.
5. Invokes the configured engine.
6. Serializes the resulting IR and report.
7. Returns the result as JSON.

The engine is invoked through its existing processing interface:

```python
engine.process(ctx)
```

The response contains:

```json
{
    "irs": [],
    "report": {}
}
```

The client then uses the returned state for subsequent workflow stages.

---

## 9. Supported IR Resources

The current remote serialization mapping supports:

| Kubernetes Resource | IR |
|---|---|
| Deployment | `DeploymentIR` |
| Service | `ServiceIR` |
| Ingress | `IngressIR` |
| ConfigMap | `ConfigMapIR` |
| Secret | `SecretIR` |
| PersistentVolumeClaim | `PVCIR` |

A new resource type requires corresponding serialization and deserialization support before it can be passed through the current remote adapter.

---

## 10. Current Implementation Boundaries

The example demonstrates:

- Separate engine processes
- HTTP-based engine invocation
- IR serialization and deserialization
- Report serialization and deserialization
- Sequential composition of remote engines
- Composition of remote and local engine instances
- Workflow execution through `trl remote`

The example does not currently demonstrate:

- Dynamic engine discovery
- Automatic engine registration
- Engine upload or installation
- Distributed sequence approval
- Authentication or authorization
- TLS configuration
- Production-grade service lifecycle management
- Parallel remote engine execution
- Cloud deployment through this example

The registry is static JSON configuration, and the endpoints use local HTTP addresses.

The HTTP server uses Python's standard-library `HTTPServer`.

The client uses a 30-second HTTP request timeout and raises an error for unsuccessful HTTP responses.

This example should therefore be treated as an architectural and implementation demonstration, not as a production security or availability model.

---

## 11. Troubleshooting

### Connection refused

Example:

```text
ConnectionError
```

Check that the corresponding engine server is running and that its configured port matches the registry.

### Workflow cannot find registry.json

Run the command from the repository root.

The workflow currently opens:

```text
examples/remote/registry.json
```

using a relative path.

### Unsupported resource type

Check the IR mapping in:

```text
trl/adapters/remote/client.py
```

The resource must have matching serialization and deserialization support.

### HTTP 500 response

Check the terminal running the corresponding remote server.

The server prints the exception traceback when engine processing fails.

---

## 12. Architectural Meaning

The important distinction is:

```text
ENGINE RESPONSIBILITY
        |
        v
 Remains independent
        |
        v
INVOCATION MECHANISM
        |
        +-- Local engine
        |
        +-- Remote HTTP client
        |
        v
WORKFLOW COMPOSITION
        |
        v
Execution order
```

Remote invocation changes where an engine runs and how it is called.

It does not change which responsibility the engine owns.

The workflow determines the composition. The engine remains responsible for its own processing logic.

This is the current foundation demonstrated by TRL's remote engine example.
