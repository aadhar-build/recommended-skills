---
name: wiki-blog
description: "Generate a blog post scaffold from your LLM wiki. The scaffold is filed back as a synthesis page — it becomes the draft you edit and publish. Use when: (1) you have a topic or angle and want the wiki to do the synthesis, (2) you want a post grounded in multiple sources. NOT for: quick social posts, posts about topics not yet in your wiki (run /wiki-ingest first)."
---

# Wiki Blog

Generate a blog post scaffold from your LLM wiki. Filed back as a synthesis page — the draft you edit and publish.

## Configuration

Set your wiki root in CLAUDE.md:
```
WIKI_ROOT=_system/wiki   # adjust to your layout
```

## Input

$ARGUMENTS

Pass a topic, angle, or claim. Example: "why organisations kill great ideas" or "the case for agent harnesses over monolithic LLMs".

## Protocol

### Step 1 — Convert topic to claim
The difference:
- Topic: "Why organisations kill great ideas"
- Claim: "Every great idea gets killed by structural incentives, not bad people — and three sources from completely different domains prove it"

State the **claim** before doing anything else. If the input is already a claim, proceed. If it's a topic, sharpen it.

### Step 2 — Read INDEX.md
Read `$WIKI_ROOT/INDEX.md`. Identify every synthesis page, concept page, and relevant source-leaf that provides evidence for or against the claim.

### Step 3 — Read relevant pages
For each relevant page, extract:
- The strongest argument it contributes to the claim
- The single best quote (sharp, attributable, quotable)
- Any counter-argument that should be pre-empted

### Step 4 — Build the scaffold

```markdown
---
type: synthesis
query: "[the claim as stated]"
sources: [list of wiki pages used]
---

# [The Claim — one sentence, sharp enough to be a headline]

## [Argument 1 — short title]
[2–3 sentences. Must synthesise ≥2 sources.]
> "[Best quote]" — [[source/quotes-page]]

## [Argument 2 — short title]
[2–3 sentences. Different source combination from Argument 1.]
> "[Best quote]" — [[source/quotes-page]]

## [Argument 3 — short title]
...

## Pre-empt
[1 paragraph: acknowledge the strongest counter-argument, then reframe.]

## Suggested post structure
- **Hook**: [One arresting opening line — not "In this post I will..."]
- **Body order**: [Which argument to lead with and why]
- **Closer**: [Reframe, call to action, or open question]

## What the wiki is missing
[1–3 gaps — sources not yet ingested that would strengthen this post. Flag for future /wiki-ingest.]
```

### Step 5 — File the scaffold
Write to `$WIKI_ROOT/synthesis/{slug}.md` where slug is derived from the claim.

### Step 6 — Update log.md and INDEX.md
Append to log.md:
```
## [YYYY-MM-DD] blog | "claim text"
Scaffold filed at: synthesis/{slug}.md. Sources: [list].
```
Add to INDEX.md under `## Synthesis`.

### Step 7 — Invite feedback
Output the scaffold in full. Then ask:
> "How does this read? Say 'strong', 'weak on [section]', or 'wrong on [point]'."

## Rules
- Claim must be stated before reading any wiki pages
- Each argument paragraph must cite ≥2 sources — single-source arguments are not synthesis
- Do not ask for confirmation before building the scaffold — produce it, then invite feedback
