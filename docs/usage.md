# TRL CLI Reference

> Pre-deployment analysis and optimization for Kubernetes manifests.

TRL provides a small CLI surface for analyzing, optimizing, and running Kubernetes workflows.

## Synopsis

```text
trl <command> [arguments] [options]
```

Run:

```bash

trl <command> --help
```

---

## Commands

| Command | Purpose |
|---|---|
| `explain` | Analyze a manifest without optimization |
| `optimize` | Optimize, validate, assess security, and produce the resulting state |
| `run` | Run a TRL workflow from a Python DSL input |
| `deploy` | CLI-based deployment input |

> `run` and `deploy` are currently on hold and may be reinitiated later.

---

# `trl explain`

Analyze a Kubernetes manifest without applying Optimizer mutations.

## Usage

```bash
trl explain <file> [options]
```

## Arguments

```text
file    Path to the input manifest
```

## Options

```text
--output {json,yaml}
--verbose
```

## Examples

```bash
# Human-readable report
trl explain ./examples/demo/bad.yaml

# JSON report
trl explain ./examples/demo/bad.yaml --output=json

# YAML manifest output
trl explain ./examples/demo/bad.yaml --output=yaml

# YAML output with a detailed report on stderr
trl explain ./examples/demo/bad.yaml --output=yaml --verbose
```

---

# `trl optimize`

Run the optimization workflow and then validate and assess the resulting state.

## Usage

```bash
trl optimize <file> [options]
```

## Arguments

```text
file    Path to the input manifest
```

## Options

```text
--target {local,aks}
--context CONTEXT
--verbose
--dry-run
--skip-rules
--allow-rules
--apply-aks-defaults
--output {json,yaml}
```

## Examples

```bash
# Optimize and report
trl optimize ./examples/demo/bad.yaml

# Optimize without applying the execution target
trl optimize ./examples/demo/bad.yaml --dry-run

# JSON report
trl optimize ./examples/demo/bad.yaml --output=json

# YAML manifest output
trl optimize ./examples/demo/bad.yaml --output=yaml

# YAML manifests plus detailed report
trl optimize ./examples/demo/bad.yaml --output=yaml --verbose
```

---

# `trl run`

Run a TRL workflow from a Python DSL input.

## Usage

```bash
trl run <file> [options]
```

## Arguments

```text
file    Path to the Python DSL application
```

## Options

```text
--target {local,aks}
--verbose
--helm HELM
--dry-run
--skip-rules
--allow-rules
```

## Example

The repository includes a Python DSL example at:

```text
examples/
└── dsl/
    └── app.py
```

The application defines Kubernetes resources with the TRL DSL:

```python
from trl.dsl import deployment, pvc


api = deployment(
   "nginxdsl-dep",
   cpu="80m",
   memory="9Mi",
   image="nginx:latest",
   replicas=2,
   ports=[5000]
)


pvc(
     name="mongo-dsl-pvc",
     storage="5Gi",
     storage_class="standard"
 )
```

Run it with:

```bash
trl run ./examples/dsl/app.py
```

`app.py` is the Python DSL input; TRL loads the user-defined IR and runs the selected workflow.

> `trl run` is currently on hold and may be reinitiated later.

---

# `trl deploy`

Create a deployment from CLI-provided deployment parameters.

## Usage

```bash
trl deploy [options]
```

## Options

```text
--name NAME
--cpu CPU
--memory MEMORY
--image IMAGE
--helm HELM
--target {local,aks}
--verbose
--dry-run
--skip-rules
--allow-rules
```

## Example

```bash
trl deploy   --name backend   --cpu 500m   --memory 512Mi   --image nginx:1.27   --target local
```

> `trl deploy` is currently on hold and may be reinitiated later.

In architectural documentation, use **execution** when referring to the broader execution system. `deploy` refers specifically to the CLI command.

---

# Output

`explain` and `optimize` support structured output:

```bash
--output=json
--output=yaml
```

Without `--output`, TRL uses its human-readable CLI reporting path.

### JSON

Use JSON when another tool, script, or CI system needs the report.

```bash
trl optimize ./app.yaml --output=json
```

### YAML

Use YAML when the resulting Kubernetes manifests are the required output.

```bash
trl optimize ./app.yaml --output=yaml
```

### Verbose

```bash
trl optimize ./app.yaml --verbose
```

For YAML output, `--verbose` keeps the manifest on standard output and emits the detailed report separately on standard error.

This preserves YAML as machine-consumable output.

---

# Standard Input and Piping

TRL accepts a manifest path as command input.

For rendered Kubernetes YAML, a Unix-style pipeline can be used where the current input loader supports standard input:

```bash
helm template ./chart | trl optimize -
```

Check the installed CLI help before relying on `-` in automation.

---

# Common Workflows

## Inspect

```bash
trl explain ./app.yaml
```

## Optimize

```bash
trl optimize ./app.yaml
```

## Optimize without execution

```bash
trl optimize ./app.yaml --dry-run
```

## Machine-readable report

```bash
trl optimize ./app.yaml --output=json > report.json
```

## Machine-readable manifests

```bash
trl optimize ./app.yaml --output=yaml > optimized.yaml
```

## Manifest + verbose diagnostics

```bash
trl optimize ./app.yaml --output=yaml --verbose > optimized.yaml
```

The manifest remains in `optimized.yaml`; the verbose report is emitted separately through stderr.

---

# Command Help

The CLI itself is the authoritative source for available flags:

```bash
trl explain --help
trl optimize --help
trl run --help
trl deploy --help
```

When this reference and the installed CLI differ, use the CLI help for the version you are running.

---

## Related Documentation

- [System Model](system-model.md) — conceptual model and responsibilities
- [Architecture](architecture.md) — engine and IR architecture
- [Guarantees](guarantees.md) — behavioral guarantees
- [Vision](vision.md) — future direction
- [Documentation Index](README.md)
