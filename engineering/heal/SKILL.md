---
name: heal
description: "Trigger a self-heal diagnostic on a CI failure log or error. Hypothesis-first. Never edits a file before the root cause is confirmed. Use when: (1) CI is red and the cause isn't obvious, (2) a test is flaking and you want structured diagnosis, (3) handing off a known failure to fix autonomously. NOT for: errors with an obvious fix (just fix them), or when you need a human decision on approach."
disable-model-invocation: true
---

# Heal

Trigger a self-heal diagnostic on a CI failure log or error. Hypothesis-first. Never edits a file before the root cause is confirmed.

## Input

$ARGUMENTS

Pass a log path, an error string, a failing test name, or a ticket ID whose description contains the failure.

## Protocol

### Step 1 — Extract error signature
From the input, extract: stack trace head, failing test name, error class. If input is a ticket ID, fetch it first.

### Step 2 — Search for prior incidents (optional)
If your project has a memory or knowledge base, search it for this error signature. If a fix pattern is found with successful prior history → state it and apply directly (skip to Step 5).

If no memory system is configured, proceed directly to Step 3.

### Step 3 — State ONE hypothesis
> "I believe the failure is caused by **X** because **Y**."

Name the single fastest verification command — a targeted test run, a grep, a log line check, a type check. Do not name more than one.

### Step 4 — Verify
Run ONLY that command. Report what it shows verbatim.

- **Confirmed** → proceed to Step 5
- **Rejected** → return to Step 3 with a new hypothesis (maximum 2 cycles total)
- **Both fail** → escalate: "Root cause unclear after 2 cycles. Findings: [X, Y]. Your call."

### Step 5 — Apply fix
Edit the minimum set of files. Do not touch unrelated code.

### Step 6 — Run full test suite
All tests must pass. Treat remaining failures as new incidents — new hypothesis cycle, do not batch.

### Step 7 — Write regression test
Add a test that would have caught this specific failure. Non-negotiable.

### Step 8 — Commit
```
git commit -m "fix: <error-signature>"
```

### Step 9 — Record outcome (optional)
If your project has a memory system, record the fix pattern and outcome so future heals can skip straight to the fix.

## Rules
- Hypothesis before edits. Always. No exceptions.
- Do not batch unrelated fixes into the same commit.
- Maximum 2 hypothesis cycles before escalating.
- Every fix requires a new regression test.
