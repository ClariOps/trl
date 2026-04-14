# 📊 TRL Output Example

This example demonstrates how TRL analyzes Kubernetes manifests and provides actionable feedback before deployment.

---

## 🚀 Command

```bash
python -m trl optimize ./examples/demo/bad.yaml --target=local --verbose=true --dry-run=True
```

---

## 🔍 Execution Logs (Verbose Mode)

```text
02:35:20 | INFO     | trl.cli.main | check arg target: local
02:35:20 | INFO     | trl.modules.optimizer.engine | Initializing optimizer ........
02:35:20 | INFO     | trl.modules.optimizer.engine | 2 resources loaded

02:35:20 | DEBUG    | trl.core.base | cpu-minimum: executing (resource=backend)
02:35:20 | DEBUG    | trl.core.base | cpu-minimum: completed
02:35:20 | DEBUG    | trl.core.base | memory-minimum: executing (resource=backend)
02:35:20 | DEBUG    | trl.core.base | memory-minimum: completed

02:35:20 | INFO     | trl.modules.optimizer.engine | Optimizer completed

02:35:20 | INFO     | trl.modules.validator.engine | Initializing Validator ...
02:35:20 | DEBUG    | trl.core.base | under-provisioning: executing (resource=backend)
02:35:20 | DEBUG    | trl.core.base | no-readiness-probe: executing (resource=backend)
02:35:20 | DEBUG    | trl.core.base | no-liveness-probe: executing (resource=backend)
02:35:20 | DEBUG    | trl.core.base | nodeport-exposure: executing (resource=backend-service)
02:35:20 | INFO     | trl.modules.validator.engine | Validator completed

02:35:20 | INFO     | trl.modules.security.engine | Initializing Security check ...
02:35:20 | DEBUG    | trl.core.base | latest-tag: executing (resource=backend)
02:35:20 | DEBUG    | trl.core.base | privileged-container: executing (resource=backend)
02:35:20 | DEBUG    | trl.core.base | run-as-root: executing (resource=backend)
02:35:20 | INFO     | trl.modules.security.engine | Security check completed

02:35:20 | INFO     | trl.modules.renderer.engine | Renderer completed
02:35:20 | INFO     | trl.modules.cloud.engine | Dry-run enabled, skipping deployment
```

---

## ❌ Errors

```text
[HIGH] privileged-container
Resource: backend
Issue : Container runs in privileged mode
Impact: Full host access (critical risk)
Fix   : Remove privileged: true
```

---

## ⚠ Warnings

```text
[LOW] under-provisioning
Issue : CPU (100m), Memory (128Mi) below recommended levels

[MEDIUM] no-readiness-probe
Issue : Traffic may be routed to unready pods

[MEDIUM] no-liveness-probe
Issue : Container failures may not be detected

[MEDIUM] nodeport-exposure
Issue : Service exposed on all node IPs

[LOW] latest-tag
Issue : Image uses mutable tag 'latest'

[HIGH] run-as-root
Issue : Container runs as root (UID 0)
```

---

## 💡 Optimizations Applied

```text
[LOW] cpu-minimum
Change : CPU increased from 50m → 100m

[LOW] memory-minimum
Change : Memory increased from 64Mi → 128Mi
```

---

## 📊 Summary

```text
Errors        : 1
Warnings      : 6
Optimizations : 2

Total Issues  : 9
Status        : FAILED
```

---

## 🧠 What This Shows

TRL automatically:

* Detects **critical security risks** (privileged containers, root access)
* Identifies **reliability issues** (missing probes)
* Flags **network exposure risks**
* Optimizes **resource allocation**
* Provides **clear fixes with impact**

👉 All before deployment.

---

## 🎯 Why This Matters

Without TRL:

* Issues reach production
* Costs increase due to over/under provisioning
* Security risks remain unnoticed

With TRL:

* Problems are caught early
* Infrastructure is optimized
* Deployments become predictable and safe
