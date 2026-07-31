---
name: wiki-query
description: "Answer a question using your LLM wiki as the knowledge source, then file the answer back as a synthesis page. Use when: (1) you want a grounded answer from your accumulated reading, (2) you want the answer to compound into the wiki. NOT for: questions about topics not yet in your wiki (run /wiki-ingest first), or quick factual lookups."
---

# Wiki Query

Answer a question using your LLM wiki as the knowledge source, then file the answer back as a synthesis page.

**Answers that stay in chat history don't compound. The wiki does.**

## Configuration

Set your wiki root in CLAUDE.md:
```
WIKI_ROOT=_system/wiki
```

## Input

$ARGUMENTS

Pass any question. Example: "Why do organisations resist good ideas?" or "What does the literature say about scaling laws and agency?"

## Protocol

### Step 1 — Read INDEX.md
Read `$WIKI_ROOT/INDEX.md` in full. Identify every page relevant to this question. Prioritise: synthesis pages first (already cross-source), then concept pages, then source-leaf pages for evidence.

### Step 2 — Read relevant pages
For each relevant page, extract:
- The key claim or insight relevant to the question
- The best quote that supports it
- Any cross-references to other pages already captured there

### Step 3 — Synthesise
Produce an answer that:
- Opens with a direct claim (not a topic) in response to the question
- Draws evidence from ≥2 distinct sources, cited with `[[wiki-links]]`
- Includes 1–2 direct quotes per major point
- Notes any tension or contradiction between sources
- Ends with what the wiki does NOT yet contain that would strengthen the answer (signals for future `/wiki-ingest`)

### Step 4 — File the answer as a synthesis page
Write the answer to a new file:
- **Concept questions**: `$WIKI_ROOT/concepts/{slug}.md`
- **Specific queries**: `$WIKI_ROOT/synthesis/{slug}.md`
- Frontmatter: `type: synthesis`, `sources: [list]`
- Slug: derived from the question (e.g. "why-orgs-resist-good-ideas")

### Step 5 — Update log.md and INDEX.md
Append to log.md:
```
## [YYYY-MM-DD] query | "question text"
New synthesis page: {path}. Sources used: [list].
```
Add the new page to INDEX.md under `## Synthesis`.

## After answering
State the synthesis page path and the 1–2 gaps in the wiki that would improve the answer on the next query.
