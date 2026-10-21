# 🧠 TRL System Model

This document explains how TRL should be **understood**.

It describes the system's mental model, responsibilities, and flow.

For implementation structure, see `architecture.md`.

For behavioral guarantees, see `guarantees.md`.

For contribution rules, see `CONTRIBUTING.md`.

---

# 🎯 1. What Is TRL?

TRL is a:

> **Pre-deployment decision system for Kubernetes.**

It helps answer:

```text
What is wrong?
What can be improved?
What is risky?
What would the resulting deployment look like?
```

TRL operates before optional execution.

```text
Traditional

Write → Deploy → Discover Problems


TRL

Write → Analyze → Prepare → Render → Decide → Optional Execution
```

The fundamental shift is:

> **From reactive debugging to proactive decision-making.**

---

# 🧠 2. The TRL Mental Model

Think of TRL as four conceptual steps:

```text
        UNDERSTAND
             │
             ▼
         PREPARE
             │
             ▼
          RENDER
             │
             ▼
     OPTIONAL EXECUTION
```

These describe **system behavior**, not four required software layers.

---

# 🧩 3. Preparation Is a Phase, Not an Engine

The Preparation Phase is a conceptual grouping of engines that analyze or prepare the deployment state.

```text
                 PREPARATION PHASE
          ┌──────────────────────────┐
          │                          │
          │  Optimizer               │
          │       ↓                  │
          │  Validator               │
          │       ↓                  │
          │  Security                │
          │                          │
          └────────────┬─────────────┘
                       │
                       ▼
                  Prepared IR
```

Important:

> **Preparation is not a super-engine.**

There is no "Preparation Engine".

There is no central intelligence authority above the engines.

The engines remain independent modules.

---

# 🔌 4. Independent Engines

Each engine has its own responsibility.

```text
┌─────────────┐
│  Optimizer  │
└─────────────┘

┌─────────────┐
│  Validator  │
└─────────────┘

┌─────────────┐
│  Security   │
└─────────────┘
```

They share the IR, but they do not need to understand each other's internal implementation.

This is the plug-and-play architectural goal.

---

# 🔄 5. Independence Does Not Mean No Workflow

Independent engines can still be composed into a workflow.

```text
ENGINE DESIGN

Optimizer ───── independent
Validator ───── independent
Security  ───── independent


WORKFLOW

Optimizer
    ↓
Validator
    ↓
Security
```

Therefore:

> **Engine independence answers "Who owns this responsibility?"**

while:

> **Workflow answers "When does this engine run?"**

These are separate concepts.

---

# 🧭 6. Current Default Flow

The current default TRL flow is:

```text
Input
  │
  ▼
 IR
  │
  ▼
Optimizer
  │
  ▼
Validator
  │
  ▼
Security
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
Optional Cloud Execution
```

This is the **current default workflow**.

It should not be interpreted as a permanent restriction on future workflow composition.

---

# 🔧 7. What Each Engine Means

## Optimizer

The Optimizer is responsible for:

> **Improving or changing deployment state according to optimization logic.**

Current behavior:

```text
Inspect
   ↓
Decide
   ↓
Change IR
   ↓
Report mutation
```

---

## Validator

The Validator is responsible for:

> **Detecting configuration problems.**

Current behavior:

```text
Inspect
   ↓
Evaluate
   ↓
Report
```

Validator does not modify IR.

---

## Security

Security is responsible for:

> **Detecting security and policy risks.**

Current behavior:

```text
Inspect
   ↓
Evaluate
   ↓
Report
```

Security does not modify IR.

---

## Renderer

Renderer is responsible for:

> **Turning the resulting IR into the requested output representation.**

```text
Prepared IR
    ↓
Renderer
    ↓
Output
```

Renderer does not decide whether something should be optimized, validated, or secured.

---

## Cloud Execution

The Cloud Execution Engine is responsible for:

> **Executing the final result in a target environment.**

```text
Final Output
    ↓
Cloud Execution
    ↓
Target Environment
```

Execution is separate from preparation.

---

# 🏷 8. How Rules Are Classified

Rules are classified by **responsibility**, not by the Kubernetes field they inspect.

