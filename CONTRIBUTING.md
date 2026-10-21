# 🤝 Contributing to TRL

Thanks for your interest in contributing 🚀

---

## 📌 Current Status

TRL is stabilizing its core architecture.
Contributions are welcome, but must follow strict design consistency.

---

## 🧪 Getting Started

```bash
pip install -r requirements.txt
python -m trl optimize ./examples/demo/bad.yaml --dry-run
```

---

## 🧱 Project Structure (Important)

* `trl/core/` → base classes, IR, reporting
* `trl/modules/` → engines (optimizer, validator, security)
* `trl/cli/` → CLI entry point
* `examples/` → test manifests

---

## 🧩 Rule Types (Important)

┌───────────────────────────────────────────────────────┐
│                 CONTRIBUTOR RULE                      │
├───────────────────────────────────────────────────────┤
│                                                       │
│  Classify a rule by its RESPONSIBILITY,               │
│  not by the field or condition it examines.           │
│                                                       │
│  OPTIMIZE / IMPROVE STATE  ──► Optimizer              │
│  DETECT CONFIGURATION      ──► Validator              │
│  DETECT SECURITY / POLICY  ──► Security               │
│  APPLY EXPLICIT CORRECTION ──► AutoFix (future)       │
│                                                       │
│  Mutation is a capability of the engine contract.     │
│  Workflow order is separate from engine ownership.    │
│                                                       │
└───────────────────────────────────────────────────────┘

TRL has **two types of rules**:

### 1. Read-only Rules

Used in:

* `validator`
* `security`

These rules:

* MUST NOT modify IR
* Only report issues

---

### 2. Mutating Rules

Used in:

* `optimizer`

These rules:

* ARE allowed to modify IR
* Must also report what was changed

---

## 🧩 How to Add a Rule

1. Choose engine:

* `validator` → correctness issues
* `security` → risks
* `optimizer` → improvements (can mutate IR)

2. Create a rule inside that module

3. Follow pattern:

```python
class ExampleRule(ValidationRule):

    name = "example-rule"
    category = "reliability"

    def match(self, ir):
        if some_condition:
            self.report.warning(
                resource=ir.name,
                issue="Problem description",
                impact="Why it matters",
                fix="How to fix it"
            )
```

---

## ⚙️ Reporting Rules (STRICT)

### Validation / Security

* MUST use:

  * issue
  * fix
* OPTIONAL:

  * impact

---

### Optimization

* MUST:

  * modify IR (if applicable)
  * provide a clear `message` describing the change

---

## 🚫 Avoid

* Cross-resource logic (for now)
* Hidden mutations outside optimizer
* Complex abstractions
* Dynamic rule loading
* Overengineering

---

## 🧠 Design Philosophy

* Simple > complex
* Explicit > implicit
* Clear output > smart tricks
* Modules must remain independent
* Prefer data flow over shared state
* Keep rules isolated and predictable

---

## 💬 Before Large Changes

Open an issue first to discuss your approach.

---

Keep it simple. Keep it clear.
