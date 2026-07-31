---
name: wiki-ingest
description: "Ingest a new source into your LLM wiki following the Karpathy compounding-graph protocol. Use when: (1) adding a book, paper, talk, or project to the wiki, (2) there is a conversation worth preserving as a source. NOT for: quick notes (use your notes system), or when the wiki INDEX.md doesn't exist yet (run /wiki-init first)."
---

# Wiki Ingest

Ingest a new source into the LLM wiki following the Karpathy compounding-graph protocol.

## Configuration

Set your wiki root in CLAUDE.md:
```
WIKI_ROOT=_system/wiki   # default path, adjust to your layout
```

## Input

$ARGUMENTS

Pass a book title, URL, file path, or "this conversation". If no argument: ingest the primary source discussed in this conversation.

## Protocol

### Step 1 — Read INDEX.md
Read `$WIKI_ROOT/INDEX.md` in full. Identify every existing page this source might touch: shared concepts, named entities, overlapping themes, contradicting claims.

### Step 2 — Update touched pages
For each existing page this source touches:
- **Synthesis pages** (`type: synthesis`): add a bullet under the relevant section with the new citation and what it adds. Do NOT rewrite existing content.
- **Concept pages** (`type: concept`): add the source to `sources:` frontmatter, add a paragraph citing this source's angle.
- **Source-leaf pages**: add a "See also" cross-reference if the connection is strong.

A good ingest touches **8–15 existing pages**. If you are only creating new files, the graph is staying disconnected — go back and find the links.

### Step 3 — Create source-leaf pages
Create a folder `$WIKI_ROOT/books/{slug}/` or `$WIKI_ROOT/projects/{slug}/` with these 6 files:

| File | Type | Length | Content |
|---|---|---|---|
| `index.md` | index | short | Author, title, year, one-para summary, links to sub-pages |
| `{slug}-overview.md` | source-leaf / overview | 400–600w | What the source argues and why it matters |
| `{slug}-core-concepts.md` | source-leaf / core-concepts | 150–300w per concept | Each major concept with examples |
| `{slug}-quotes.md` | source-leaf / quotes | 8–15 quotes | Direct quotes, attributed |
| `{slug}-author-talks.md` | source-leaf / author-talks | — | YouTube/podcast appearances |
| `{slug}-connections.md` | synthesis | — | How this source connects to ≥3 existing wiki entries |

Add YAML frontmatter to every file:
```yaml
---
type: source-leaf   # or synthesis, concept, index
wiki_root: $WIKI_ROOT
grounded: null
quality_score: null
---
```

### Step 4 — Update log.md
Append to `$WIKI_ROOT/log.md`:
```
## [YYYY-MM-DD] ingest | Source Title
Brief note on key concepts added and pages touched.
```

### Step 5 — Update INDEX.md
Add all new pages to the catalog table under the correct section. Format: `path | type | one-line summary`.

## After ingesting
State: how many existing pages were updated, how many new pages created, and what the strongest new connection to the existing wiki is.

## Rules
- Do not pause between steps
- If the source is a URL, fetch it. If it is a transcript, read the file.
- If the source is "this conversation", ingest the primary topic discussed.
