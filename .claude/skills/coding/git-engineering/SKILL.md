---
name: git-engineering
description: >
  Activate this skill for general software engineering Git workflows: branch 
  management (feature/bugfix), conventional commits, rebase strategies, interactive 
  git bisect debugging, submodules, and clean history management.
---

# Git Engineering Skill — Software Engineering Git Workflows

## Core Rule
> Git history must be linear, descriptive, and clean.  
> Ambiguous commit messages like `WIP`, `fixed`, `asdf` are strictly forbidden.

---

## 1. Branching Model

```
main       ───●──────────────●───────────────●─── (Always stable & passing tests)
              \             /
feature/env    └──●────●───┘ (Feature branch)
```

- `main` / `master`: Production-ready, passing all unit and integration tests.
- `feature/<name>`: Isolated feature development.
- `fix/<name>`: Bug fixes.

---

## 2. Conventional Commit Standards

```
<type>(<scope>): <short description>

[optional detailed body]
```

### Valid Commit Types
- `feat`: New feature or capability
- `fix`: Bug fix
- `docs`: Documentation updates
- `refactor`: Code quality improvement without changing observable behavior
- `test`: Adding or modifying unit/integration tests
- `chore`: Configuration, tool, or dependency updates

---

## 3. Advanced Git Operations (Rebase & Bisect)

```bash
# 1. Interactive Rebase (Clean last 4 commits)
git rebase -i HEAD~4

# 2. Binary search to isolate breaking commit (Git Bisect)
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
git bisect run pytest tests/test_failing.py
```
