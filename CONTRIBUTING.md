# 🤝 Contributing to TRL

Thanks for contributing to TRL.

TRL is designed to grow through small, isolated contributions while keeping the core architecture predictable.

The easiest way to contribute is to add or improve a **rule**.

However, contributions are not limited to rules. Bug fixes, tests, documentation, CLI improvements, and other improvements are welcome as well.

---

# 🧭 1. Understand TRL First

TRL is a pre-deployment intelligence system for Kubernetes.

At a high level:

```text
Kubernetes Input
       │
       ▼
      IR
       │
       ▼
┌─────────────────────────────┐
│      Preparation Phase      │
│                             │
│  Optimizer                 │
│       ↓                     │
│  Validator                 │
│       ↓                     │
│  Security                  │
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

**Preparation** is a conceptual phase, not a separate engine.

The engines remain independent modules.

---

# 🔌 2. Engine Independence

TRL engines are designed to be:

- self-contained
- independently testable
- replaceable
- responsible for their own logic
- usable within different workflows

Engine independence and workflow order are different concepts.

```text
ENGINE INDEPENDENCE

Optimizer     Validator     Security
    │             │             │
    └────── independent modules ──────┘


WORKFLOW

Input
  ↓
Optimizer
  ↓
Validator
  ↓
Security
  ↓
Renderer
```

The workflow determines **when** an engine runs.

Engine ownership determines **what responsibility** that engine has.

---

# 🧩 3. Current Contribution Areas

Contributions currently fall into several categories.

### 🟢 Rules — Primary Extension Surface

Most contributors should start here.

```text
Rule
 │
 ├── inspect resource
 ├── evaluate condition
 └── produce result
```

Rules should remain:

- focused
- deterministic
- isolated
- independently testable
- easy to understand

---

### 🟢 Tests

Tests are always welcome.

Examples:

- rule tests
- regression tests
- parser tests
- renderer tests
- CLI tests
- integration tests

A bug fix should normally include a regression test when practical.

---

### 🟢 Documentation

Documentation improvements are valuable contributions.

Examples:

- fixing unclear explanations
- adding examples
- improving diagrams
- correcting inaccurate documentation
- documenting new behavior

---

### 🟢 Bug Fixes

Bug fixes are welcome when they preserve the existing architectural boundaries.

When possible:

```text
Bug
 ↓
Reproduce
 ↓
Test
 ↓
Fix
 ↓
Regression test
```

---

### 🟢 CLI and Reporting

Contributions to:

- CLI usability
- error messages
- human-readable reports
- JSON output
- YAML output
- command behavior

are also valid contribution areas.

---

# 🧠 4. Choosing the Correct Engine

When adding a rule, do not classify it by the Kubernetes field it examines.

Classify it by its **responsibility**.

```text
                    New Rule
                       │
                       ▼
              What does it do?
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   Improve /        Detect          Detect
   change state     configuration   security /
                    problem         policy risk
        │              │              │
        ▼              ▼              ▼
    Optimizer       Validator       Security
```

### Contributor Rule

```text
┌─────────────────────────────────────────────────────┐
│                  CONTRIBUTOR RULE                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Do not classify a rule by the field it examines.  │
│                                                     │
│  Classify it by the responsibility it owns:        │
│                                                     │
│  CHANGE / IMPROVE STATE ───► Optimizer             │
│  DETECT CONFIGURATION ─────► Validator             │
│  DETECT SECURITY / POLICY ─► Security              │
│                                                     │
│  The same field may be examined by multiple       │
│  engines when their responsibilities differ.       │
│                                                     │
│  Workflow order is separate from engine ownership.│
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# 🔧 5. Optimizer Rules

Use the Optimizer when the rule is responsible for changing or improving deployment state.

Current Optimizer rules may mutate IR.

```text
Input State
     │
     ▼
Optimizer Rule
     │
     ▼
Decision
     │
     ▼
Changed IR
```

If a rule mutates IR, the mutation must be explicitly reported.

Reports should make clear:

```text
Before → After
```

---

# ⚠️ 6. Validator Rules

Use Validator when the rule detects a configuration problem.

