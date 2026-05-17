
# TRL — Pre-Deployment Intelligence for Kubernetes

> Analyze • Optimize • Secure • Validate — before it hits your cluster

---

## 🚀 What is TRL?

TRL is a CLI-first engine that **analyzes and improves Kubernetes manifests before deployment**. 

It acts as a **pre-deployment intelligence layer**, helping teams detect issues, optimize resources, and enforce best practices.

Deployment is optional — TRL can run purely as an analysis engine or integrate into CI/CD pipelines.

👉 [See system model for how TRL works conceptually](docs/system-model.md)

---

## 📚 Documentation

TRL documentation is structured across multiple layers (architecture, system model, guarantees, and vision).

👉 Start here: [Documentation Index](docs/README.md)

---

## 🔥 Why TRL?

Unlike traditional tools that focus only on linting or validation:

- TRL combines validation, security, and optimization in a single run
- Provides actionable fixes (not just warnings)
- Focuses on pre-deployment intelligence, not post-failure debugging
- Designed for clarity and fast feedback, not complex pipelines

## ⚖️ Comparison

| Tool        | Validation | Security | Optimization | Auto Fix |
|------------|-----------|----------|-------------|---------|
| kube-score | ✅        | ❌       | ❌          | ❌      |
| trivy      | ❌        | ✅       | ❌          | ❌      |
| TRL        | ✅        | ✅       | ✅          | 🚧      |

## 🎯 The Problem

Kubernetes is powerful — but:

* ❌ Over-provisioned resources → wasted cloud cost
* ❌ Under-provisioned apps → instability under load
* ❌ Missing probes → unreliable deployments
* ❌ Security misconfigurations → critical risks
* ❌ Exposure misconfigurations → attack surface

Most tools detect problems **after deployment**.

👉 By then, it's already too late.

---

## 💡 The Solution

TRL shifts validation **left** — into the development phase.

It automatically:

* 🔍 Detects misconfigurations
* ⚙️ Optimizes resource allocation
* 🔐 Flags security risks
* 📊 Provides actionable fixes

Before anything reaches your cluster.

---

## ⚡ Key Capabilities

* 🧠 Intelligent resource optimization (CPU, memory, replicas)
* ⚠️ Validation engine (probes, exposure, scaling)
* 🔐 Security analysis (root user, privileged containers, image tags)
* 📦 Multi-resource support (Deployment, Service, PVC, ConfigMap, Secret, Ingress)
* 🎯 Actionable suggestions with impact + fixes
* 🧪 Dry-run mode for safe analysis

---

## 🔥 Quick Start

```bash
git clone <repo>
cd trl
pip install -r requirements.txt

### Analyze & Optimize (Recommended)

python -m trl optimize ./examples/demo/bad.yaml --dry-run 

### Deploy (Optional)

python -m trl optimize ./examples/demo/good.yaml --target=local
```

---

## 📊 Example Output (CLI)

```text
████████╗██████╗ ██╗     
╚══██╔══╝██╔══██╗██║     
   ██║   ██████╔╝██║     
   ██║   ██╔══██╗██║     
   ██║   ██║  ██║███████╗
   ╚═╝   ╚═╝  ╚═╝╚══════╝

🚚 TRL — Pre-Deployment Intelligence System
────────────────────────────────────────────
Analyze • Optimize • Validate • Secure

"Making Kubernetes predictable before it runs"


01:21:24 | INFO     | trl.cli.main | args, Namespace(cmd='optimize', file='./trl/examples/demo/bad.yaml', target=None, context=None, verbose=False, dry_run=True, skip_rules=False, allow_rules=False, apply_aks_defaults=False, output=None)
01:21:24 | INFO     | trl.modules.optimizer.engine | Initializing optimizer ........
01:21:24 | INFO     | trl.modules.optimizer.engine | 2 resources loaded
01:21:24 | INFO     | trl.modules.optimizer.engine | Optimizer completed

01:21:24 | INFO     | trl.modules.validator.engine | Initializing Validator ...
01:21:24 | INFO     | trl.modules.validator.engine | Validator completed

01:21:24 | INFO     | trl.modules.security.engine | Initializing Security check ...
01:21:24 | INFO     | trl.modules.security.engine | Security check completed

01:21:24 | INFO     | trl.modules.renderer.engine | Initializing Renderer ...
01:21:24 | INFO     | trl.modules.renderer.engine | Renderer completed

01:21:24 | INFO     | trl.modules.cloud.engine | Dry-run enabled, skipping deployment


--------------------------------------------------
Resource: backend
--------------------------------------------------
❌ [HIGH] privileged-container

⚠ [LOW] under-provisioning

⚠ [MEDIUM] no-readiness-probe

⚠ [MEDIUM] no-liveness-probe

⚠ [LOW] latest-tag

⚠ [MEDIUM] run-as-root

--------------------------------------------------
Resource: backend-service
--------------------------------------------------
⚠ [MEDIUM] nodeport-exposure


Status: FAILED
Found 7 issues (❌ 1 errors, ⚠ 6 warnings, 💡 0 optimizations)
```
or 
👉 Full output: see docs/output-example.md

