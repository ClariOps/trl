# 🚀 TRL (Truck Overload) — Example Scenarios

This directory contains curated Kubernetes manifests designed to demonstrate the capabilities of **TRL**.

These examples are intentionally crafted to simulate real-world DevOps scenarios across **validation, security, and optimization**.

---

## 📂 Available Examples

### 🔴 `bad.yaml` — Misconfigured Deployment (Full Issues)

A deliberately flawed setup that triggers multiple TRL rules.

**Covers:**

* Security risks (privileged container, latest image tag)
* Missing health checks (readiness/liveness probes)
* Poor resource configuration
* Unsafe service exposure (NodePort)

👉 Use this to see TRL’s **full detection capability**

```bash
trl explain examples/demo/bad.yaml
trl optimize examples/demo/bad.yaml
```

---

### 🟢 `good.yaml` — Production-Ready Configuration

A clean and well-configured deployment following Kubernetes best practices.

**Covers:**

* Proper probes
* Secure container settings
* Balanced resource allocation
* Safe service exposure (ClusterIP)

👉 Use this to verify that TRL:

* does **not produce noise**
* respects good configurations

```bash
trl explain examples/demo/good.yaml
```

---

### 🔐 `security.yaml` — Security-Focused Issues

A minimal setup designed to highlight **security misconfigurations**.

**Covers:**

* Privileged containers
* Root execution risks
* Unsafe image tagging

👉 Use this to isolate and test **Security Engine behavior**

```bash
trl explain examples/demo/security.yaml
```

---

### ⚙️ `perf.yaml` — Resource Optimization Scenario

Focuses on inefficient CPU and memory configurations.

**Covers:**

* Under-provisioning
* Over-provisioning
* Resource imbalance

👉 Use this to evaluate **Optimization Engine recommendations**

```bash
trl optimize examples/demo/perf.yaml
```

---

## 🧠 What These Examples Demonstrate

These scenarios highlight TRL’s core capabilities:

| Capability          | Demonstrated In         |
| ------------------- | ----------------------- |
| Validation          | bad.yaml                |
| Security            | bad.yaml, security.yaml |
| Optimization        | bad.yaml, perf.yaml     |
| Noise-free Analysis | good.yaml               |

---

## 🔍 Explain vs Optimize

TRL provides two main analysis modes:

### 🔎 Explain Mode

```bash
trl explain <file>
```

* Read-only analysis
* Detects issues and risks
* Provides suggestions

---

### ⚙️ Optimize Mode

```bash
trl optimize <file>
```

* Includes all explain features
* Adds optimization insights
* Injects safe defaults (when applicable)

---

## 🎯 Why This Matters

These examples simulate real-world DevOps challenges:

* Prevent misconfigurations before deployment
* Improve security posture
* Optimize resource usage
* Standardize best practices

---

## 🚀 Recommended Demo Flow

```bash
trl explain examples/demo/bad.yaml
trl optimize examples/demo/bad.yaml
trl explain examples/demo/good.yaml
```

This demonstrates:

1. Problem detection
2. Suggested improvements
3. Clean configuration validation

---

## 🧩 Philosophy

TRL focuses on:

* **Clarity over automation**
* **Suggestions over implicit changes**
* **Real DevOps value over complexity**

---

## 📌 Note

These examples are intentionally minimal and focused.
They are designed to be:

* easy to understand
* quick to test
* effective for demonstration

---