```text
Input State
     │
     ▼
Validator Rule
     │
     ▼
Finding
```

Validator rules:

- inspect
- evaluate
- report

They do not modify IR.

A Validator may recommend a fix.

It does not apply that fix.

---

# 🔐 7. Security Rules

Use Security when the rule detects a security or policy risk.

```text
Input State
     │
     ▼
Security Rule
     │
     ▼
Security Finding
```

Security rules:

- inspect
- evaluate
- report

They do not modify IR.

---

# 🔄 8. Workflow Is Not Ownership

The default workflow is currently:

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
```

This does not mean:

```text
Validator depends on Optimizer implementation
Security depends on Validator implementation
```

It means that later stages receive the state produced by earlier stages.

The modules themselves remain independently defined.

---

# 🔒 9. Current Mutation Boundary

Current behavior:

```text
Optimizer  → may mutate IR
Validator  → read-only
Security   → read-only
Renderer   → does not perform preparation mutations
```

These are current architectural boundaries.

They are documented and maintained through:

- implementation
- tests
- rule design
- contributor conventions

TRL does not currently have a separate runtime "contract authority" that grants mutation permission.

If a future engine requires mutation, its responsibility and mutation behavior must be explicitly defined when that engine is introduced.

---

# 🧱 10. Rules Should Be Independent

A rule should not:

- depend on another rule's internal state
- silently modify shared state
- call another rule directly
- assume another rule has already run
- create hidden side effects

Prefer:

```text
Engine
 │
 ├── Rule A
 ├── Rule B
 ├── Rule C
 └── Rule D
```

rather than:

```text
Rule A
  ↓
Rule B
  ↓
Rule C
```

Rule composition belongs to the workflow, not hidden inside individual rules.

---

# 🧪 11. Rule Checklist

Before submitting a rule:

```text
□ Is the responsibility clearly defined?

□ Is the rule in the correct engine?

□ Does it avoid hidden state?

□ Does it avoid depending on another rule?

□ Is it deterministic?

□ Does it have tests?

□ Does it produce a clear result?

□ If it mutates IR, is the mutation explicitly reported?

□ Does it preserve the engine's current boundary?
```

---

# 🏗 12. Changes to Engines or Architecture

Adding a normal rule is different from changing the architecture.

Before proposing:

- a new engine
- a new workflow stage
- a new mutation capability
- a new IR structure
- cross-resource analysis
- cloud/environment-specific behavior
- a plugin-loading system
- an AI engine
- AutoFix architecture

discuss the design first.

These changes can affect multiple parts of TRL.

A useful distinction is:

```text
RULE CHANGE

One responsibility
      ↓
One engine
      ↓
Usually localized


ARCHITECTURAL CHANGE

New capability
      ↓
Multiple components
      ↓
Workflow / IR / documentation
may be affected
```

This does not mean architectural contributions are prohibited.

It means they should be designed deliberately before implementation.

---

# 🔮 13. Future Extension Points

TRL may eventually support capabilities such as:

```text
AutoFix
Relationship Engine
Cloud Adapters
AI-based Intelligence
Dynamic Engine / Plugin Loading
```

These are architectural directions, not necessarily current contributor contracts.

When they become implemented extension points, their contribution rules should be documented separately.

---

# 📋 14. What Should I Contribute?

If you are new to TRL:

```text
Start here
    │
    ▼
Add / improve a rule
    │
    ▼
Add tests
    │
    ▼
Improve documentation
```

If your proposal changes the architecture:

```text
Idea
  ↓
Explain responsibility
  ↓
Explain workflow impact
  ↓
Explain IR impact
  ↓
Discuss architecture
  ↓
Implement
```

---

# 🎯 15. The Main Principle

TRL should remain easy to extend without becoming difficult to understand.

The goal is:

> **Many independent rules, clear engine responsibilities, predictable behavior, and deliberate architectural growth.**

When contributing, always ask:

```text
What responsibility does this change own?

What state does it read?

What state does it change?

Which engine should own it?

Does it introduce a new architectural dependency?
```

If those answers are clear, the contribution is likely in the right place.
