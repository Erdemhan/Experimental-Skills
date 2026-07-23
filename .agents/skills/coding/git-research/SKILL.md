---
name: git-research
description: >
  Activate this skill when managing Git repositories for academic research projects. 
  Enforces academic commit tags (exp:, data:, result:), paper/ paper-draft branching, 
  large model weight tracking (.gitignore), and commit-msg hooks.
---

# Git Research Skill — Academic Research Git Workflows

## Core Rule
> Model weights (.pt/.pth/.onnx) and raw datasets must NEVER be committed to Git.  
> Use `.claude/templates/.gitignore` and commit tags (`exp:`, `result:`, `paper:`) for research tracking.

---

## 1. Academic Commit Message Types

```
<type>(<scope>): <description>

BUG-IMPACT: [A / B / C / None]
FORMULATION-REF: [EQ-01 / None]
```

### Research Commit Types
- `exp`: Running or configuring an empirical experiment
- `result`: Updating experimental log tables, plots, or statistical metrics
- `paper`: Editing LaTeX sections, figures, or BibTeX files
- `model`: Model architecture adjustments (code only)
- `data`: Data pipeline or preprocessing script updates

---

## 2. Large Artifact Protection

Make sure `.gitignore` contains:
```gitignore
# Exclude model weights and datasets
*.pt
*.pth
*.onnx
*.npz
data/
results/logs/
context.db
```
