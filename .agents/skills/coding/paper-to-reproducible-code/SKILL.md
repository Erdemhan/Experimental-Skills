---
name: paper-to-reproducible-code
description: >
  Activate this skill when comparing paper tables/text with the codebase to prevent 
  parameter mismatch. This skill audits paper tables vs YAML/JSON configs, checks for 
  hidden hyperparameters, and ensures 1-to-1 fidelity between published tables and 
  run parameters.
---

# Paper To Reproducible Code Skill — Makale ↔ Kod Parametre Denetimi

## Temel Kural
> Makale metninde veya Tablo 1'de ve kilitli `.claude/context/FORMULATION.md` dosyasında yazan denklem/hiperparametreler ile `configs/*.yaml` ve Python fonksiyonları %100 örtüşmelidir.
> `FORMULATION.md` kullanıcı kilitlidir; çelişki varsa koddaki hata düzeltilir.

---

## Parametre Denetim Protokolü

```markdown
## Parametre Denetim Raporu — <Paper / Deney Adı>

### 1. Parametre Eşleşme Matrisi
| Parametre | Paper / Tablo Değeri | Code Config Değeri | Durum |
|-----------|----------------------|--------------------|-------|
| Learning Rate | 3e-4 (Tablo 2) | `lr: 0.0003` | ✅ Eşleşti |
| Discount Factor (γ) | 0.99 | `gamma: 0.99` | ✅ Eşleşti |
| GAE Lambda (λ) | 0.95 | `lambda: 0.95` | ✅ Eşleşti |
| Batch Size | 256 | `batch_size: 512` | ❌ UYUMSUZ |
| Target Update Freq | 1000 steps | `target_update: 500` | ❌ UYUMSUZ |
```

---

## Otomatik Uyum Denetim Scripti

```python
# scripts/audit_paper_params.py
import yaml
import json
import sys
from pathlib import Path

def audit_config(config_path: Path, expected_params: dict):
    """Compare yaml/json config against expected paper values."""
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    mismatches = []
    for key, expected_val in expected_params.items():
        actual_val = config.get(key)
        if actual_val != expected_val:
            mismatches.append((key, expected_val, actual_val))
    
    if mismatches:
        print(f"❌ Parametre Uyumsuzluğu ({config_path.name}):")
        for key, exp, act in mismatches:
            print(f"   - {key}: Beklenen={exp}, Koddaki={act}")
        return False
    
    print(f"✅ Tüm parametreler makale ile uyumlu: {config_path.name}")
    return True
```
