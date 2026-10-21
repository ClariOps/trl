# 🏗 TRL Architecture

TRL is a pipeline-based pre-deployment intelligence system for Kubernetes.

It analyzes, optimizes, validates, and secures Kubernetes resources before they are passed to the final output or optional execution stage.

---

# 🧭 1. High-Level Architecture

```text
Input
  │
  ▼
Intermediate Representation (IR)
  │
  ▼
┌───────────────────────────────┐
│       Preparation Phase       │
│                               │
│  Optimizer → Validator       │
│              → Security      │
└───────────────┬───────────────┘
                │
                ▼
          Prepared IR
                │
                ▼
            Renderer
                │
                ▼
             Output
                │
                ▼
      Optional Cloud Engine
```

### Important

**Preparation** is a conceptual phase.

It groups the engines that inspect or prepare the deployment state.

It is not a separate engine or implementation component.

---

# 🧱 2. Intermediate Representation

TRL converts supported Kubernetes resources into a shared Intermediate Representation (IR).

The IR provides a common structure between input handling and rule processing.

```text
Kubernetes Manifest
        │
        ▼
      Input
        │
        ▼
       IR
        │
        ▼
     Engines
```

The IR helps TRL:

- normalize resources
- separate parsing from rule logic
- provide a common structure for engines

Examples:

```text
Deployment
    ↓
DeploymentIR

Service
    ↓
ServiceIR

PersistentVolumeClaim
    ↓
PersistentVolumeClaimIR
```

---

# 🔌 3. Independent Engines

TRL is composed of independent engines operating on the shared IR.

The engines are intended to be:

- self-contained
- replaceable
- independently understandable
- independently testable
- responsible for their own logic
- free from dependencies on another engine's internal implementation

"Plug-and-play" describes this architectural goal:

> An engine should be usable as a distinct module within a workflow without requiring another engine to understand its internal implementation.

It does **not** imply that TRL currently provides a dynamic plugin-loading framework.

---

# 🔄 4. Engine Independence vs Workflow

These are two different concepts.

```text
ENGINE INDEPENDENCE
        │
        ▼
"What does this module own?"

        +

WORKFLOW
        │
        ▼
"When is this module executed?"
```

The current default workflow is:

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
Optional Cloud Engine
```

The workflow order does not create implementation coupling.

For example:

```text
Optimizer
    │
    │ produces a resulting IR
    ▼
Validator
```

means that Validator sees the resulting state.

It does not mean that Validator contains or depends on Optimizer's implementation.

---

# 🧠 5. Engine Responsibilities

Engine ownership is based on **responsibility**.

It is not based simply on the Kubernetes field being inspected.

```text
                         Engine Responsibility
                                  │
              ┌───────────────────┼──────────────────┐
              │                   │                  │
              ▼                   ▼                  ▼
       Improve / change      Detect configuration  Detect security /
            state                 problem            policy risk
              │                   │                  │
              ▼                   ▼                  ▼
          Optimizer             Validator           Security
```

The same Kubernetes field may be examined by more than one engine when the purpose is different.

---

# 🔧 6. Optimizer

The Optimizer is responsible for optimization decisions that may change the deployment state.

Examples may include:

- establishing optimization defaults
- improving resource configuration
- applying optimization policies
- adjusting configuration according to optimization rules

Conceptually:

```text
Input State
    │
    ▼
Optimizer Rule
    │
    ▼
Optimization Decision
    │
    ▼
Modified IR
```

### Current behavior

Optimizer rules may mutate IR.

Mutations must be explicitly reported.

---

# ⚠️ 7. Validator

The Validator detects and reports configuration problems.

It may:

- identify invalid or undesirable configuration
- produce warnings
- produce errors
- explain impact
- provide recommendations

Conceptually:

```text
Input State
    │
    ▼
Validator Rule
    │
    ▼
Finding
```

Validator rules are read-only.

They do not modify IR.

---

# 🔐 8. Security

Security detects security and policy risks.

It may:

- identify dangerous configurations
- report severity
- explain impact
- provide remediation guidance

Conceptually:

```text
Input State
    │
    ▼
Security Rule
    │
    ▼
Security Finding
```

Security rules are read-only.

They do not modify IR.

---

# 🎨 9. Renderer

The Renderer converts the prepared IR into the requested output representation.

```text
Prepared IR
    │
    ▼
Renderer
    │
    ▼
Output
```

The Renderer does not decide:

- what should be optimized
- whether a configuration is problematic
- whether a configuration is a security risk

Those responsibilities belong to the preparation engines.

---

# ☁️ 10. Cloud Engine

The Cloud Engine operates on the final output representation.

```text
Final Output
     │
     ▼
Cloud Engine
     │
     ▼
