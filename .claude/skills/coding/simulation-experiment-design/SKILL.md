---
name: simulation-experiment-design
description: >
  Activate this skill when designing a simulation-based experiment for academic 
  research. Bridges scientific experimental design (control variables, statistical 
  power, confounds) with simulation-specific implementation concerns (simulator 
  non-determinism, environment variants, wall-clock budget planning). Use before 
  writing any simulation code.
---

# Simulation Experiment Design Skill — Simülasyon Deneyi Tasarımı

## Temel Kural
> Simülasyon ucuz olduğu için fazla deney yapmak cazip gelir.  
> Ama plansız çok sayıda deney, hata düzeltmesi yapılmamış çok sayıda sonuç üretir.

---

## Deney Tasarım Formu (Her Deneyden Önce Doldur)

```markdown
## Deney Tasarım Belgesi — <Deney Adı>

**Tarih**: YYYY-MM-DD
**Araştırmacı**: 
**Bağlı Araştırma Sorusu**: <hypothesis-framing skill'inden gelen RQ>

### 1. Amaç
Bu deney hangi soruyu cevaplayacak?
→ [Bir cümle]

### 2. Bağımsız Değişkenler (Manipüle Edilenler)
| Değişken      | Değerler                  | Neden bu değerler? |
|---------------|---------------------------|-------------------|
| Ödül şekli    | baseline, potential, dense | Ablation          |
| Öğrenme oranı | 1e-4, 3e-4, 1e-3          | Grid search       |

### 3. Bağımlı Değişkenler (Ölçülenler)
| Metrik           | Ölçüm Yöntemi    | Başarı Kriteri |
|------------------|------------------|----------------|
| Mean episode reward | 100 eval ep. | > 200          |
| Sample efficiency | Steps to 150 reward | < 500K    |

### 4. Kontrol Altına Alınanlar (Sabitler)
- Algoritma: PPO
- Ağ mimarisi: [64, 64] MLP
- Seed'ler: [42, 123, 456, 789, 1024]
- Ortam: HalfCheetah-v4, mujoco==2.3.7
- Donanım: RTX 4090, CUDA 12.1

### 5. Potansiyel Confound'lar
- Ortam versiyonu farkı (simülatör güncellenmesi)
- GPU non-determinizm (float16 işlemler)
- Paralel env sayısı etkisi

### 6. Bütçe
- Her konfigürasyon: 5 seed × 1M step × ~2 saat = 10 saat
- Toplam konfigürasyon: 6
- Toplam süre: ~60 GPU saati
- Deadline: YYYY-MM-DD
```

---

## Simülatör Non-Determinizm Yönetimi

Simülatörler seed'e rağmen non-deterministik olabilir:

```python
# MuJoCo / Gymnasium için tam deterministik kurulum
import os
import mujoco

# 1. Thread sayısını sabitle (paralel işlem non-determinizm kaynağı)
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

# 2. Her sıfırlamada tam seed chain
class DeterministicWrapper(gym.Wrapper):
    """Ensures full seed propagation through simulation stack."""
    
    def reset(self, seed=None, **kwargs):
        if seed is not None:
            self.env.np_random, _ = gym.utils.seeding.np_random(seed)
            # MuJoCo model seed'ini de ayarla
            if hasattr(self.env, 'model'):
                self.env.model.opt.seed = seed
        return super().reset(seed=seed, **kwargs)

# 3. Floating point determizm (dikkat: yavaşlatır)
import torch
torch.use_deterministic_algorithms(True)
os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"

# 4. Aynı başlangıç noktası doğrulama
env = DeterministicWrapper(gym.make("HalfCheetah-v4"))
obs1, _ = env.reset(seed=42)
obs2, _ = env.reset(seed=42)
assert (obs1 == obs2).all(), "Simülatör deterministic değil!"
```

---

## Deney Faktöriyel Tasarımı

Birden fazla değişken test ediyorsanız:

