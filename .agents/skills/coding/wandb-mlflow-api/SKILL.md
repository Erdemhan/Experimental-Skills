---
name: wandb-mlflow-api
description: >
  Activate this skill when programmatically querying, fetching, or analyzing 
  training runs from Weights & Biases (WandB) or MLflow APIs. Converts cloud 
  experiment logs into Pandas DataFrames for statistical analysis and plotting.
---

# WandB & MLflow API Skill — Programatik Deney Sorgulama

## Temel Kural
> Manuel ekran görüntüsü veya WandB UI kopyalama yok.  
> Tüm deney verileri WandB/MLflow API ile programatik olarak çekilmeli ve saklanmalıdır.

---

## 1. WandB API ile Run Çekme

```python
import wandb
import pandas as pd
from pathlib import Path

def fetch_wandb_runs(entity: str, project: str) -> pd.DataFrame:
    """Fetch all completed runs from a WandB project into a DataFrame."""
    api = wandb.Api()
    runs = api.runs(f"{entity}/{project}")

    summary_list = []
    config_list = []
    name_list = []

    for run in runs:
        if run.state == "finished":
            # Summary metrics
            summary_list.append(run.summary._json_dict)
            # Config / Hyperparameters
            config_list.append({k: v for k, v in run.config.items() if not k.startswith("_")})
            name_list.append(run.name)

    df_summary = pd.DataFrame(summary_list)
    df_config = pd.DataFrame(config_list)
    df_summary["run_name"] = name_list

    df_full = pd.concat([df_summary, df_config], axis=1)
    return df_full
```

---

## 2. MLflow Tracking API ile Metric Çekme

```python
import mlflow
import pandas as pd

def fetch_mlflow_experiment(experiment_name: str) -> pd.DataFrame:
    """Fetch runs from an MLflow experiment."""
    exp = mlflow.get_experiment_by_name(experiment_name)
    if not exp:
        raise ValueError(f"Experiment {experiment_name} not found")

    runs = mlflow.search_runs(experiment_ids=[exp.experiment_id])
    return runs
```