Target Environment
```

Its responsibility is execution.

It is separate from the preparation engines.

The architectural term should remain **Cloud Engine**.

The user-facing command `trl deploy` can be documented separately as the deployment operation.

---

# 🔒 11. Documented Engine Boundaries

TRL currently follows these boundaries:

| Engine | Responsibility | Current IR behavior |
|---|---|---|
| Optimizer | Improve / change deployment state | May mutate |
| Validator | Detect configuration problems | Read-only |
| Security | Detect security / policy risks | Read-only |
| Renderer | Convert prepared IR to output | Read-only |
| Cloud Engine | Execute final representation | Operates on final output |

These are **documented architectural boundaries**.

They are not currently enforced by a separate contract-authority engine.

The purpose of documenting them is to keep the implementation and contributions consistent.

---

# 🧩 12. Rule Architecture

Engines contain rules.

Rules should be:

- self-contained
- deterministic
- isolated
- independently testable
- free from hidden shared state

A rule should not depend on another rule's internal implementation.

Conceptually:

```text
Engine
  │
  ├── Rule A
  ├── Rule B
  ├── Rule C
  └── Rule D
```

The engine provides the responsibility boundary.

The individual rule provides the specific behavior.

---

# 🏷 13. Rule Classification

The key contributor rule is:

> **Classify rules by responsibility, not by the field they inspect.**

For example:

```text
CPU request
    │
    ├── Optimizer rule
    │      └── changes / improves state
    │
    └── Validator rule
           └── detects / reports a problem
```

Therefore this classification is too simplistic:

```text
Missing field → Optimizer
Bad field     → Validator
```

Instead:

```text
What does the rule do?
        │
        ├── Change / improve state → Optimizer
        ├── Detect configuration   → Validator
        └── Detect security risk   → Security
```

---

# 🔁 14. Data Flow

The default workflow passes the shared IR forward.

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
                 Output
```

Optimizer changes are visible to subsequent engines because the workflow passes the resulting IR forward.

This is workflow behavior, not implementation coupling.

---

# 📊 15. Reporting and Output

TRL separates engine processing from output representation.

Conceptually:

```text
                    TRL RESULT
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
         CLI           JSON          YAML
       Human         Machine       Manifest
       report        report        output
```

Current reporting includes:

- human-readable CLI reporting
- JSON reporting
- YAML output for manifests

The output format does not change engine ownership.

---

# 🧪 16. Predictable Behavior

The architecture aims to provide:

- deterministic rule behavior
- explicit mutation reporting
- clear engine responsibilities
- isolated rules
- predictable workflow composition

The important distinction is:

```text
Documented boundary
        ≠
Runtime authority system
```

TRL currently relies on implementation structure, rule design, tests, and contributor discipline to maintain these boundaries.

---

# 🔮 17. Future Engines

Future engines should preserve the same architectural principles.

Possible future capabilities include:

```text
AutoFix
Relationship Engine
Cloud Adapter
Cost Intelligence
AI-based Intelligence
Multi-Orchestrator Support
```

A future engine should define its own responsibility.

For example:

```text
Optimizer
    → optimization responsibility

Validator
    → configuration analysis

Security
    → security / policy analysis

AutoFix (future)
    → explicit correction responsibility
```

This prevents future engines from being forced into today's classifications.

---

# 🔧 18. AutoFix — Future

AutoFix is planned as a future correction capability.

Conceptually:

```text
Validator / Security
        │
        ▼
     Finding
        │
        ▼
     AutoFix
     (future)
        │
        ▼
    Corrected State
```

AutoFix should remain separate from detection.

Its future mutation behavior should be explicitly documented when implemented.

No current architecture should claim that AutoFix already exists.

---

# 🧩 19. Relationship Engine — Future

A future Relationship Engine may analyze relationships between resources.

Examples:

```text
Deployment
     │
     ▼
Service
     │
     ▼
Ingress
```

Potential checks include:

- Deployment without Service
- Service with unmatched selectors
- Ingress pointing to a missing backend

Its implementation and workflow position should be defined when the engine is introduced.

---

# ☁️ 20. Cloud Adapter — Future

A future Cloud Adapter may perform environment-specific transformations.

For example:

```text
Prepared Output
      │
      ▼
Cloud Adapter
      │
      ▼
Environment-specific Output
      │
      ▼
Cloud Engine
```

Examples may include:

- AKS-specific configuration
- GKE-specific configuration
- EKS-specific configuration
- storage classes
- load balancer configuration

This remains a future architecture concept until implemented.

---

# 🎯 21. Architecture in Four Rules

The TRL architecture can be remembered through four simple ideas:

```text
1. Engines are independent modules.

2. Responsibility determines engine ownership.

3. Current implementation determines what an engine may do.

4. Workflow determines execution order.
```

Or:

```text
RESPONSIBILITY
"What do I own?"
        │
        ▼
ENGINE
        │
        ▼
CURRENT CAPABILITY
"What can I do?"
        │
        ▼
WORKFLOW
"When do I run?"
        │
        ▼
OUTPUT
"What do I produce?"
```

> **Engine independence is the module design.  
> Responsibility defines ownership.  
> Current implementation defines capability.  
> Workflow defines composition.**