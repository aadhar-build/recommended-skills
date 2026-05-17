---
name: swarm
description: "Run a parallel 5-agent code review on the current branch diff vs master. Use when: (1) reviewing a PR before merge, (2) spot-checking a large refactor, (3) security-sensitive changes. Flags: --security (SecurityAgent only), --perf (PerformanceAgent only), --tests (TestCoverageAgent only). NOT for: trivial 1-line fixes, first-draft work, or branches without any tests."
---

# Swarm

Run a parallel 5-agent code review on the current branch diff vs master.

## Input

$ARGUMENTS

- (empty) → full 5-agent review of current branch vs master
- `--security` → SecurityAgent only
- `--perf` → PerformanceAgent only
- `--tests` → TestCoverageAgent only

## Protocol

### Step 1 — Get the diff
```bash
git diff master...HEAD --stat
git diff master...HEAD
```

### Step 2 — Spawn specialist agents in parallel

Use the Agent tool. All 5 calls must be in **a single message** (parallel execution). Pass each agent the full diff.

**SecurityAgent** — scan for:
- Secret/API key leaks in code or comments
- Injection risks: SQL, shell command, prompt injection
- Unsafe deserialization or `eval()` usage
- Hardcoded credentials or tokens

Returns: `{verdict: pass|fail|warn, findings: [...]}`

**PerformanceAgent** — flag:
- N+1 query patterns
- Blocking I/O in async paths
- Unbounded loops or missing pagination
- Memory leaks or large object accumulation

Returns: `{verdict: pass|fail|warn, findings: [...]}`

**TestCoverageAgent** — verify:
- Every changed function has a corresponding test
- Coverage on touched files ≥ 85% (run `pytest --cov` or equivalent)
- New code branches are covered

Returns: `{verdict: pass|fail|warn, findings: [...]}`

**ImportDriftAgent** — check:
- Any removed or renamed exports that break other modules
- Stale imports referencing deleted symbols (`grep -r "from <changed_module> import"`)
- No circular imports introduced

Returns: `{verdict: pass|fail|warn, findings: [...]}`

**ContractAgent** — check:
- Public API signatures unchanged (unless version bump present)
- No removed exports or broken imports
- No breaking type changes

Returns: `{verdict: pass|fail|warn, findings: [...]}`

### Step 3 — Aggregate results

Produce a verdict matrix:

```
| Agent             | Verdict | Key Finding                           |
|-------------------|---------|---------------------------------------|
| SecurityAgent     | PASS    | —                                     |
| PerformanceAgent  | WARN    | unbounded loop in lib/foo.py:42       |
| TestCoverageAgent | PASS    | 91% coverage on touched files         |
| ImportDriftAgent  | PASS    | —                                     |
| ContractAgent     | FAIL    | removed export `bar` from lib/baz.py  |
```

### Step 4 — State merge recommendation

`APPROVE` / `BLOCK` / `WARN` with explicit reasons.

## Block conditions (hard)
- SecurityAgent returns `fail` → **BLOCK**
- ContractAgent returns `fail` → **BLOCK**

## Warn conditions (soft)
- PerformanceAgent returns `warn`
- TestCoverageAgent returns `warn` (but not `fail`)
- ImportDriftAgent returns `warn`

## No dependencies
Requires only `git` and a test runner. No external binaries.
