---
name: rl-marl-design
description: >
  Activate this skill when designing Multi-Agent Reinforcement Learning (MARL) 
  environments or algorithms. Enforces PettingZoo API compliance, Centralized 
  Training with Decentralized Execution (CTDE) patterns, MAPPO, QMIX, and IPPO architectures.
---

# MARL Design Skill — Multi-Agent Reinforcement Learning Architecture

## Core Rule
> Multi-Agent RL environments MUST comply with PettingZoo API (`ParallelEnv` / `AECEnv`).  
> Multi-agent algorithms MUST follow Centralized Training with Decentralized Execution (CTDE) to avoid non-stationarity.

---

## 1. CTDE Architecture Pattern (Centralized Training, Decentralized Execution)

```
[TRAINING PHASE - Centralized]
Joint States (S) + Joint Actions (A1, A2...) ──► Centralized Critic V(S) / Q(S, A1, A2)

[EXECUTION PHASE - Decentralized]
Local Obs (O_i) ──► Decentralized Policy Actor_i(a_i | O_i)
```

---

## 2. PettingZoo ParallelEnv Interface Template

```python
import numpy as np
from pettingzoo.utils.env import ParallelEnv
from gymnasium import spaces

class AcademicMARLEnv(ParallelEnv):
    """PettingZoo ParallelEnv template for multi-agent RL research."""
    metadata = {"name": "academic_marl_v0"}

    def __init__(self, num_agents=3):
        super().__init__()
        self.possible_agents = [f"agent_{i}" for i in range(num_agents)]
        self.agents = self.possible_agents[:]

        # Shared space definitions across agents
        self.observation_spaces = {
            agent: spaces.Box(low=-1.0, high=1.0, shape=(6,), dtype=np.float32)
            for agent in self.possible_agents
        }
        self.action_spaces = {
            agent: spaces.Discrete(4) for agent in self.possible_agents
        }

    def reset(self, seed=None, options=None):
        self.agents = self.possible_agents[:]
        observations = {agent: self._get_obs(agent) for agent in self.agents}
        infos = {agent: {} for agent in self.agents}
        return observations, infos

    def step(self, actions):
        # Actions is a dict mapping agent -> action
        rewards = {agent: self._compute_reward(agent, actions[agent]) for agent in self.agents}
        terminations = {agent: False for agent in self.agents}
        truncations = {agent: False for agent in self.agents}
        infos = {agent: {} for agent in self.agents}
        observations = {agent: self._get_obs(agent) for agent in self.agents}

        return observations, rewards, terminations, truncations, infos
```
