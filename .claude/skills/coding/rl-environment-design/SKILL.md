---
name: rl-environment-design
description: >
  Activate this skill when creating or modifying Gymnasium/PettingZoo compliant 
  Reinforcement Learning environments. Enforces space definitions, reset/step API contracts, 
  seed handling, and rendering wrappers.
---

# RL Environment Design Skill — Gymnasium Environment Contracts

## Core Rule
> RL environments MUST strictly adhere to Gymnasium standards (`gymnasium.Env`).  
> Non-standard APIs break RLlib, Stable-Baselines3, and Ray Tune integration.

---

## 1. Gymnasium Standard Interface Template

```python
import gymnasium as gym
from gymnasium import spaces
import numpy as np

class AcademicRLEnv(gym.Env):
    """Standard Gymnasium environment for RL research."""
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}

    def __init__(self, render_mode=None):
        super().__init__()
        self.render_mode = render_mode
        
        # 1. Observation & Action Space Definitions
        self.observation_space = spaces.Box(low=-1.0, high=1.0, shape=(8,), dtype=np.float32)
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,), dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # Seed initialization for reproducibility
        if seed is not None:
            self.np_random, _ = gym.utils.seeding.np_random(seed)
            
        obs = self._get_obs()
        info = self._get_info()
        return obs, info

    def step(self, action):
        # Action bounds check
        action = np.clip(action, self.action_space.low, self.action_space.high)
        
        # State transition
        self._update_state(action)
        
        obs = self._get_obs()
        reward = self._compute_reward()
        terminated = self._check_terminated()
        truncated = self._check_truncated()
        info = self._get_info()

        return obs, reward, terminated, truncated, info
```