```text
                         RULE
                           │
                           ▼
                 What does it own?
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
         Change /       Detect         Detect
         improve        config        security
          state         problem         risk
             │             │             │
             ▼             ▼             ▼
         Optimizer      Validator      Security
```

The same field may legitimately be inspected by multiple engines.

Example:

```text
CPU Request
    │
    ├── Optimizer
    │      └── improves configuration
    │
    └── Validator
           └── detects undesirable configuration
```

The field does not determine ownership.

The responsibility does.

---

# 🔒 9. Current Mutation Model

Currently:

```text
Optimizer  → may mutate IR
Validator  → read-only
Security   → read-only
Renderer   → no preparation mutations
```

This is a **current architectural behavior**.

It is not a claim that Optimizer is permanently the only possible mutating engine.

Future engines may have different capabilities when they are explicitly designed and implemented.

---

# 🔮 10. Future Engines

TRL may eventually gain additional capabilities.

For example:

```text
                Future
                   │
       ┌───────────┼────────────┐
       ▼           ▼            ▼
    AutoFix   Relationship    AI
               Engine        Engine
```

These should be introduced as independent responsibilities.

For example:

```text
AutoFix
    → correction

Relationship Engine
    → cross-resource analysis

AI Engine
    → intelligent analysis / assistance
```

Future engines should not be forced into an existing engine simply because they happen to inspect the same Kubernetes fields.

---

# 🌐 11. Cross-Resource Intelligence

Current TRL analysis is resource-oriented.

Conceptually:

```text
Deployment → analyzed independently
Service    → analyzed independently
Ingress    → analyzed independently
```

TRL does not currently infer relationships between these resources.

A future Relationship Engine may introduce:

```text
Deployment
      │
      ├──── Service
      │
      └──── Ingress
```

This would allow TRL to reason about system-level relationships.

---

# 🤖 12. Future AutoFix

AutoFix is a possible future correction capability.

Conceptually:

```text
Validator / Security
        │
        ▼
      Finding
        │
        ▼
     AutoFix
        │
        ▼
   Corrected State
```

The important distinction is:

```text
Detection ≠ Correction
```

Validator and Security identify problems.

AutoFix, if implemented, would apply an explicit correction.

This keeps the responsibilities understandable.

---

# ☁️ 13. Environment Awareness

The TRL core should remain environment-agnostic.

Conceptually:

```text
Core Intelligence
       │
       ▼
Prepared State
       │
       ▼
Environment-specific processing
       │
       ▼
Execution
```

Cloud-specific behavior should not leak into the core Optimizer, Validator, or Security responsibilities.

Environment-specific adapters are a future extension.

---

# 🧠 14. The Most Important Distinction

There are four different concepts in TRL:

```text
RESPONSIBILITY
      │
      ▼
What does the engine own?


CAPABILITY
      │
      ▼
What may it currently do?


WORKFLOW
      │
      ▼
When does it run?


PHASE
      │
      ▼
How do we conceptually group the work?
```

For example:

```text
Preparation
    │
    ├── Optimizer
    ├── Validator
    └── Security

Workflow
    │
    ├── Optimizer
    ├── Validator
    └── Security

But:

Preparation ≠ Engine
Workflow ≠ Engine Dependency
```

---

# 🎯 15. TRL in One Diagram

```text
                         TRL
                          │
                          ▼
                         IR
                          │
                          ▼
              ┌───────────────────────┐
              │   PREPARATION PHASE   │
              │      (Conceptual)     │
              │                       │
              │  Optimizer            │
              │      ↓                │
              │  Validator            │
              │      ↓                │
              │  Security             │
              └──────────┬────────────┘
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
                Optional Execution
```

---

# 🚀 16. The TRL Mental Model

When thinking about TRL, remember:

```text
1. Engines own responsibilities.

2. Rules belong to engines according to responsibility.

3. Engines remain independently designed.

4. Workflow determines execution order.

5. Preparation is a conceptual phase.

6. Current implementation determines capabilities.

7. Future engines may introduce new responsibilities.

8. Rendering and execution are separate from preparation.
```

> **TRL separates responsibility, capability, workflow, and execution so that the system can grow without making its behavior difficult to understand.**