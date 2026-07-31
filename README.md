# Recommended Agent Skills (aadhar-build)

A curated collection of skills for high-performance multi-agent teams — a core
"operating system" for OpenClaw and Claude Code agent instances.

## Structure

Skills are organised into **topic folders**, modelled on the taxonomy used by
[mattpocock/skills](https://github.com/mattpocock/skills). Every skill lives at
`<category>/<skill-name>/SKILL.md`.

The three lifecycle folders (`misc/`, `in-progress/`, `deprecated/`) each carry their
own README explaining exactly when a skill moves in or out.

| Folder | What lives here |
| --- | --- |
| `engineering/` | Writing, reviewing, debugging and shipping code |
| `knowledge/` | Capturing, connecting and querying accumulated knowledge |
| `integrations/` | Driving an external tool, service or feed |
| `productivity/` | Working *with the human* — review, consensus, planning |
| `misc/` | Live and recommended, but no clear category yet |
| `in-progress/` | Draft or under trial — not yet recommended |
| `deprecated/` | Superseded or retired — kept, never deleted |

This replaces the previous flat layout. The old informal README groupings map across
directly: *Engineering & Execution* → `engineering/`, *Coordination & Knowledge
(Wiki-Mesh)* → `knowledge/`, *Intelligence & Operations* → `integrations/`.

---

## engineering/

Code gets written, reviewed, diagnosed and shipped here.

- **coding-agent** — Delegate coding tasks to Codex, Claude Code, or Pi agents via background process.
- **github** — GitHub operations via the `gh` CLI: issues, PRs, CI runs, code review, API queries.
- **heal** — Trigger a self-heal diagnostic on a CI failure log or error. Hypothesis-first; never edits before root cause is confirmed.
- **hypothesis** — Force hypothesis-first root-cause diagnosis before any file edits.
- **karpathy-filter** — Engineering guidelines that reduce common LLM coding mistakes: surgical changes, simplicity first, no speculative abstraction.
- **superpowers-mode** — Strict engineering workflow: clarify goal → spec → plan → small steps (prefer TDD) → review.
- **swarm** — Parallel 5-agent code review on the current branch diff vs master.
- **wayfinder** — Plan a chunk of work too big for one agent session as a shared map of decision tickets on the issue tracker. *(Vendored from mattpocock/skills, where it also lives under `engineering/`.)*

## knowledge/

The wiki-mesh cluster: turning sources, findings and project state into a durable,
queryable graph.

- **ontology** — Anchor ephemeral project thinking to a permanent semantic backbone of entities.
- **wiki-mesh** — Participate in a "Project War Room" by tagging findings and retrieving synthesised project context.
- **wiki-ingest** — Ingest a new source (book, paper, talk, project) into the wiki using the compounding-graph protocol.
- **wiki-query** — Answer a question from the wiki, then file the answer back as a synthesis page.
- **wiki-lint** — Health-check the wiki and surface emergent concept pages.
- **wiki-blog** — Generate a blog post scaffold from the wiki, filed back as a synthesis page.

## integrations/

Each of these is a thin, well-documented driver over one external surface.

- **gog** — Google Workspace CLI: Gmail, Calendar, Drive, Contacts, Sheets, Docs.
- **slack** — Control Slack: reactions, pinning, channel and DM operations.
- **gemini** — Gemini CLI for one-shot Q&A, summaries and generation.
- **blogwatcher** — Monitor blogs and RSS/Atom feeds for updates.

## productivity/

Skills whose output is consumed by a human, not by another agent.

- **comments-page** — Publish any Markdown doc as a Tailscale-only reviewable page with inline, text-anchored commenting.

## misc/ · in-progress/ · deprecated/

Currently empty of skills. See each folder's README for the rules on when something
moves in — and, for `in-progress/`, when it moves back out.

---

## How to use

1. Clone this repository into your agent's skills directory.
2. Read the `SKILL.md` in each skill directory for configuration requirements.
3. Enable the skills you want in your agent persona files.

Note that skill paths are now `<category>/<skill>/SKILL.md`, not `<skill>/SKILL.md`.
Any script, permission entry, or raw.githubusercontent URL pinned to the old flat
path needs updating.
