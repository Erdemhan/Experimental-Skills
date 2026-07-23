---
name: auto-adr-generator
description: >
  Activate this skill when major architectural decisions are made (e.g. choosing 
  an RL framework, database schema, or API structure). Automatically generates 
  MADR-compliant Architecture Decision Records in `docs/adr/`.
---

# Auto-ADR Generator Skill — Architecture Decision Records

## Core Rule
> Every major architectural decision MUST be documented in `docs/adr/XXXX-title.md`.  
> Decisions MUST state Context, Decision Drivers, Considered Options, and Consequences.

---

## 1. MADR Template (Markdown Architectural Decision Records)

```markdown
# [ADR-0001] Choice of Reinforcement Learning Environment & Framework

* **Status:** Accepted
* **Deciders:** `@architect`, User
* **Date:** 2026-07-23

## Context and Problem Statement
We need a standardized RL environment interface supporting single-agent and multi-agent experiments.

## Decision Drivers
* Compliance with Gymnasium / PettingZoo standards
* PyTorch ecosystem compatibility
* Multi-seed reproducibility requirements

## Considered Options
1. Legacy Gym API
2. Gymnasium & PettingZoo API
3. Custom ad-hoc RL loop

## Decision Outcome
Chosen Option: **Option 2 (Gymnasium & PettingZoo API)** because it provides active maintenance, strict space definitions, and seamless Ray Tune integration.

### Positive Consequences
* Long-term API stability and no deprecation warnings.
* Direct compatibility with `@experiment-runner` 5-seed benchmark scripts.

### Negative Consequences
* Requires wrapping legacy Gym environments with `gymnasium.make()`.
```
