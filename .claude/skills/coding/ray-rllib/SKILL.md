---
name: ray-rllib
description: >
  Activate this skill when using Ray or Ray RLlib for distributed reinforcement 
  learning, hyperparameter tuning with Ray Tune, or distributed data processing 
  with Ray Data. Covers RLlib algorithm configuration, custom model registration, 
  Ray Tune search spaces, and cluster deployment.
---

# Ray RLlib Skill — Dağıtık Pekiştirmeli Öğrenme

## Temel Kural
> Ray'in gücü tek makine çok çekirdek → çok makine dağıtık geçişini şeffaf yapmasından gelir. Ama yanlış konfigürasyon, dağıtıktan fayda yerine overhead üretir.

---

## Hızlı Başlangıç — RLlib ile PPO

```python
import ray
from ray.rllib.algorithms.ppo import PPOConfig
from ray.tune.registry import register_env

# 1. Ortamı kaydet
register_env("my_env", lambda config: MyCustomEnv(**config))

# 2. RLlib'i başlat
ray.init()

# 3. Algoritma konfigürasyonu (yeni API)
config = (
    PPOConfig()
    .environment(
        env="my_env",
        env_config={},         # Ortam yapılandırması
    )
    .env_runners(
        num_env_runners=4,     # Paralel worker sayısı
        num_envs_per_env_runner=1,
    )
    .training(
        lr=3e-4,
        gamma=0.99,
        lambda_=0.95,          # GAE lambda
        clip_param=0.2,        # PPO clip
        train_batch_size=4096,
        sgd_minibatch_size=128,
        num_sgd_iter=10,
    )
    .resources(
        num_gpus=1,            # Trainer GPU'su
    )
    .framework("torch")        # torch veya tf2
    .debugging(seed=42)        # Tekrarlanabilirlik
)

# 4. Eğitim
algo = config.build()

for i in range(100):
    result = algo.train()
    print(f"Iter {i}: reward={result['env_runners']['episode_reward_mean']:.2f}")
    
    if i % 10 == 0:
        checkpoint = algo.save()
        print(f"Checkpoint: {checkpoint}")

ray.shutdown()
```

---

## Ray Tune — Hyperparameter Search

```python
from ray import tune
from ray.tune.schedulers import ASHAScheduler
from ray.tune.search.optuna import OptunaSearch

def train_rl(config):
    """Trainable function for Ray Tune."""
    algo = PPOConfig().training(
        lr=config["lr"],
        gamma=config["gamma"],
        clip_param=config["clip_param"],
    ).environment(env="my_env").build()
    
    for _ in range(50):
        result = algo.train()
        tune.report(
            reward=result["env_runners"]["episode_reward_mean"],
            loss=result.get("info", {}).get("learner", {}).get("default_policy", {}).get("total_loss", 0),
        )

# Search space
search_space = {
    "lr": tune.loguniform(1e-5, 1e-3),
    "gamma": tune.uniform(0.95, 0.999),
    "clip_param": tune.uniform(0.1, 0.3),
}

# Bayesian optimization + ASHA pruner
searcher = OptunaSearch(metric="reward", mode="max")
scheduler = ASHAScheduler(metric="reward", mode="max", grace_period=10)

analysis = tune.run(
    train_rl,
    config=search_space,
    num_samples=50,           # Toplam deneme sayısı
    search_alg=searcher,
    scheduler=scheduler,
    resources_per_trial={"cpu": 4, "gpu": 0.5},
    storage_path="./ray_results",
    name="ppo_hyperparam_search",
)

best_config = analysis.get_best_config(metric="reward", mode="max")
print("En iyi konfigürasyon:", best_config)
```

---

## Custom Model Kaydı

```python
from ray.rllib.models import ModelCatalog
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
import torch
import torch.nn as nn

class CustomNetwork(TorchModelV2, nn.Module):
    """Custom neural network for RLlib."""
    
    def __init__(self, obs_space, action_space, num_outputs, model_config, name):
        TorchModelV2.__init__(self, obs_space, action_space, num_outputs, model_config, name)
        nn.Module.__init__(self)
        
        self.network = nn.Sequential(
            nn.Linear(obs_space.shape[0], 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
        )
        self.policy_head = nn.Linear(256, num_outputs)
        self.value_head = nn.Linear(256, 1)
        self._value = None
    
    def forward(self, input_dict, state, seq_lens):
        features = self.network(input_dict["obs"].float())
        self._value = self.value_head(features)
        return self.policy_head(features), state
    
    def value_function(self):
        return self._value.squeeze(1)

# Modeli RLlib'e kaydet
ModelCatalog.register_custom_model("custom_net", CustomNetwork)

# Konfigürasyonda kullan
config.training(
    model={"custom_model": "custom_net", "custom_model_config": {}}
)
```

---

## Ray Cluster Yapılandırması

```yaml
# cluster.yaml — Ray cluster konfigürasyonu
cluster_name: rl_training

provider:
  type: aws
  region: us-east-1

head_node_type:
  instance_type: g4dn.xlarge  # GPU'lu head node
  resources:
    CPU: 4
    GPU: 1

worker_node_types:
  - node_type_name: cpu_worker
    resources:
      CPU: 8
    min_workers: 2
    max_workers: 10
```

```bash
# Cluster başlat
ray up cluster.yaml

# Job gönder
ray submit cluster.yaml train.py

# Dashboard
ray dashboard cluster.yaml  # http://localhost:8265
```

---

## RLlib Kontrol Listesi

- [ ] Ortam `register_env()` ile kaydedildi mi?
- [ ] `seed` konfigürasyona eklendi mi?
- [ ] Worker sayısı CPU çekirdeğine göre ayarlandı mı?
- [ ] Checkpoint sıklığı yeterli mi?
- [ ] Ray Tune ile hyperparameter arama yapıldı mı?
- [ ] Sonuçlar `WandB` veya `MLflow` ile loglanıyor mu?
- [ ] Memory leak kontrolü: uzun eğitimlerde bellek izlendi mi?

---

## Desteklenen Algoritmalar (Özet)

| Algoritma | Action Space | Kullanım |
|---|---|---|
| PPO | Discrete + Continuous | Genel amaçlı, kararlı |
| SAC | Continuous | Sample efficient, off-policy |
| TD3 | Continuous | Deterministic, düşük varyans |
| DQN | Discrete | Basit discrete problemler |
| IMPALA | Discrete + Continuous | Çok büyük ölçek, asenkron |
| APPO | Discrete + Continuous | Asenkron PPO, büyük ölçek |
