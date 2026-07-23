---
name: ci-cd-design
description: >
  Activate this skill when creating or modifying CI/CD pipelines (GitHub Actions, 
  GitLab CI) for academic Python repositories. Enforces automated PyTest runs, 
  code quality checks (ruff/black/mypy), and artifact caching. Docker is optional.
---

# CI/CD Design Skill — Academic GitHub Actions Pipeline

## Core Rule
> CI/CD pipelines in research repositories must run automated unit tests and code formatting checks on every pull request.

---

## 1. GitHub Actions Workflow Template (`.github/workflows/ci.yml`)

```yaml
name: Academic CI Pipeline

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"
          cache: "pip"

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest pytest-cov black ruff mypy
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Code Formatting & Lint Check
        run: |
          black --check .
          ruff check .

      - name: Run Unit Tests
        run: |
          pytest tests/unit/ --cov=src --cov-report=xml
```
