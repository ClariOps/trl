

# 🏗 TRL Architecture

TRL is a **pipeline-based pre-deployment intelligence system** for Kubernetes.

It analyzes, optimizes, validates, and secures manifests **before deployment**, ensuring predictable and production-ready configurations.

---

## 🔄 High-Level Flow

```text
Input → IR → Optimizer → Validator → Security → Renderer → (Optional) Cloud Engine
```

---

## 🧠 Architectural Philosophy

TRL is built on three core principles:

### 1. Pre-Deployment Intelligence

All decisions are made **before deployment**, not after failure.

---

### 2. Clear Separation of Concerns

| Layer        | Responsibility                |
| ------------ | ----------------------------- |
| Input        | Load manifests                |
| IR           | Normalize data                |
| Engines      | Apply logic (rules)           |
| Renderer     | Generate final manifests      |
| Cloud Engine | Execute deployment (optional) |

---

### 3. Predictable System Behavior

* Deterministic output (same input → same result)
* No hidden mutations
* Explicit reporting of all changes
* Strict module boundaries

---

## 📥 1. Input Layer

TRL accepts:

* Single YAML file
* Multiple YAML files
* Directory of manifests
* Standard input (stdin)

```bash
trl optimize ./app.yaml
```

---

## 🔧 2. Intermediate Representation (IR)

All manifests are converted into a unified structure:

> **IR (Intermediate Representation)**

### 🎯 Purpose

* Normalize Kubernetes resources
* Decouple parsing from logic
* Enable rule-based processing

### 🧱 Examples

```text
Deployment → DeploymentIR  
Service → ServiceIR  
PVC → PersistentVolumeClaimIR
```

---
## ⚙️ 3. Engine Architecture

TRL is composed of independent engines that operate on the shared Intermediate Representation (IR).

The engines are designed to be:

- Self-contained
- Replaceable
- Plug-and-play
- Responsible for their own logic
- Free from dependencies on other engines' internal implementations

### 🔌 Engine Independence vs Workflow Order

Engine independence and workflow order are separate concepts.

> **Engine independence describes the module boundary. Workflow order describes how modules are composed for a particular execution.**

The default TRL workflow is:

```text
Input
  ↓
IR
  ↓
Optimizer
  ↓
Validator
  ↓
Security
  ↓
Renderer
  ↓
Cloud Engine (optional)
```

This order is the current default workflow.

It does **not** mean that Validator is structurally dependent on Optimizer, or that Security is structurally dependent on Validator.

Each engine must remain usable according to its own contract.

---

### 🔒 Engine Contracts

| Engine | Reads IR | May Modify IR | Produces Reports | Default Position |
| :--- | :---: | :---: | :---: | :---: |
| **Optimizer** | ✅ | ✅ | ✅ | 1 |
| **Validator** | ✅ | ❌ | ✅ | 2 |
| **Security** | ✅ | ❌ | ✅ | 3 |
| **Renderer** | ✅ | ❌ | Output | 4 |
| **Cloud Engine** | Output | ❌ | Operational | 5 |

The **default position is a workflow decision**, not a module dependency.

### 🧠 Optimizer

The Optimizer is the only normal preparation engine allowed to autonomously modify the deployment state.

Its responsibility is to improve or prepare the state according to optimization rules.

Examples include:

- Establishing safe defaults
- Improving resource configuration
- Adjusting resource values according to optimization policy
- Applying safe optimization decisions

Every mutation must be reported.

### ⚠️ Validator

The Validator evaluates the current deployment state.

It:

- Detects configuration problems
- Reports warnings and errors
- Provides actionable explanations
- May suggest fixes

It **must not modify IR**.

A Validator rule is defined by its responsibility to **detect and report**, not by whether the problem happens to involve a missing, explicit, high, low, or default value.

### 🔐 Security

Security evaluates the deployment state for security and policy risks.

It:

