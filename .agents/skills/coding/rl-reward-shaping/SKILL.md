---
name: rl-reward-shaping
description: >
  Activate this skill when designing or modifying reward functions in RL algorithms. 
  Enforces potential-based reward shaping, prevents reward hacking/perverse incentives, 
  and ensures mathematical alignment with optimal policy convergence.
---

# RL Reward Shaping Skill — Reward Design & Anti-Hacking

## Core Rule
> Reward shaping must be potential-based ($\Phi(s)$) to guarantee optimal policy invariance.  
> Unbounded or unnormalized rewards cause value function explosion and reward hacking.

---

## 1. Potential-Based Reward Shaping Formula

$$\mathcal{R}'(s, a, s') = \mathcal{R}(s, a, s') + \gamma \Phi(s') - \Phi(s)$$

- $\mathcal{R}$: Original sparse ground-truth reward
- $\Phi(s)$: State potential function (e.g. negative distance to goal)
- $\gamma$: Discount factor

### Anti-Reward Hacking Checklist
- [ ] **No Infinite Loop Exploit**: Agent cannot collect infinite positive reward by cycling between two states.
- [ ] **Survival Incentive Alignment**: In penalty-per-step environments, agent cannot commit immediate suicide to minimize cumulative loss.
- [ ] **Reward Bounding**: Output is normalized or bounded to $[-1.0, +1.0]$ or $[0, 1]$.
