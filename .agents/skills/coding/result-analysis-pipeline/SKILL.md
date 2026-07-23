---
name: result-analysis-pipeline
description: >
  Activate this skill when processing raw experiment log files into statistical metrics, 
  generating publication-ready vector figures (PDF), and producing LaTeX table fragments.
---

# Result Analysis Pipeline Skill — Log-to-LaTeX Table & Figure Pipeline

## Core Rule
> Manual copy-pasting of experiment results into paper tables is forbidden.  
> Raw log parsing, statistical computation, PDF figure plotting, and TeX table generation must be automated.

---

## 1. Automated Analysis Pipeline Flow

```
[Raw Log Files (JSON/CSV/WandB)]
  │
  ├── 1. Parse Logs & Extract Multi-Seed Runs
  ├── 2. Compute Mean, 95% Confidence Intervals, & Welch's t-test (@statistical-validity)
  ├── 3. Plot Colorblind-Friendly PDF Figures (Seaborn / Matplotlib)
  └── 4. Export Publication LaTeX Table Fragment (`results/table_summary.tex`)
```

---

## 2. Publication-Ready LaTeX Table Generator

```python
import pandas as pd

def generate_latex_table(df_stats: pd.DataFrame, output_path: str):
    """Generate a clean booktabs LaTeX table from statistical DataFrame."""
    latex_str = df_stats.to_latex(
        index=False,
        column_format="lcccc",
        caption="Empirical benchmark performance across 5 random seeds.",
        label="tab:main_results",
        escape=False
    )
    with open(output_path, "w") as f:
        f.write(latex_str)
```
