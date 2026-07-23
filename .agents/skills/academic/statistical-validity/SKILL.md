---
name: statistical-validity
description: >
  Activate this skill when evaluating numerical results, comparing baseline performance, 
  computing confidence intervals, performing hypothesis testing (Welch's t-test / Mann-Whitney U), 
  and reporting Cohen's d effect sizes.
---

# Statistical Validity Skill — Statistical Testing & Effect Size Analysis

## Core Rule
> Raw mean values without confidence intervals or p-values are statistically meaningless.

---

## 1. Statistical Analysis Pipeline

```python
import numpy as np
from scipy import stats

def compute_academic_stats(sample_a: list, sample_b: list):
    """Compute 95% Confidence Intervals, Welch's t-test, and Cohen's d."""
    a, b = np.array(sample_a), np.array(sample_b)
    
    # 1. 95% Confidence Interval
    ci_a = stats.t.interval(0.95, len(a)-1, loc=np.mean(a), scale=stats.sem(a))
    ci_b = stats.t.interval(0.95, len(b)-1, loc=np.mean(b), scale=stats.sem(b))
    
    # 2. Welch's t-test (unequal variances)
    t_stat, p_val = stats.ttest_ind(a, b, equal_var=False)
    
    # 3. Cohen's d Effect Size
    pooled_std = np.sqrt((np.std(a, ddof=1)**2 + np.std(b, ddof=1)**2) / 2)
    cohens_d = (np.mean(a) - np.mean(b)) / pooled_std
    
    return {
        "mean_a": np.mean(a), "ci_95_a": ci_a,
        "mean_b": np.mean(b), "ci_95_b": ci_b,
        "p_value": p_val, "cohens_d": cohens_d
    }
```