- Detects dangerous configurations
- Reports security findings
- Provides severity and remediation information

It **must not modify IR**.

Security rules follow the same independence principle as Validator rules but have a security/policy responsibility.

### 🎨 Renderer

Renderer converts the prepared IR into the required output representation.

It does not decide whether the deployment should be optimized, validated, or considered secure.

Its responsibility is:

```text
Prepared IR → Kubernetes Manifest
```

### ☁️ Cloud Engine

The Cloud Engine operates on the final deployment representation.

It is responsible for deployment operations and does not modify the prepared manifest as part of deployment logic.

---

## 🧩 Rule Design Principle

TRL may eventually contain a large number of rules contributed by different developers.

To keep those rules maintainable, contributors should classify a rule by **what the rule is responsible for doing**, not simply by what field it examines.

### Optimizer Rule

Use when the rule is responsible for **changing the deployment state**.

```text
Input state
    ↓
Optimization decision
    ↓
Modified state
```

### Validator Rule

Use when the rule is responsible for **detecting and reporting a configuration problem**.

```text
Input state
    ↓
Validation decision
    ↓
Finding / warning / error
```

### Security Rule

Use when the rule is responsible for **detecting security or policy risk**.

```text
Input state
    ↓
Security decision
    ↓
Security finding
```

### 🚫 Important

Do not classify rules using a simplistic rule such as:

```text
Missing field → Optimizer
Bad field → Validator
```

That is not a TRL architectural boundary.

The correct question is:

> **Is this rule responsible for changing the state, detecting a configuration problem, or detecting a security/policy risk?**

---

## 🔁 Data Flow

The default workflow shares the IR between preparation engines:

```text
                    Shared IR
                       │
                       ▼
                 ┌───────────┐
                 │ Optimizer │
                 └─────┬─────┘
                       │
                 Modified IR
                       │
                       ▼
                 ┌───────────┐
                 │ Validator │
                 └─────┬─────┘
                       │
                 Same IR
                       │
                       ▼
                 ┌───────────┐
                 │ Security  │
                 └─────┬─────┘
                       │
                       ▼
                  Prepared IR
                       │
                       ▼
                   Renderer
                       │
                       ▼
                 Final Manifest
                       │
                       ▼
                Cloud Engine
                  (optional)
```

The important architectural property is:

> **Each engine owns its own responsibility. The workflow owns the order in which independent engines are composed.**

Optimizer mutations are visible to subsequent engines because the default workflow intentionally passes the resulting IR forward.

That visibility is a workflow behavior, not a dependency between engine implementations.
---

## 📊 4. Rule System

All engines operate using **rules**.

---

### 🧩 Rule Characteristics

* Self-contained logic
* Deterministic behavior
* No shared state
* No cross-rule dependency

---

### 🏷 Rule Categories

```text
scaling
security
cost
reliability
network
```

---

### 🔁 Rule Execution Model

```text
For each resource:
    For each rule:
        if match:
            apply logic
```

---

## 🧱 5. Rule Contracts

### 🔧 Optimizer Rules

* Can modify IR
* MUST report changes

```python
        ctx.report.optimization(rule= self.name,
            engine = self.engine,
            resource=ir.name,
            message= f"CPU request not defined → defaulting to {self.DEFAULT_CPU} → ensure baseline scheduling"
            )
```

---

### ⚠️ Validator Rules

* Match → Condition → Validate
* MUST NOT modify IR

```python
def validate(self, ir, ctx):
        ctx.report.warning(
            engine=self.engine,
            category=self.category,
            severity=self.severity,
            rule=self.name,
            resource=ir.name,
            issue="Service exposed via NodePort → opens access on every node IP",
            impact="Increases attack surface → may lead to unauthorized access",
            fix="Use ClusterIP for internal services or Ingress for controlled external access"
        )
```

---

### 🔐 Security Rules

* Same structure as validator
* Higher severity focus

---

### 🔒 Rule Constraints

