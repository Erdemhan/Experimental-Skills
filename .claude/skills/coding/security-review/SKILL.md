---
name: security-review
description: >
  Activate this skill when reviewing code for security vulnerabilities. Refactored 
  specifically for ML/RL research stacks: sub-process command injection, Ray Tune REST 
  API port exposure, FastAPI control endpoints, and unsafe model pickle deserialization.
---

# Security Review Skill — Research & ML Stack Security Audit

## Core Rule
> Unsafe pickle deserialization (`pickle.load()`) and unauthenticated Ray cluster ports are severe security vulnerabilities.

---

## 1. Vulnerability Checklist for ML/RL Stacks

1. **Unsafe Model Loading**: Avoid untrusted `pickle.load()` or `torch.load()` without weights_only:
   - **Unsafe**: `torch.load("checkpoint.pt")`
   - **Safe**: `torch.load("checkpoint.pt", weights_only=True)` or Safetensors.
2. **Subprocess Injection**: Never pass raw user inputs to `subprocess.Popen(shell=True)`.
3. **Ray Tune / FastAPI Port Binding**: Bind Ray dashboard and FastAPI endpoints to `127.0.0.1` instead of `0.0.0.0` in non-isolated environments.
