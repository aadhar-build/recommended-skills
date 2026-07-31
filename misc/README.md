# misc

This folder now carries two distinct meanings. Read the one that applies.

## 1. `misc/recommended/` — skills that aren't ours

The main use of `misc/` today. Everything under `misc/recommended/` is **copied from, or
inspired by, someone else** — vendored upstream skills, ports of another person's
framework, or skills whose substance is somebody else's published method.

They are here because they are worth keeping and worth recommending. They are *not* at the
repo root because the root is reserved for skills originally built here — that split is the
whole organising axis of this repo (see the root `README.md`).

**A skill belongs in `misc/recommended/` if any of these hold:**
- It was copied verbatim or lightly edited from another repo, marketplace or bundled
  distribution (OpenClaw bundled skills, `mattpocock/skills`, a ClawHub install, …).
- It is a port or re-implementation of a named third-party workflow.
- Its core content is another person's published method, even if the file was typed here.

**Conventions:**
- Layout is flat: `misc/recommended/<skill-name>/SKILL.md`. No topic sub-folders — topic
  categorisation is for own skills only.
- Credit the source in the skill's own `SKILL.md` (or at minimum in the root README entry):
  upstream repo, author, licence where one applies.
- Local edits are fine and expected — a lightly edited copy is still a copy.
- Promotion out is allowed but rare: if a skill gets rewritten far enough that nothing of
  the original remains, move it into a topic folder at the root and say so in its
  `SKILL.md`.

## 2. `misc/` itself — the uncategorised landing zone

The original meaning still stands for **own** skills that don't fit `engineering/`,
`knowledge/`, `integrations/` or `productivity/` yet. Such a skill sits directly in
`misc/<skill-name>/` — never inside `recommended/`, which would misattribute it.

This is a landing zone, not a dumping ground. If three or more accumulate around a common
theme, promote them into a new topic folder. There are currently none — every own skill in
this repo has a real topic.
