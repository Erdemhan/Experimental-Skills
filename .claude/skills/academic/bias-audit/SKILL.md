---
name: bias-audit
description: >
  Activate this skill when evaluating datasets, model metrics, or experimental 
  results for selection bias, evaluation bias, data leakage, and selective metric reporting.
---

# Bias Audit Skill — Bias Evaluation & Data Integrity Audit

## Core Rule
> Unexamined datasets and selective metric evaluations produce invalid scientific conclusions.

---

## 1. Bias Check Categories

1. **Selection Bias**: Ensure dataset distributions match real-world deployment scenarios.
2. **Selective Reporting**: Verify that all evaluated metrics (mean, median, min, max, std) are reported across all algorithms.
3. **Data Leakage**: Confirm preprocessing scaling factors (mean/std) are calculated strictly on training folds.