* MUST be isolated
* MUST be deterministic
* MUST NOT share state
* MUST NOT depend on other rules

---

## 🔁 6. Data Flow Model

* IR is shared across engines
* Renderer produces final canonical manifests
* No deep copies (unless explicitly needed)
* Optimizer mutations are visible to all subsequent engines
* No cross-resource logic (current limitation)

---

## 📦 7. Output Aggregation

Results are grouped based on Resources with :

* ❌ Errors (blocking)
* ⚠ Warnings (non-blocking)
* 💡 Optimizations (applied changes)

---

## 📊 8.

TRL produces three outputs:

1. **Human-readable report (CLI)**
2. **Machine-readable report (JSON)** for CI/CD
3. **Optimized manifests (YAML)**

### Status Model

- `PASSED` → no errors
- `FAILED` → errors present

---

# 🧩 Product Architecture Layers

TRL is evolving into a **multi-layer system**, not just a CLI.

---

## 🧱 1. TRL Core (Current — Foundation)

**Status: ✅ Implemented**

Capabilities:

* IR system
* Rule engine
* Optimizer / Validator / Security
* CLI interface

👉 This is the **decision engine**
👉 Must remain stable and predictable

---

## 🚀 2. TRL Deploy (Planned)

**Goal:** One-command deployment

```bash
trl deploy app.yaml
```

Capabilities:

* Wraps kubectl / Helm
* Uses TRL intelligence
* Safe deployment execution

👉 Developer-friendly UX layer

---

## ☁️ 3. TRL SaaS (Future)

**Goal:** Hosted intelligence platform

Capabilities:

* Upload YAML → get analysis
* Cost + security insights
* Team-level usage

👉 Business and scaling layer

---

# 🔮 Future Architecture Evolution

Planned improvements:

---

### ☁️ Cloud Adapter Layer

Applies environment-specific adjustments before deployment.

Responsibilities:

- Inject cloud-specific configurations (AKS, GKE, EKS)
- Handle storage classes, load balancer types, etc.

#### Constraints:

- MUST NOT mutate IR
- MUST operate on rendered manifests only
- Runs before Cloud Engine
- Keeps Cloud Engine execution-only

---

### 🔧 AutoFix Engine

A controlled mutation engine for applying fixes suggested by Validator and Security.

Responsibilities:

- Apply safe, rule-based fixes
- Convert suggestions into actionable changes
- Operate only when explicitly enabled

#### Design Principles:

- Separate detection from action
- Preserve deterministic behavior
- All mutations must be explicitly reported

#### Position in Pipeline (Future):

Input → IR → Optimizer → Validator → Security → AutoFix → Renderer

---

### 🧩 Relationship Engine

A dedicated engine for cross-resource analysis.

Responsibilities:

- Detect relationships between resources (Deployment, Service, Ingress)
- Identify broken or missing connections
- Surface system-level misconfigurations

Examples:

- Deployment without Service  
- Service with unmatched selectors  
- Ingress pointing to non-existent backend  

#### Constraints:

- MUST NOT mutate IR (initial phase)
- Operates after Validator and Security

---

### 🤖 AI-Based Intelligence

* Smarter optimization suggestions
* Context-aware recommendations

---

### 🌍 Multi-Orchestrator Support

* Extend beyond Kubernetes
* Support other deployment platforms

---

### 📊 Cost Intelligence Engine

* Predict cloud cost
* Recommend savings

---

### 🧩 DSL Layer (Advanced)

* Developer-friendly abstraction
* Optional, not core

---

# 🎯 Summary

TRL is a **pipeline-driven intelligence system**:

```text
Normalize → Optimize → Validate → Secure → Render → Deploy
```

It ensures:

* safer deployments
* optimized resources
* predictable behavior

---

## 🧠 Final Principle

> TRL does not replace Kubernetes
>
> It makes Kubernetes **safe, efficient, and predictable before execution**

---

