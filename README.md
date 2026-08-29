# aadhar-build-skills

Agent skills used by Aadhar's OpenClaw and Claude Code instances.

## The organising axis: authorship

The top level of this repo is split by **who wrote the skill**, not by what it does.

| Location | What lives there |
| --- | --- |
| Topic folders at the repo root (`engineering/`, `knowledge/`, `integrations/`, `productivity/`) | **Skills built here.** Originally authored for this setup — the idea, the protocol and the text are ours. |
| `misc/recommended/` | **Skills copied from, or inspired by, someone else.** Vendored upstream skills, ports, and skills derived from another person's framework — kept because they are good, credited because they aren't ours. |

Own skills keep their **topic folder**, so each still lives at
`<category>/<skill-name>/SKILL.md`. Third-party skills live flat at
`misc/recommended/<skill-name>/SKILL.md` — they are not re-categorised by topic.

### Which side does a new skill belong on?

Put it in `misc/recommended/` if **any** of these are true:

- It was copied (verbatim or lightly edited) from another repo, marketplace or bundled
  distribution — e.g. an OpenClaw bundled skill, a `mattpocock/skills` skill, a ClawHub
  install.
- It is a port or re-implementation of someone else's named framework or workflow.
- Its substance is another person's published method, even if the file was typed here.

Otherwise it belongs in a topic folder at the root. If a copied skill is eventually
rewritten far enough that nothing of the original remains, it can be promoted out of
`misc/recommended/` into a topic folder — note that in the skill's own `SKILL.md`.

---

## Own skills

### engineering/
Code gets written, reviewed, diagnosed and shipped here.

- **heal** — Trigger a self-heal diagnostic on a CI failure log or error. Hypothesis-first; never edits before root cause is confirmed.
- **hypothesis** — Force hypothesis-first root-cause diagnosis before any file edits.
- **swarm** — Parallel 5-agent code review on the current branch diff vs master.

### knowledge/
The wiki cluster: turning sources, findings and project state into a durable,
queryable graph.

- **wiki-ingest** — Ingest a new source (book, paper, talk, project) into the wiki using the compounding-graph protocol.
- **wiki-query** — Answer a question from the wiki, then file the answer back as a synthesis page.
- **wiki-lint** — Health-check the wiki and surface emergent concept pages.
- **wiki-blog** — Generate a blog post scaffold from the wiki, filed back as a synthesis page.

### integrations/
Thin, well-documented drivers over one external surface each.

_Currently empty — `blogwatcher` moved to `misc/recommended/` on 2026-08-02 once it was
confirmed to be a third-party skill. The category stays open for future own drivers._

### productivity/
Skills whose output is consumed by a human, not by another agent.

- **comments-page** — Publish any Markdown doc as a Tailscale-only reviewable page with inline, text-anchored commenting.

---

## misc/recommended/ — copied or inspired

Kept and recommended, but authored elsewhere. See `misc/README.md` for the rules.

- **blogwatcher** — Monitor blogs and RSS/Atom feeds for updates. *(OpenClaw bundled skill; upstream `Hyaxia/blogwatcher`. Differs from the bundled copy on one line only.)*
- **coding-agent** — Delegate coding tasks to Codex, Claude Code, or Pi agents via background process. *(OpenClaw bundled skill, locally edited.)*
- **github** — GitHub operations via the `gh` CLI. *(OpenClaw bundled skill, locally edited.)*
- **gog** — Google Workspace CLI: Gmail, Calendar, Drive, Contacts, Sheets, Docs. *(OpenClaw bundled skill, effectively verbatim.)*
- **slack** — Control Slack: reactions, pinning, channel and DM operations. *(OpenClaw bundled skill, locally edited.)*
- **gemini** — Gemini CLI for one-shot Q&A, summaries and generation. *(OpenClaw bundled skill, locally edited.)*
- **karpathy-filter** — Engineering guidelines that reduce common LLM coding mistakes. *(Derived from Andrej Karpathy's published observations.)*
- **adhd** — Parallel divergent ideation: spawn isolated idea branches under different cognitive frames, score, cluster, prune traps and deepen the survivors. *(Vendored from `UditAkhourii/adhd`, MIT, by Udit Akhouri; upstream `main` at `eaeba4e98b38`.)*
- **llm-council** — Run a question through a council of five advisors who analyse it independently, peer-review each other anonymously, then synthesise a final verdict. *(Vendored from `aiwithremy/claude-skills-llm-council`, by Ole Lehmann; methodology adapted from Andrej Karpathy's `karpathy/llm-council`. Upstream declares no licence.)*
- **impeccable** — Design, critique and polish frontend interfaces: visual hierarchy, accessibility, responsive behaviour, motion, UX copy and reusable design tokens. *(Vendored from `pbakaus/impeccable`, Apache-2.0, by Paul Bakaus, v4.0.4; upstream `main` at `c5e1ddd`.)*

---

## Lifecycle folders

- `misc/` — third-party skills under `misc/recommended/`, plus the original "no clear topic yet" landing zone for own skills.
- `in-progress/` — draft or under trial, not yet recommended. Currently holds no skills.
- `deprecated/` — superseded or retired, kept and never deleted. Currently holds
  **ontology** and **wiki-mesh** (own work, superseded 2026-08-02), and **wayfinder** and
  **superpowers-mode** (both `misc/recommended/`, superseded 2026-08-30 — each duplicates a
  skill already shipped by an installed plugin: `wayfinder` by `mattpocock-skills`,
  `superpowers-mode` by the always-on `superpowers` plugin).

Each carries its own README with the rules for moving in and out.

---

## How to use

1. Clone this repository into your agent's skills directory.
2. Read the `SKILL.md` in each skill directory for configuration requirements.
3. Enable the skills you want in your agent persona files.

Skill paths are `<category>/<skill>/SKILL.md` for own skills and
`misc/recommended/<skill>/SKILL.md` for copied ones. Any script, permission entry, or
raw URL pinned to an older path — flat, or the earlier topic-only layout — needs updating.
Three paths moved on 2026-08-02 and any pin to them is now stale:
`integrations/blogwatcher` → `misc/recommended/blogwatcher`,
`knowledge/ontology` → `deprecated/ontology`, and
`knowledge/wiki-mesh` → `deprecated/wiki-mesh`.
Two more paths moved on 2026-08-30:
`misc/recommended/wayfinder` → `deprecated/wayfinder`, and
`misc/recommended/superpowers-mode` → `deprecated/superpowers-mode`.
The repository was also renamed from `recommended-skills` to `aadhar-build-skills`;
GitHub redirects the old name, but pinned URLs are better updated.
