# Project Constitution — Agentic AI & Skills System

## Overview
This project contains a 3-tier hierarchical multi-agent system, Model Context Protocol (MCP) server configurations, and a comprehensive skills library for Claude Code.

---

## Agent Hierarchy

This project uses a **3-tier agent hierarchy**. Select the appropriate agent for your scenario:

| Scenario | Agent |
|---|---|
| New project setup / major feature / architectural decisions | `@architect` |
| Module design / function specification planning | `@module-planner` |
| Single function implementation & unit test generation | `@worker-coder` |
| Failed unit test debugging (Tier 2 escalation) | `@unit-tester` |
| Cross-module integration testing & contract verification | `@integration-verifier` |
| Long-running experiment execution, sweep tracking & monitoring | `@experiment-runner` |
| Academic writing, LaTeX formatting & BibTeX compilation | `@paper-writer` |
| Academic advisor progress reporting & executive briefing | `@advisor-reporter` |
| Session startup, context sync & state report | `@context-manager` |

### Golden Rule
> Architect never writes code. Worker never makes design decisions. Every agent operates strictly within its layer.

---

## Communication & Approval Rules (Plan-First vs. Autonomous Execution)
- **Design & Functionality Level (`@architect`, `@module-planner`, `@paper-writer`) — PLAN-FIRST REQUIRED**:
  - When designing a new feature, architectural change, or function spec, **the plan must first be explained to the user and explicit approval requested**.
  - No design files (`module_spec` or `FunctionSpec`) or paper structures are finalized until the user explicitly approves (e.g., "approved", "proceed", "apply").
- **Implementation & Test Level (`@worker-coder`, `@unit-tester`, `@integration-verifier`, `@experiment-runner`) — AUTONOMOUS EXECUTION**:
  - Once the user approves the spec/design, the execution layer operates **autonomously**.
  - `worker-coder` and `unit-tester` execute unit tests, 3x retry cycles, and code fixes **autonomously without stopping for user approval at every step**.
  - Escalation to the user occurs ONLY when all retries are exhausted, when a functionality/spec change is required, or when a Type B/C research bug impact is identified.

---

## Coding & Debugging Rules
- Never write code without a spec.
- **🚫 Speculative Debugging Prohibited (Empirical Evidence Required)**:
  - No agent (`worker-coder`, `unit-tester`, `architect`) may make code changes or hypothesize solutions without first reading the full log file, `traceback` output, or `pytest` `stderr` to **empirically verify the root cause**.
  - Every code modification MUST be justified by an explicit error log or a failing test.
- Every function requires a corresponding unit test before completion.
- Pull requests / commits are not opened until tests pass.
- **Research Code Debugging (Critical)**:
  - When fixing a bug in an academic research project/code, **the `@research-debug` skill MUST be invoked first**.
  - **Academic Integrity Boundary**: Fixes must not introduce data leakage or violate theoretical assumptions.
  - **Goal Distortion Prevention**: Bug fixes must not alter the test hypothesis (`hypothesis-framing`) or distort fair comparison baselines (`fair-comparison`).
  - Classify bugs into Type A (isolated software), Type B (result-altering), or Type C (methodology-breaking).
  - Type B and C bugs require assessing previous results and specifying `BUG-IMPACT` in commit messages before modifying code.
- **📐 Formal Standards & Latest Stable Version Rule**:
  - **Formal Methodology**: When implementing algorithms, mathematical models, or architectures, ad-hoc, informal, or hacky shortcuts are strictly prohibited. Agents MUST strictly adhere to the most formal, mathematically rigorous standards from peer-reviewed literature and official specifications.
  - **Latest Stable Versions**: Deprecated APIs, obsolete syntax, or legacy package patterns (e.g. legacy Gym instead of `gymnasium`, outdated PyTorch autograd patterns instead of `torch.amp` / `torch.compile`, deprecated NumPy scalar types) are forbidden. Agents MUST target the latest stable releases and official current API specifications.
- **⚡ Token Budgeting & Context Isolation Rule**:
  - **Subagent Context Isolation**: Subagents (`worker-coder`, `unit-tester`) MUST be invoked with minimal isolated context (`FunctionSpec` JSON and error tracebacks) rather than dumping full conversation history.
  - **Log & File Pruning**: Full file viewing for files > 300 lines or reading full 1000-line log files is forbidden. Use targeted `view_file` line ranges and traceback extraction to preserve context window attention.
- Every function must have a `FunctionSpec` JSON before implementation.
- Code without unit tests is NEVER considered `Done`.
- Type annotations (type hints) are mandatory.
- Docstring format: Google style.

---

## Academic Research Rules
- Every claim must be supported by citations — unreferenced claims are rejected.
- **Formulation & Parameters Registry Rule (`FORMULATION.md`)**:
  - Academic equations, symbols, explanations, and parameter sources are maintained in `.claude/context/FORMULATION.md`.
  - This file is **User-Locked**; NO AGENT may modify `FORMULATION.md` content, equations, or parameter values without explicit, direct user approval.
  - If code conflicts with `FORMULATION.md`, the code must be fixed; the registry remains untouched.
- **🌐 Heterogeneous Environment Awareness**:
  - Agents must recognize that the development machine (local OS) and the experiment execution server/cluster (HPC/GPU cluster) may have different hardware (GPU/CPU/RAM), OS (Windows/Linux), CUDA versions, or library dependencies.
  - "Works on my local machine" is an invalid assumption. Paths must use dynamic resolution (`pathlib.Path`, `os.path`) and device checks (`torch.cuda.is_available()`); hardcoded OS/hardware assumptions are forbidden.
- Comparative studies MUST activate the `@fair-comparison` skill.
- Experimental setup MUST activate the `@empirical-rigor` skill.
- Numerical result interpretation MUST activate the `@statistical-validity` skill.

---

## Task & Context Tracking
- `context.db` (SQLite) is queried at session startup via `@context-manager` or `python .claude/hooks/context_db.py summary`.
- `ARCHITECTURE.md` is updated after every architectural decision.
- `@context-manager` runs automatically at session initialization.

---

## Security
- Destructive commands (`rm -rf`, disk format, fork bomb, force pushing to main/master) are blocked by the `security_gate.py` hook.