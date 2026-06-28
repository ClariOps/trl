
# TRL — Pre-Deployment Intelligence for Kubernetes

> Analyze • Optimize • Secure • Validate — before it hits your cluster

## 🎬 Demo

See TRL in action — analyzing a misconfigured Kubernetes manifest in seconds:

![TRL Demo](./docs/assets/trl-demo.gif)

**Built by ClariOps** — bringing clarity to Kubernetes operations.

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

### Analyze (Fastest)

python -m trl explain ./examples/demo/bad.yaml

### Analyze + Optimize (Recommended)

python -m trl optimize ./examples/demo/bad.yaml --dry-run

### Deploy (Optional)

python -m trl optimize ./examples/demo/good.yaml --target=local
```

---
## 🧭 Command Guide

TRL provides different commands depending on your use case:

| Command        | Purpose |
|---------------|--------|
| `optimize`    | Full pipeline: optimize + validate + security (recommended) |
| `explain`     | Analysis-only (no optimization) — ideal for reports and demos |
| `run`         | Execute TRL DSL workflows (experimental) |
| `deploy`      | Apply CLI based to cluster (optional) |

---

## 📊 Example Output 
👉 See: [Detailed Output](docs/transparency/output-example.md)

### CLI (human-readable)
```bash
   python -m trl explain ./trl/examples/demo/bad.yaml 
```

```text

📦 Resource: backend

❌ HIGH: privileged-container
⚠ LOW: under-provisioning
⚠ MEDIUM: no-readiness-probe
⚠ MEDIUM: no-liveness-probe
⚠ LOW: latest-tag
⚠ MEDIUM: run-as-root


📦 Resource: backend-service

⚠ MEDIUM: nodeport-exposure

📊 Summary
Errors: 1	Warnings: 6	Optimizations: 0

❌ Status: FAILED
```
---

### JSON (Pipeline)
```bash
   python -m trl explain ./trl/examples/demo/bad.yaml --output=json 
```

```json
{
  "status": "FAILED",
  "summary": {
    "errors": 1,
    "warnings": 6
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
helm create mychart
helm template ./examples/helmCharts/mychart | python -m trl optimize - --dry-run 
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

Contributions are welcome!

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines, rules, and architecture details.

We are currently stabilizing the core system, so we recommend reviewing the contribution rules before submitting changes.


## 📜 License

© 2026 ClariOps. Licensed under the Apache License 2.0 — see [LICENSE](LICENSE) for details.

##

---

## 🧩 About ClariOps

ClariOps builds developer-first tools focused on clarity, reliability, and intelligence in Kubernetes and DevOps.

TRL is the first step toward a broader platform for pre-deployment intelligence.
