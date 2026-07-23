---
name: ml-experiment
description: >
  Activate this skill when setting up a machine learning experiment, training a 
  model, designing an evaluation pipeline, or running ablation studies. This skill 
  enforces reproducible ML setups: fixed seeds, proper train/val/test splits, 
  baseline comparisons, and systematic logging with experiment tracking.
---

# ML Experiment Skill — Makine Öğrenmesi Deneyi

## Temel Kural
> Ölçmeden iyileştirme olmaz. Kayıt etmeden tekrarlama olmaz.

---

## ML Deney Kurulum Kontrol Listesi

### 1. Tekrarlanabilirlik Kurulumu (Zorunlu)
```python
import random
import numpy as np
import torch
import os

def set_seed(seed: int = 42) -> None:
    """Fix all random seeds for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    
    # Deterministic ops (yavaşlatır ama tekrarlanabilir)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed(42)  # Her deneyin başında
```

### 2. Veri Ayrışımı (Data Split)
```python
from sklearn.model_selection import train_test_split, StratifiedKFold

# Standart split (sınıf dengesi korunarak)
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
)
# Sonuç: %70 train, %15 val, %15 test

# ⚠️ Test seti modeli hiç görmemeli — yalnızca final raporlama için
```

### 3. Baseline Tanımlama
Her deneyde baseline zorunludur:
- **Random baseline**: Rastgele tahmin → ne kadar kolay?
- **Majority class baseline**: Hep çoğunluk sınıfı → şansa karşı ne kadar iyi?
- **Previous SOTA**: Alandan en iyi bilinen sonuç

### 4. Konfigürasyon Yönetimi
```yaml
# configs/experiment.yaml
experiment:
  name: "bert_turkish_sentiment_v1"
  seed: 42
  
model:
  name: "bert-base-turkish-cased"
  hidden_size: 768
  dropout: 0.1
  
training:
  epochs: 10
  batch_size: 32
  learning_rate: 2e-5
  warmup_steps: 500
  
data:
  dataset: "turkish_sentiment_v2"
  max_length: 128
  train_split: 0.70
  val_split: 0.15
  test_split: 0.15
```

---

## Deney Takip Sistemi (Experiment Tracking)

### MLflow ile (Önerilen)
```python
import mlflow

with mlflow.start_run(run_name="bert_v1_seed42"):
    # Parametreleri logla
    mlflow.log_params({
        "model": "bert-base-turkish-cased",
        "lr": 2e-5,
        "batch_size": 32,
        "seed": 42,
    })
    
    # Her epoch metriklerini logla
    for epoch in range(num_epochs):
        train_loss, val_f1 = train_epoch(...)
        mlflow.log_metrics({
            "train_loss": train_loss,
            "val_f1": val_f1,
        }, step=epoch)
    
    # Model ve artifact'leri kaydet
    mlflow.pytorch.log_model(model, "model")
    mlflow.log_artifact("configs/experiment.yaml")
```

---

## Ablation Çalışması Tasarımı

Ablation: Bileşenlerin katkısını ölçme

```python
experiments = [
    {"name": "full_model",        "use_pretrain": True,  "use_augment": True},
    {"name": "no_pretrain",       "use_pretrain": False, "use_augment": True},
    {"name": "no_augment",        "use_pretrain": True,  "use_augment": False},
    {"name": "baseline",          "use_pretrain": False, "use_augment": False},
]

# Her kombinasyonu aynı koşulda çalıştır (same seed, same split, same hardware)
```

Ablation tablosu formatı:
```
| Konfigürasyon      | Accuracy | F1    | ΔF1 (full'a göre) |
|--------------------|----------|-------|-------------------|
| Full Model         | 0.923    | 0.918 | —                 |
| w/o Pre-training   | 0.891    | 0.884 | -0.034            |
| w/o Augmentation   | 0.910    | 0.905 | -0.013            |
| Baseline           | 0.867    | 0.861 | -0.057            |
```

---

## Değerlendirme Metrikleri Seçim Rehberi

| Problem Tipi | Birincil Metrik | İkincil Metrikler |
|---|---|---|
| İkili sınıflandırma (dengeli) | Accuracy | F1, AUC-ROC |
| İkili sınıflandırma (dengesiz) | F1-Macro | AUC-ROC, PR-AUC |
| Çok sınıflı | F1-Macro | Accuracy, Confusion Matrix |
| Regresyon | RMSE | MAE, R² |
| Sıralama | NDCG@K | MAP, MRR |
| Nesne tespiti | mAP | IoU |
| Metin üretimi | BLEU/ROUGE | BERTScore, human eval |

---

## Raporlama Standardı

```
Deney ID: exp_20260723_142300
Model: bert-base-turkish-cased
Seed: 42 (5 çalıştırma: 42, 123, 456, 789, 1024)
Donanım: NVIDIA RTX 4090, CUDA 12.1
Veri: turkish_sentiment_v2 (N=50,000)

Sonuçlar (Test Seti, N=5 çalıştırma ortalaması ± std):
  Accuracy: 0.923 ± 0.004
  F1-Macro: 0.918 ± 0.005
  F1-Micro: 0.923 ± 0.004
  AUC-ROC:  0.971 ± 0.002

Random Baseline: Accuracy = 0.333, F1-Macro = 0.333
Majority Baseline: Accuracy = 0.521, F1-Macro = 0.228
```
