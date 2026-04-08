# 🏗 TRL Architecture

TRL follows a **pipeline-based architecture** designed to analyze, validate, optimize, and secure Kubernetes manifests before deployment.

---

## 🔄 High-Level Flow

```text
Input YAML → IR → Engines → Aggregation → Renderer → Output
```

---

## 📥 1. Input Layer

TRL accepts:

* Single YAML file
* Multiple YAML files
* Directory of manifests
* Standard input (stdin)

Examples:

```bash
trl optimize ./examples/demo/bad.yaml
cat manifest.yaml | trl optimize -
```

---

## 🔧 2. Intermediate Representation (IR)

All input manifests are converted into a unified structure called:

> **IR (Intermediate Representation)**

### 🎯 Purpose

* Normalize different Kubernetes resources
* Enable engine-level processing
* Decouple parsing from logic

### 🧱 Example

```text
Deployment → DeploymentIR  
Service → ServiceIR  
PVC → PersistentVolumeClaimIR
```

---

## ⚙️ 3. Engine Pipeline

TRL processes IR through multiple independent engines.

Each engine is:

* modular
* rule-driven
* extensible

---

### 🧠 3.1 Optimizer Engine

**Goal:** Improve resource efficiency

#### Responsibilities:

* Set default CPU / memory
* Enforce minimum resource thresholds
* Suggest replica counts

#### Output:

* Modified IR (applies optimizations)

---

### ⚠️ 3.2 Validator Engine

**Goal:** Detect configuration issues

#### Responsibilities:

* Missing readiness/liveness probes
* Over/under-provisioning
* Incorrect service exposure (NodePort, etc.)
* Scaling inconsistencies

#### Output:

* Warnings (non-blocking issues)

---

### 🔐 3.3 Security Engine

**Goal:** Detect security risks

#### Responsibilities:

* Privileged containers
* Running as root (UID 0)
* Use of `latest` image tags
* Unsafe configurations

#### Output:

* Errors / high-severity warnings

---

### 🎨 3.4 Renderer Engine

**Goal:** Generate final manifests

#### Responsibilities:

* Convert IR back to Kubernetes YAML
* Apply optimizer changes
* Prepare output for deployment

---

### ☁️ 3.5 Cloud Engine

**Goal:** Handle deployment

#### Responsibilities:

* Deploy manifests to target environment
* Support dry-run mode
* Integrate with local or cloud clusters

---

## 📊 4. Rule System

Each engine operates using **rules**.

### 🧩 Rule Characteristics:

* Self-contained logic
* Match → Apply pattern
* Categorized (security, reliability, cost)

### 🔁 Flow:

```text
For each resource:
    For each rule:
        if match:
            execute
```

---

## 📦 5. Output Aggregation

Results from all engines are combined into:

* ❌ Errors (blocking)
* ⚠ Warnings (non-blocking)
* 💡 Optimizations (applied changes)

---

## 🧾 6. Final Output

TRL produces:

1. CLI report (human-readable)
2. Optimized manifests (via renderer)
3. Summary (issue count, status)

---

## 🧠 Design Principles

### 1. Pre-Deployment Focus

Detect and fix issues **before** reaching the cluster.

---

### 2. Modular Architecture

Each engine operates independently → easy to extend.

---

### 3. Rule-Based System

Flexible and scalable validation/optimization logic.

---

### 4. Separation of Concerns

| Layer    | Responsibility  |
| -------- | --------------- |
| Input    | Load manifests  |
| IR       | Normalize data  |
| Engines  | Process logic   |
| Renderer | Generate output |
| Cloud    | Deploy          |

---

### 5. Extensibility

TRL is designed to support:

* New resource types
* Custom rules
* Additional engines
* Future orchestrators

---

## 🔮 Future Architecture Evolution

Planned enhancements:

* 🤖 AI-based suggestion engine
* 🌍 Multi-orchestrator support (beyond Kubernetes)
* ☁️ SaaS-based analysis platform
* 📊 Cost estimation engine
* 🧩 CRD generation support

---

## 🎯 Summary

TRL transforms Kubernetes manifests into a structured pipeline:

* Normalize → Analyze → Optimize → Secure → Render

👉 Delivering **safe, efficient, and production-ready configurations** before deployment.
