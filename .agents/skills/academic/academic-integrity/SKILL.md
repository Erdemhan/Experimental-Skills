---
name: academic-integrity
description: >
  Activate this skill when evaluating academic claims, checking citations, verifying 
  references, or ensuring scientific integrity. Enforces strict rules against unreferenced 
  claims, hallucinated citations, selective reporting, and unfair baselines.
---

# Academic Integrity Skill — Scientific Rigor & Citation Verification

## Core Rule
> Every factual claim must be backed by a verified reference.  
> Unreferenced assertions, hallucinated citations, or unverified claims are strictly forbidden.

---

## 1. Citation & Claim Audit Rules

### A. Unreferenced Claim Prevention
- Any statement claiming performance, theoretical bounds, or empirical facts MUST include a reference.
- **Incorrect**: "PPO is the most stable RL algorithm for continuous control."
- **Correct**: "PPO is widely used for continuous control due to its clipped surrogate objective (Schulman et al., 2017)."

### B. Anti-Hallucination Citation Verification Protocol
- Before citing a paper, verify its existence via DOI, Google Scholar, or ArXiv ID.
- Do NOT fabricate authors, publication venues, or publication years.

---

## 2. Scientific Honesty Guidelines

1. **Selective Reporting Prohibited**: Do NOT omit seeds, baseline runs, or metrics that show poor performance.
2. **Fair Baseline Comparison**: Baseline algorithms MUST be run with identical computational budgets (steps/GPUs) and equal hyperparameter tuning.
3. **Data Leakage Prohibition**: Test set inputs MUST NEVER be used during training, hyperparameter search, or feature scaling.
