---
name: self-consistency-verifier
description: >
  Activate this skill for post-implementation audit and self-correction. 
  Enforces an independent critique loop between the generator agent and 
  verifier agent to detect hidden edge cases, logic flaws, and specification drift.
---

# Self-Consistency Verifier Skill — Cross-Agent Critique & Self-Correction

## Core Rules

1. **Critique Isolation**:
   - The verifying agent MUST act as an independent reviewer, questioning assumptions made by the generator agent.

2. **Edge-Case & Boundary Audit**:
   - Test for zero-values, NaN/Inf bounds, empty lists, out-of-bounds array indices, and network disconnection states before declaring implementation `Done`.

3. **Self-Correction Protocol**:
   - If the verifier detects a logic flaw or spec mismatch, execution returns to `@worker-coder` with an explicit critique report before requesting user sign-off.

---

## Verification Audit Matrix

| Category | Check Item | Action on Failure |
|---|---|---|
| Contract | Does output type match `FunctionSpec` exact type hints? | Reject code, re-specify |
| Boundary | Are 0, None, NaN, Inf handling verified? | Add boundary guard clause |
| Concurrency | Are thread synchronization / lock leaks audited? | Enforce explicit lock release |
