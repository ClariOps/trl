## ⚖️ Role of This Document

This document defines the **strict behavioral contract** of TRL.

- Architecture describes *how the system is built*
- Guarantees define *how the system must behave*

In case of conflict, **guarantees take precedence**.

# 🔒 TRL Guarantees

TRL is designed to provide **predictable, transparent, and safe pre-deployment intelligence** for Kubernetes.

This document defines the **non-negotiable guarantees** that govern system behavior, rule design, and execution flow.

---

## 🎯 Core Guarantee

> Same input → same output → same decisions

TRL is deterministic, explicit, and free from hidden behavior.

---

## 🧠 System Behavior Guarantees

### 1. Deterministic Execution

* Identical input always produces identical output
* No randomness or hidden state
* Rule execution order is fixed and predictable

---

### 2. Explicit Mutations Only

* Only the **Optimizer Engine** is limited to modify IR
* All mutations MUST be explicitly reported
* No silent or implicit changes are allowed

---

### 3. Strict Separation of Detection and Action

* **Validator** and **Security** engines:

  * MUST NOT modify IR
  * MUST only detect and report issues

* **Optimizer Engine**:

  * Responsible for improvements and safe defaults

👉 Detection and action are intentionally separated to ensure clarity and control

---

### 4. No Hidden Side Effects

* Rules MUST be isolated
* Rules MUST NOT share state
* Rules MUST NOT depend on other rules
* Execution of one rule MUST NOT affect another

---

### 5. Pipeline Integrity

TRL follows a strict, one-directional pipeline:

```text
Input → IR → Optimizer → Validator → Security → Renderer → (Optional) Cloud Engine
```

* Each stage has a well-defined responsibility
* Later stages consume results from earlier stages
* No backward data flow is allowed

---

### 6. Transparent Reporting

Every issue or change includes:

* Resource name
* Rule name
* Category
* Clear human-readable message

Additionally:

#### Validator / Security Reports:

* issue
* fix
* (optional) impact

#### Optimizer Reports:

* exact mutation performed
* before → after values

---

### 7. Deployment Safety

* Cloud Engine:

  * MUST NOT modify manifests
  * MUST NOT apply defaults
  * MUST ONLY execute deployment

* Deployment is optional and never required for analysis

---

### 8. Environment-Agnostic Core

* Core engines (Optimizer, Validator, Security):

  * MUST NOT depend on cloud providers

* Environment-specific behavior must be applied **before deployment** (future adapter layer)

---

### 9. No Cross-Resource Logic (Current Phase)

TRL supports analyzing multiple Kubernetes resources across files and directories.

However:

* Each resource is analyzed **independently**
* No relationships are inferred between resources
* No assumptions are made about connections (e.g., Deployment ↔ Service)

This ensures:

* predictable behavior
* rule isolation
* simpler debugging

👉 Cross-resource intelligence will be introduced in a **dedicated Relationship Engine** in future versions.

---
### 10. Future: Relationship-Aware Analysis

TRL will evolve to include a **Relationship Engine** responsible for cross-resource analysis.

This engine will:

* analyze relationships between resources (Deployment, Service, Ingress, etc.)
* detect broken or missing connections
* identify system-level misconfigurations

Examples include:

* Deployment without a Service
* Service without matching selectors
* Ingress pointing to non-existent services

### Design Constraint:

* MUST NOT mutate IR (initial phase)
* MUST only detect and report issues

This preserves the core guarantee:

> Detection remains separate from mutation

---

### 11. Environment-Aware Behavior (Future)

TRL may support environment-specific behavior (e.g., AWS, Azure, GCP).

This is implemented via an **Adapter Layer** that provides context to the system.

* The Adapter Layer MUST NOT mutate IR
* It only supplies environment-specific configuration

All mutations:

* MUST occur inside the Optimizer Engine
* MUST follow the same reporting and transparency rules

👉 This ensures a single source of mutation while enabling environment-aware intelligence.

### 12. CLI Simplicity

TRL must remain:

* simple to run
* fast to execute
* easy to understand

Output must prioritize clarity over complexity.

---

## 🚫 What TRL Does NOT Guarantee

TRL intentionally does NOT:

* Guarantee perfect optimization for every workload
* Replace Kubernetes tools (kubectl, Helm)
* Manage runtime orchestration
* Provide post-deployment monitoring

TRL focuses strictly on **pre-deployment intelligence**

---

## 🔮 Future Guarantees (Planned)

As TRL evolves, additional guarantees may include:

* Safe and controlled auto-fix engine
* Cross-resource awareness
* Cost estimation accuracy
* Policy enforcement for teams

---

## 🧩 Future Extension: Auto-Fix Model

TRL will introduce a separate **AutoFix Engine** to apply fixes safely.

### Planned Flow:

```text
Optimizer → Validator → Security → AutoFix → Renderer
```

### Design Principles:

* Validator/Security detect issues
* AutoFix applies fixes (opt-in)
* Mutation remains controlled and explicit

👉 This preserves the core guarantee:
**Detection ≠ Action**

---

## 🧠 Final Principle

> TRL makes decisions visible, not magical.

Users should always understand:

* what changed
* why it changed
* how to override it

---

## 🎯 Summary

TRL guarantees:

* Predictability
* Transparency
* Safety
* Modularity

Before anything reaches your cluster.