---

## 📊 Example Output JSON (Pipeline)
```bash
   python -m trl explain ./trl/examples/demo/good.yaml  --verbose --output=json
```

```json
   {
  "summary": {
    "status": "PASSED",
    "total": 1,
    "errors": 0,
    "warnings": 1,
    "optimizations": 0
  },
  "resources": {
    "backend-clean": {
      "errors": [],
      "warnings": [
        {
          "rule": "run-as-root",
          "severity": "medium",
          "category": "security"
        }
      ],
      "optimizations": []
    }
  }
}
```
---
## 🧪 Example Manifests

```bash
examples/demo/bad.yaml   # intentionally misconfigured
examples/demo/good.yaml  # optimized version
```

Run:

```bash
trl optimize ./examples/demo/bad.yaml --dry-run
```
Run with Deployment(Optional):
```bash
trl optimize ./examples/demo/bad.yaml --target=local
```


---
## 🔄 CI/CD Integration

TRL is designed to run in pipelines.

Example using GitHub Actions:

```yaml
- name: Run TRL
  run: |
    python -m trl optimize ./k8s.yaml --dry-run --output=json > report.json

- name: Fail if issues found
  run: |
    cat report.json | jq -r '.status' | grep FAILED && exit 1 || exit 0
```

---

## 📦 Helm Support

TRL does not directly parse Helm charts.

Instead, it works with **rendered Kubernetes manifests**, enabling seamless integration with Helm workflows.

```bash
helm template mychart | trl optimize -
```

This approach:

* avoids re-implementing Helm
* works with any chart
* keeps TRL lightweight and fast

Native Helm support is planned in future releases.

---

## 🏗 How It Works

TRL follows a pipeline-based architecture:

1. Load manifests → convert into IR (Intermediate Representation)
2. Run engines in order:

   * Optimizer (applies safe improvements)
   * Validator (detects misconfigurations)
   * Security (detects risks)

3. Render final manifests from IR
4. (Optional) Deploy to cluster

👉 See full architecture:
docs/architecture.md


---

## 🧠 Core Philosophy

> Fix problems before they reach the cluster.

---

## 👥 Who is this for?

* DevOps Engineers
* Backend developers deploying to Kubernetes
* Startups optimizing cloud cost
* Teams enforcing deployment best practices

---

## ⚠️ Current Status

* CLI: ✅ Stable
* Engines: ✅ Functional
* Multi-resource support: ✅
* Cloud deployment: ⚠️ In progress

---

## 🗺 Roadmap

* Auto-fix engine for safe automated remediation
* Cloud-specific adaptation layer (AKS, GKE, EKS)
* Relationship-aware analysis (cross-resource intelligence)
* Rule expansion (cost + reliability)
* AI-powered suggestions
* SaaS platform (hosted analysis)
* Multi-orchestrator support

---

Experimental DSL support is under development and will be introduced in future releases.

## 🤝 Contributing

Contributions will be opened soon.

We are currently stabilizing architecture and rules to ensure a consistent foundation.

Stay tuned 🚀
---

## 📜 License

Copyright 2026 TruckOverload

Apache 2.0 — See [LICENSE](LICENSE) file for details.
##
