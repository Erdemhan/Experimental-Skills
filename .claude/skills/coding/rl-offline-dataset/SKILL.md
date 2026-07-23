---
name: rl-offline-dataset
description: >
  Activate this skill when training RL algorithms on pre-collected static datasets 
  without environment interaction (Offline RL). Enforces Conservative Q-Learning (CQL), 
  Implicit Q-Learning (IQL), D4RL dataset formatting, and distribution shift audits.
---

# Offline RL Skill — Static Dataset Training & CQL/IQL Algorithms

## Core Rule
> Offline RL MUST account for Out-Of-Distribution (OOD) action extrapolation errors.  
> Standard Q-learning fails offline due to overestimation bias on unseen actions; CQL or IQL penalty terms are required.

---

## 1. Conservative Q-Learning (CQL) Loss Objective

$$\min_Q \alpha \cdot \mathbb{E}_{s \sim \mathcal{D}} \left[ \log \sum_a \exp(Q(s, a)) - \mathbb{E}_{a \sim \mathcal{D}}[Q(s, a)] \right] + \frac{1}{2} \mathbb{E}_{(s, a, s') \sim \mathcal{D}} \left[ \left( Q(s, a) - (r + \gamma \max_{a'} \hat{Q}(s', a')) \right)^2 \right]$$

- $\mathcal{D}$: Static offline dataset (e.g. D4RL trajectories)
- $\alpha$: Conservative penalty trade-off weight

---

## 2. Offline Dataset Processing Template (D4RL Format)

```python
import numpy as np
import torch

class OfflineReplayBuffer:
    """Offline RL Replay Buffer reading static D4RL or custom datasets."""
    def __init__(self, dataset_dict: dict):
        self.observations = torch.FloatTensor(dataset_dict["observations"])
        self.actions = torch.FloatTensor(dataset_dict["actions"])
        self.next_observations = torch.FloatTensor(dataset_dict["next_observations"])
        self.rewards = torch.FloatTensor(dataset_dict["rewards"])
        self.terminals = torch.FloatTensor(dataset_dict["terminals"])
        self.size = len(self.observations)

    def sample(self, batch_size: int):
        indices = np.random.randint(0, self.size, size=batch_size)
        return (
            self.observations[indices],
            self.actions[indices],
            self.next_observations[indices],
            self.rewards[indices],
            self.terminals[indices],
        )
```
