# 📚 TRL Documentation

Welcome to the TRL documentation hub.

TRL is a **pre-deployment intelligence system for Kubernetes** that analyzes, optimizes, validates, and prepares manifests before deployment.

This documentation explains how TRL is built, how it behaves, and how to use it.

---

# 🧭 Documentation Hierarchy

TRL documentation is organized into five core layers:

---

## 🧱 Structure

> How TRL is built

- [architecture.md](architecture.md)

Defines:
- system design
- pipeline flow
- engine responsibilities
- IR structure
- execution order

👉 This is the **technical blueprint**

---

## 🧠 Behavior

> How TRL works conceptually

- [system-model.md](system-model.md)

Defines:
- decision vs execution separation
- layered system design
- mental execution flow
- AutoFix (future) behavior model

👉 This is the **thinking model of TRL**

---

## 🔒 Rules

> What cannot break

- [guarantees.md](guarantees.md)

Defines:
- deterministic execution rules
- mutation constraints
- engine boundaries
- system safety guarantees

👉 This is the **trust contract of TRL**

---

## 🚀 Usage

> How to use TRL

- [../README.md](../README.md)

Defines:
- CLI usage
- examples
- features overview
- quick start guide

👉 This is the **user entry point**

---

## 🎯 Vision

> Where TRL is going

- [vision.md](vision.md)

Defines:
- product direction
- roadmap
- future layers (SaaS, adapters, intelligence)
- long-term goals

👉 This is the **future of TRL**

---

# 🧠 Design Philosophy

TRL documentation is designed to be:

- 📖 easy to navigate
- 🧩 clearly separated by responsibility
- 🧠 layered from concept → implementation
- 🔒 strict about system boundaries

---

# 🔁 How to Read TRL Docs

If you're new:

1. Start with `README.md` (usage)
2. Then `system-model.md` (behavior)
3. Then `architecture.md` (structure)
4. Then `guarantees.md` (rules)
5. Finally `vision.md` (future)

---

# 🎯 Summary

TRL is not just a tool.

It is a **structured decision system for Kubernetes deployments**.

This documentation exists to ensure:

> every contributor and user builds the same mental model of TRL