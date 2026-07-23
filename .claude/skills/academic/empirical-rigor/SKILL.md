---
name: empirical-rigor
description: >
  Activate this skill when designing, executing, or auditing empirical experiments 
  (especially RL, ML, and simulation benchmarks). Enforces minimum 5-seed evaluation, 
  environment metadata logging, hyperparameter freezing, and reproducibility standards.
---

# Empirical Rigor Skill — Experimental Standards & Reproducibility

## Core Rule
> Single-seed or unseeded experiments are scientifically invalid.  
> Every empirical result reported must be evaluated over at least 5 random seeds with logged environment metadata.

---

## 1. Experimental Standards Checklist

1. **Multi-Seed Rule**: Minimum 5 random seeds (`seed: [42, 43, 44, 45, 46]`) required for all RL and stochastic training runs.
2. **Environment Metadata Logging**: Automatically log execution environment details to `results/<exp_name>/env_metadata.json`:
   - System details: OS platform, Python version, PyTorch version, CUDA version, GPU model, CPU model, `pip freeze`.
3. **Hyperparameter Freezing**: Freeze hyperparameters across all random seeds during benchmark runs.
4. **Determinism Controls**: Set deterministic flags for PyTorch and NumPy:
   ```python
   import random, torch, numpy as np
   def set_seed(seed: int):
       random.seed(seed)
       np.random.seed(seed)
       torch.manual_seed(seed)
       torch.cuda.manual_seed_all(seed)
       torch.backends.cudnn.deterministic = True
   ```
