# 🚀 trload (Truck Overload) — Example Scenarios

This directory contains curated Kubernetes manifests designed to demonstrate the capabilities of **trload**.

These examples are intentionally crafted to simulate real-world DevOps scenarios across **validation, security, and optimization**.

---

## 📂 Available Examples

### 🔴 `bad.yaml` — Misconfigured Deployment (Full Issues)

A deliberately flawed setup that triggers multiple trload rules.

**Covers:**

* Security risks (privileged container, latest image tag)
* Missing health checks (readiness/liveness probes)
* Poor resource configuration
* Unsafe service exposure (NodePort)

👉 Use this to see trload’s **full detection capability**

```bash
trload explain examples/demo/bad.yaml
trload optimize examples/demo/bad.yaml
```

---

### 🟢 `good.yaml` — Production-Ready Configuration

A clean and well-configured deployment following Kubernetes best practices.

**Covers:**

* Proper probes
* Secure container settings
* Balanced resource allocation
* Safe service exposure (ClusterIP)

👉 Use this to verify that trload:

* does **not produce noise**
* respects good configurations

```bash
trload explain examples/demo/good.yaml
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
trload explain examples/demo/security.yaml
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
trload optimize examples/demo/perf.yaml
```

---

## 🧠 What These Examples Demonstrate

These scenarios highlight trload’s core capabilities:

| Capability          | Demonstrated In         |
| ------------------- | ----------------------- |
| Validation          | bad.yaml                |
| Security            | bad.yaml, security.yaml |
| Optimization        | bad.yaml, perf.yaml     |
| Noise-free Analysis | good.yaml               |

---

## 🔍 Explain vs Optimize

trload provides two main analysis modes:

### 🔎 Explain Mode

```bash
trload explain <file>
```

* Read-only analysis
* Detects issues and risks
* Provides suggestions

---

### ⚙️ Optimize Mode

```bash
trload optimize <file>
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
trload explain examples/demo/bad.yaml
trload optimize examples/demo/bad.yaml
trload explain examples/demo/good.yaml
```

This demonstrates:

1. Problem detection
2. Suggested improvements
3. Clean configuration validation

---

## 🧩 Philosophy

trload focuses on:

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
