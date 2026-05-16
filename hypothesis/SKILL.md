---
name: hypothesis
description: "Force hypothesis-first root-cause diagnosis before any file edits. Use when: (1) handing off a tricky bug, (2) the first instinct is to start editing without understanding, (3) a CI failure needs root cause before a fix. NOT for: simple one-liner fixes where the cause is obvious."
---

# Hypothesis

Force hypothesis-first root-cause diagnosis before any file edits.

## Input

$ARGUMENTS

Pass a failing test path, an error string, a log excerpt, or a ticket ID.

## Protocol

### Step 1 — Read only, do NOT edit
Read the error, failing test output, or bug description. Read the relevant code. Form a mental model. **Do not touch any file.**

### Step 2 — State ONE hypothesis
> "I believe the failure is caused by **X** because **Y**."

One sentence. One claim. Not a list of possibilities.

### Step 3 — Name the single fastest verification
The one command that will confirm or refute the hypothesis — a targeted test, a grep, a type check, a log tail. Name it before running it.

### Step 4 — Run ONLY that command
Report what it shows verbatim.

### Step 5a — Hypothesis confirmed
List exactly which files to change and what the minimal fix is. Proceed with edits.

### Step 5b — Hypothesis rejected
Return to Step 2 with a new hypothesis. Do NOT iterate on the old one. Maximum **2 cycles total**.

### Step 6 — If both hypotheses fail
Escalate:
> "Root cause unclear after 2 cycles. Findings: [X, Y]. Your call."

Stop. Do not guess a third time.

### Step 7 — After fix
Run the full test suite. Write a regression test that would have caught this specific failure. Non-negotiable.

## Rules
- Never touch a file before a hypothesis is confirmed
- Maximum 2 hypothesis cycles before escalating
- Every fix requires a new regression test
- Do not batch unrelated fixes in the same hypothesis cycle
