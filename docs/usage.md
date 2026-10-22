# TRL CLI Reference

> Pre-deployment analysis and optimization for Kubernetes manifests.

TRL provides a small CLI surface for analyzing, optimizing, and executing Kubernetes workflows.

## Synopsis

```text
trl <command> [arguments] [options]
```

Run:

```bash
trl --help
trl <command> --help
```

---

## Commands

| Command | Purpose |
|---|---|
| `explain` | Analyze a manifest without optimization |
| `optimize` | Optimize, validate, assess security, and produce the resulting state |
| `run` | Run a TRL workflow from a workflow/DSL input |
| `deploy` | CLI-based deployment input |

---

# `trl explain`

Analyze a Kubernetes manifest without applying optimizer mutations.

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

# Render the resulting manifests as YAML
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

Run a TRL workflow from a workflow/DSL input.

## Usage

```bash
trl run <file> [options]
```

## Arguments

```text
file    Path to the workflow input
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

```bash
trl run ./workflow.yaml
```

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
trl deploy \
  --name backend \
  --cpu 500m \
  --memory 512Mi \
  --image nginx:1.27 \
  --target local
```

> `deploy` is the explicit CLI deployment command. In architectural documentation, prefer the term **execution** when describing the broader execution system.

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

TRL accepts a manifest path as the command input.

For rendered Kubernetes YAML, the intended Unix-style pattern is:

```bash
helm template ./chart | trl optimize -
```

Support for `-` depends on the current input loader; check command help before relying on stdin in automation.

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
trl --help
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
