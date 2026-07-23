---
name: research-debug
description: >
  Activate this skill when debugging code in an academic research project — 
  especially RL experiments, simulation pipelines, or any code whose output 
  was or will be reported in a paper. This skill MUST run before debug-tracer 
  in research contexts. It classifies the bug by academic impact, decides 
  whether previous results remain valid, and ensures any fix preserves 
  experimental integrity.
---

# Research Debug Skill — Debugging in Research Contexts

## Core Rule
> Debugging in research code must answer two questions simultaneously:  
> (1) Is it technically correct?  
> (2) Does it invalidate previously reported academic claims or results?

---

## Step 0 — Bug & Fix Classification (Before Any Code Edit)

Before making any code modifications or applying bug fixes, answer these 4 questions:

```
BUG & FIX INTEGRITY AUDIT
══════════════════════════════════════════════════════════

❓ 1. DOES THE FIX / BUG VIOLATE ACADEMIC INTEGRITY?
   • Does the fix introduce data leakage?
   • Are test set inputs bleeding into training/debug pipelines?
   • Is the bug caused by local dev machine vs. server/cluster (Windows vs. Linux, CUDA ver, CPU cores) environment differences?
   • Are theoretical assumptions from cited papers being violated?
   → If YES: STOP! Academic integrity violation. Run @academic-integrity first.

❓ 2. DOES THE FIX DISTORT EXPERIMENTAL GOALS? (Goal Distortion)
   • Does the fix change the research question being tested (hypothesis-framing)?
   • Does it alter baseline comparison equality (fair-comparison)?
   → If YES: STOP! Consult user before changing code.

❓ 3. BUG IMPACT CLASSIFICATION
   ├── TYPE A (Isolated Software Bug): Does not affect experimental metrics (e.g. logging format, UI display, CLI typo).
   │     └─ Action: Fix safely, run unit tests.
   │
   ├── TYPE B (Result-Altering Bug): Alters numerical outputs, rewards, or metrics of reported experiments.
   │     └─ Action: Mark previous run logs as INVALID. Tag git commit with `BUG-IMPACT: B`. Schedule re-run.
   │
   └── TYPE C (Methodology-Breaking Bug): Violates paper pseudocode or theoretical formulation (FORMULATION.md).
         └─ Action: STOP IMMEDIATELY! Notify user. Requires re-formulation & full re-evaluation.

❓ 4. EMPIRICAL EVIDENCE CHECK
   • Has the bug been verified with full log files, tracebacks, or pytest outputs?
   → If NO: STOP! Empirical evidence required before making code changes.
```
