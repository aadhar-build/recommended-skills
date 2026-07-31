# Skill: Karpathy Filter
Engineering guidelines to reduce common LLM coding mistakes, derived from Andrej Karpathy's observations.

## When to Use
- When writing, refactoring, or reviewing code.
- When tasked with "fixing" or "improving" a system.

## 1. Surgical Changes
**Touch only what you must. Clean up only your own mess.**
- Do not "improve" adjacent code, comments, or formatting unless asked.
- Do not refactor things that aren't broken.
- Match existing style perfectly.
- If you notice unrelated dead code, mention it in chat—do not delete it.
- **The Test:** Every changed line should trace directly to the user's request.

## 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**
- No features beyond what was asked.
- No abstractions for single-use code.
- No speculative "flexibility" or "configurability."
- If you write 200 lines and it could be 50, rewrite it.
- Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Think Before Coding
- State assumptions explicitly before implementing. If uncertain, ask.
- If multiple interpretations exist, present them—don't pick silently.
- If a simpler approach exists, push back and propose it.
- If something is unclear, STOP and ask for clarification.

## 4. Goal-Driven Execution
Transform imperative tasks into verifiable goals:
- "Fix the bug" -> "Write a test that reproduces it, then make it pass."
- For multi-step tasks, state a brief plan: `[Step] -> verify: [check]`
