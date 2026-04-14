# TRL — Pre-Deployment Intelligence for Kubernetes

> Analyze • Optimize • Secure • Validate — before it hits your cluster

---

## 🚀 What is TRL?

TRL is a CLI-first engine that **analyzes Kubernetes manifests before deployment** to detect issues, optimize resources, and enforce best practices automatically.

It acts as a **pre-deployment intelligence layer** for Kubernetes.

---

## 🔥 Why TRL?

Unlike traditional tools that focus only on linting or validation:

- TRL combines validation, security, and optimization in a single run
- Provides actionable fixes (not just warnings)
- Focuses on pre-deployment intelligence, not post-failure debugging
- Designed for clarity and fast feedback, not complex pipelines


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

python -m trl optimize ./examples/demo/bad.yaml --target=local --verbose=True --dry-run
```

---

## 📊 Example Output

```text
❌ Errors (1)
[HIGH] privileged-container → Container runs in privileged mode

⚠ Warnings (6)
[LOW] under-provisioning
[MEDIUM] no-readiness-probe
[MEDIUM] no-liveness-probe
[MEDIUM] nodeport-exposure
[LOW] latest-tag
[HIGH] run-as-root

💡 Optimizations (2)
[LOW] cpu-minimum
[LOW] memory-minimum → set to 128Mi to reduce OOM risk
```

👉 Full output: see docs/output-example.md

---

## 🧪 Example Manifests

```bash
examples/demo/bad.yaml   # intentionally misconfigured
examples/demo/good.yaml  # optimized version
```

Run:

```bash
trl optimize ./examples/demo/bad.yaml --target=local
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
2. Run engines:

   * Optimizer
   * Validator
   * Security
3. Aggregate findings
4. Render optimized manifests and structured report

👉 See full structured output with Issue / Impact / Fix:
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
