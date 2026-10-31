# 📚 TRL Documentation

Welcome to the TRL documentation.

TRL is a **pre-deployment decision system for Kubernetes**. It analyzes Kubernetes resources before they reach a target environment and helps users understand:

- what is wrong
- what can be improved
- what is risky
- what TRL changed
- what the resulting configuration looks like

TRL is designed to keep these responsibilities separate while allowing its engines to evolve independently.

---

# 🧭 Start Here

If you are new to TRL, read the documentation in this order:

```text
                         ┌───────────────┐
                         │   docs/README │
                         │  Start Here   │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ System Model  │
                         │ How to think  │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ Architecture  │
                         │ How it's built│
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │  Guarantees   │
                         │ What must hold│
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ CONTRIBUTING  │
                         │ How to extend │
                         └───────────────┘
```

### Quick guide

| You want to understand... | Read |
|---|---|
| What TRL is | [README.md](./README.md) |
| How to think about TRL | [system-model.md](./system-model.md) |
| How engines and IR fit together | [architecture.md](./architecture.md) |
| What behavior must remain stable | [guarantees.md](./guarantees.md) |
| How to contribute | [CONTRIBUTING.md](../CONTRIBUTING.md) |
| Project direction | [vision.md](./vision.md) |
| CLI Reference | [usage.md](./usage.md) |

| How remote engines are invoked and composed | [remote-engines.md](./remote-engines.md) |

---

# 🧠 The TRL Mental Model

At the highest level:

```text
Kubernetes Input
       │
       ▼
      IR
       │
       ▼
┌─────────────────────────────┐
│      PREPARATION PHASE      │
│                             │
│  Optimizer                 │
│      ↓                      │
│  Validator                 │
│      ↓                      │
│  Security                  │
│                             │
│  Conceptual grouping       │
└──────────────┬──────────────┘
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

### Important

**Preparation is a conceptual phase, not an engine.**

There is no central "Preparation Engine".

The Optimizer, Validator, and Security engines remain independent modules with their own responsibilities.

---

# 🔌 Independent Engines, Composable Workflow

This distinction is important.

```text
ENGINE INDEPENDENCE

┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  Optimizer  │   │  Validator  │   │  Security   │
└─────────────┘   └─────────────┘   └─────────────┘
      Independent modules
             │
             ▼
      Composable workflow
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
Output
  ↓
Optional Execution
```

The order describes **workflow composition**.

It does not mean:

```text
Validator depends on Optimizer implementation
Security depends on Validator implementation
```

Instead:

> **Engine independence defines ownership. Workflow defines order.**

This distinction is central to TRL's architecture.

---

# 🌐 Remote Engine Composition

TRL includes an experimental example of composing engines that run in
separate processes.

The current example uses HTTP clients to invoke remote Optimizer,
Validator, and Security engines. A local workflow definition determines
the sequence, and a local Renderer handles the final output.

```text
Input Manifest
      │
      ▼
     IR
      │
      ▼
Remote Optimizer
      │
      ▼
Remote Validator
      │
      ▼
Remote Security
      │
      ▼
Local Renderer
      │
      ▼
    Output

This demonstrates that workflow composition does not require every
engine to execute inside the same process.

The current implementation uses a static JSON registry and HTTP
endpoints. It does not yet provide automatic discovery, dynamic
registration, engine uploads, or production-grade remote execution.

---

# 🧩 Engine Responsibilities

TRL classifies engines by **responsibility**, not simply by the Kubernetes field they inspect.

```text
                         RULE / ENGINE
                              │
                              ▼
                     What is it responsible for?
                              │
              ┌───────────────┼────────────────┐
              │               │                │
              ▼               ▼                ▼
       Change / improve   Detect config   Detect security /
            state            problem        policy risk
              │               │                │
              ▼               ▼                ▼
          Optimizer        Validator         Security
```

## Optimizer

Responsible for:

> **Improving or preparing the deployment state.**

Current behavior:

```text
State
  ↓
Optimizer
  ↓
Modified State
```

Optimizer rules may mutate IR.

Mutations must be explicitly reported.

---

## Validator

Responsible for:

> **Detecting and reporting configuration problems.**

```text
State
  ↓
Validator
  ↓
Finding
```

Validator rules are read-only.

They may recommend a fix, but they do not apply it.

---

## Security

Responsible for:

> **Detecting security and policy risks.**

```text
State
  ↓
Security
  ↓
Security Finding
```

Security rules are read-only.

They may provide remediation guidance, but they do not apply the remediation.

---

## Renderer

Responsible for:

> **Turning the prepared state into the requested output representation.**

```text
Prepared IR
     ↓
 Renderer
     ↓
Output
```

Renderer does not decide whether something should be optimized, validated, or secured.

---

## Optional Execution

Execution is separate from preparation.

Conceptually:

```text
Prepared Output
      ↓
Optional Execution
      ↓
Target Environment
```

The execution component operates on the final prepared representation rather than deciding how the state should have been prepared.

---

# 🏷️ How Rules Are Classified

A rule should **not** be classified simply because it examines a particular field.

For example:

```text
CPU Request
   │
   ├── Optimizer
   │      └── improve / establish configuration
   │
   └── Validator
          └── detect an undesirable configuration
```

Both can be valid.

The important question is:

> **What responsibility does the rule own?**

Use:

```text
CHANGE / IMPROVE STATE
        ↓
    Optimizer


DETECT CONFIGURATION PROBLEM
        ↓
    Validator


DETECT SECURITY / POLICY RISK
        ↓
     Security
```

This becomes especially important as TRL grows to hundreds or thousands of rules.

---

# 🔄 State Flow

The default workflow passes the resulting IR forward:

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

The important distinction is:

> The workflow passes state between engines; it does not make their implementations dependent on one another.

---

# 📊 Reporting and Output

TRL can present results in different formats without changing engine responsibilities.

Current reporting/output modes include:

```text
                 TRL Results
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
         CLI         JSON        YAML
     Human view   Machine data  Manifest
```

### CLI

Human-readable output for developers.

### JSON

Machine-readable output useful for automation and CI/CD.

### YAML

Manifest output representing the resulting deployment state.

The output format does **not** determine which engine owns a rule.

For example:

```text
Optimizer
   │
   ├── CLI report
   ├── JSON report
   └── YAML state
```

The engine responsibility remains the same.

---

# 🔒 Current Mutation Model

The current architecture has a simple mutation boundary:

```text
Optimizer  → may mutate IR
Validator  → read-only
Security   → read-only
Renderer   → no preparation mutations
```

This is a **current architectural behavior**.

It should not be interpreted as a permanent rule that no future engine may ever mutate state.

If a future engine introduces mutation, its responsibility and mutation behavior must be explicitly defined when that capability is implemented.

---

# 🧱 IR

The Intermediate Representation (IR) provides the common structure used by TRL engines.

Conceptually:

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
        │
        ▼
   Prepared IR
        │
        ▼
    Renderer
```

The IR helps separate:

- input handling
- Kubernetes resource representation
- rule logic
- output generation

This allows engines to operate on a common representation without knowing how the original input was loaded.

For implementation details, see [architecture.md](./architecture.md).

---

# 🧪 Predictable Behavior

TRL is designed around:

```text
Same input
    ↓
Same decisions
    ↓
Predictable result
```

The system aims to maintain:

- deterministic rule behavior
- isolated rules
- explicit mutations
- clear engine responsibilities
- predictable workflow composition
- transparent reporting

These are behavioral guarantees, not claims that every future engine must have exactly the same implementation.

See [guarantees.md](./guarantees.md) for the formal behavioral guarantees.

---

# 🧩 Contribution Model

TRL is designed to grow through independent contributions.

The easiest contribution path today is:

```text
Idea
  ↓
Rule
  ↓
Test
  ↓
Report
  ↓
Pull Request
```

Contributors should classify rules by responsibility:

```text
Change state       → Optimizer
Detect problem     → Validator
Security / policy  → Security
```

Rules should remain:

- isolated
- deterministic
- independently testable
- free from hidden shared state
- free from cross-rule dependencies

Architecture changes are different from normal rule contributions.

New engines, new mutation capabilities, IR changes, workflow changes, or future plugin mechanisms should be discussed before implementation.

See [CONTRIBUTING.md](../CONTRIBUTING.md).

---

# 🔮 Future Capabilities

TRL may eventually support additional capabilities such as:

```text
                    Future
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
     AutoFix    Relationship      AI
                  Engine
```

Other possible extensions may include:

```text
Cloud Adapters
Cost Intelligence
Multi-orchestrator support
Plugin / dynamic engine loading
```

These are **future architectural directions**, not claims that these capabilities currently exist.

A future engine should define its own responsibility rather than being forced into an existing engine merely because it examines similar data.

---

# 📖 Documentation Map

| Document | Purpose |
|---|---|
| [system-model.md](./system-model.md) | Mental model and system behavior |
| [architecture.md](./architecture.md) | Technical architecture and module structure |
| [guarantees.md](./guarantees.md) | Non-negotiable behavioral guarantees |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | How to contribute safely |
| [vision.md](./vision.md) | Long-term project direction |
| [remote-engines.md](./remote-engines.md) | Remote engine invocation and workflow composition example |
---

# 🎯 In One Picture

```text
                         TRL
                          │
                          ▼
                    Kubernetes Input
                          │
                          ▼
                         IR
                          │
                          ▼
              ┌──────────────────────┐
              │   PREPARATION PHASE  │
              │                      │
              │  Optimizer           │
              │      ↓               │
              │  Validator           │
              │      ↓               │
              │  Security            │
              │                      │
              │  Independent engines │
              └──────────┬───────────┘
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

## The Core Idea

TRL separates four things:

```text
RESPONSIBILITY
     ↓
Who owns the decision?


CAPABILITY
     ↓
What may the engine currently do?


WORKFLOW
     ↓
When does the engine run?


EXECUTION
     ↓
How is the prepared result delivered?
```

Keeping these concepts separate allows TRL to grow without making the system harder to understand.

> **TRL makes deployment decisions visible, predictable, and understandable before they reach the target environment.**