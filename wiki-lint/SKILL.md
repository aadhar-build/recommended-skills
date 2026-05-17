---
name: wiki-lint
description: "Health-check your LLM wiki and surface emergent concept pages. Use when: (1) after every 3 ingests, (2) the wiki feels disconnected, (3) you want to find gaps in coverage. NOT for: first-time setup (no INDEX.md yet), or quick reads."
---

# Wiki Lint

Health-check your LLM wiki and surface emergent concept pages.

Run after every 3 ingests, or any time the graph feels disconnected.

## Configuration

Set your wiki root in CLAUDE.md:
```
WIKI_ROOT=_system/wiki
```

## Protocol

### Step 1 — Orphan detection
Scan every page in `$WIKI_ROOT/` (use INDEX.md as the page list). For each page, check whether any other page links to it with a `[[wiki-link]]`. Pages with zero inbound links are orphans.

Report orphans grouped by type. Offer to:
- Connect them (add a link from a relevant page), or
- Flag for deletion if genuinely redundant

### Step 2 — Concept emergence
Scan all pages for `[[wiki-link]]` targets that appear in **3 or more** different source pages but do not have their own dedicated concept page.

For each emergent concept:
1. Create `$WIKI_ROOT/concepts/{concept-slug}.md`:
   - `type: concept` frontmatter
   - Definition (2–3 sentences)
   - One section per source that cites it: key insight + best quote
   - Synthesis paragraph: what do all these sources together say that none says alone?
2. Add backlinks: update each citing page to include a `[[concepts/{concept-slug}]]` cross-reference

Concepts must emerge from data — do not create pages for concepts appearing in only 1–2 sources.

### Step 3 — Grounding failures
Find all pages where `grounded: false` in frontmatter. For each:
- Report the `grounding_errors` field (if present)
- Offer to fix broken links or remove the link

### Step 4 — Quality flags
Find all synthesis/concept pages where `quality_score < 5` or `needs_regen: true`. Report paths and scores. Offer to regenerate.

### Step 5 — Divergence report
If your wiki uses a quality judge and a `feedback.jsonl` log, check for:
- `user_signal = "positive"` AND `judge_score < 5` (judge too harsh)
- `user_signal = "negative"` AND `judge_score >= 6` (judge too lenient)

If 10+ divergences: surface the pattern and propose a rubric revision.

### Step 6 — Update log.md
Append:
```
## [YYYY-MM-DD] lint | N orphans, M concepts emerged, K grounding failures, J quality flags
```

## Output format
```
## Lint Report — [date]
Orphans (N): [list]
Emergent concepts (M): [list of created pages]
Grounding failures (K): [list with errors]
Quality flags (J): [list with scores]
```

Then take action on anything resolvable automatically. Flag anything needing a decision.
