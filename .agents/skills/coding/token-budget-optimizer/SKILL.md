---
name: token-budget-optimizer
description: >
  Activate this skill to optimize token usage and context window efficiency. 
  Enforces subagent context isolation, log pruning, AST chunk viewing, and 
  prevents Lost-in-the-Middle attention degradation.
---

# Token Budget Optimizer Skill — Context & Token Efficiency

## Core Rules

1. **Subagent Context Isolation**:
   - Subagents (`@worker-coder`, `@unit-tester`) MUST be invoked with isolated minimal context (only `FunctionSpec` JSON, error tracebacks, and relevant AST class definitions), avoiding passing the full conversation history.

2. **Log Pruning**:
   - Never read full 1000-line test logs or training outputs. Use grep/tail patterns to extract ONLY the exact failure traceback lines.

3. **AST Chunk Viewing & Targeted Edits**:
   - Avoid reading full files over 300 lines when making local changes. Use `view_file` with precise `StartLine` and `EndLine` parameters.
   - Use `multi_replace_file_content` for non-contiguous edits rather than rewriting full files.

---

## Token Efficiency Checklist

- [ ] Is full file viewing avoided for files > 300 lines?
- [ ] Are error tracebacks extracted via minimal line ranges instead of full logs?
- [ ] Are subagent prompts constrained strictly to `FunctionSpec` and target snippets?