```python
from itertools import product
from dataclasses import dataclass

@dataclass
class ExperimentConfig:
    reward_type: str
    learning_rate: float
    seed: int
    
    @property
    def name(self) -> str:
        return f"reward={self.reward_type}_lr={self.learning_rate:.0e}_seed={self.seed}"

# Tam faktöriyel tasarım
reward_types = ["baseline", "potential", "dense"]
learning_rates = [1e-4, 3e-4]
seeds = [42, 123, 456]

all_configs = [
    ExperimentConfig(r, lr, s)
    for r, lr, s in product(reward_types, learning_rates, seeds)
]

print(f"Toplam deney sayısı: {len(all_configs)}")  # 18

# Bütçe hesabı
hours_per_exp = 2.0
total_hours = len(all_configs) * hours_per_exp
print(f"Tahmini süre: {total_hours:.0f} GPU saat")
```

---

## İstatistiksel Güç Analizi (Kaç Seed Yeterli?)

```python
from scipy import stats
import numpy as np

def required_seeds(
    effect_size: float,    # Beklenen fark / std (Cohen's d)
    alpha: float = 0.05,   # Tip I hata
    power: float = 0.80,   # 1 - Tip II hata
) -> int:
    """Kaç seed gerekli sorusunu istatistiksel olarak yanıtla."""
    from scipy.stats import norm
    
    z_alpha = norm.ppf(1 - alpha / 2)
    z_beta = norm.ppf(power)
    n = ((z_alpha + z_beta) / effect_size) ** 2
    return int(np.ceil(n))

# RL için tipik değerler:
# Küçük etki (d=0.2) → 198 seed (imkansız)
# Orta etki (d=0.5) → 32 seed (çok fazla)
# Büyük etki (d=0.8) → 13 seed
# RL gerçekçi (d=1.0+) → 5-8 seed (standart)

n = required_seeds(effect_size=1.0)
print(f"d=1.0 için gereken seed sayısı: {n}")  # 9

# Pratikte: 5 seed minimum, 10 seed ideal
```

---

## Ortam Varyant Tasarımı

Tek ortamda test yetmez — **genelleştirilebilirlik** için varyantlar:

```python
# Eğitim ortamları (farklı başlangıç koşulları)
TRAIN_CONFIGS = [
    {"gravity": 9.81, "friction": 0.8},   # Normal
    {"gravity": 9.81, "friction": 0.4},   # Düşük sürtünme
    {"gravity": 15.0, "friction": 0.8},   # Yüksek yerçekimi
]

# Test ortamları (hiç görülmemiş koşullar)
TEST_CONFIGS = [
    {"gravity": 12.0, "friction": 0.6},   # Ara değer (interpolation)
    {"gravity": 20.0, "friction": 1.2},   # Aşırı değer (extrapolation)
]

# Her konfigürasyon için ayrı seed seti kullan
TRAIN_SEEDS = [42, 123, 456, 789, 1024]
TEST_SEEDS  = [9999, 8888, 7777]  # Train seed'lerinden farklı
```

---

## Deney Koşturma Planlaması

```bash
# Paralel koşturma — tmux + ray ile
tmux new-session -d -s "exp_reward_baseline"
tmux send-keys -t "exp_reward_baseline" \
    "python train.py --reward=baseline --seeds 42 123 456 789 1024" Enter

# Ray ile toplu koşturma
python run_experiments.py \
    --configs configs/factorial_design.yaml \
    --n_parallel 4 \
    --output_dir results/exp_2026_07_23/
```

---

## Deney Tamamlama Kontrol Listesi

**Başlamadan Önce**
- [ ] Deney tasarım belgesi dolduruldu mu?
- [ ] Bütçe hesaplandı mı? (GPU saat, deadline)
- [ ] Deterministik kurulum doğrulandı mı?
- [ ] Faktöriyel tasarım mantıklı mı? (çok fazla konfigürasyon?)

**Çalışırken**
- [ ] WandB/MLflow logları geliyor mu?
- [ ] İlk 10K step'te makul bir öğrenme var mı?
- [ ] Herhangi bir NaN/Inf var mı?
- [ ] Checkpoint'ler düzgün kaydediliyor mu?

**Bitiminde**
- [ ] Tüm seed'ler tamamlandı mı?
- [ ] Sonuçlar Git'e commit edildi mi? (`result:` tipi ile)
- [ ] İstatistiksel analiz yapıldı mı?
- [ ] Deney notları güncellendi mi?
