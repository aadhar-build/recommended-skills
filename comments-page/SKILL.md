---
name: comments-page
description: Publish any Markdown doc (PRD, charter, plan) as a Tailscale-only reviewable web page with inline, text-anchored commenting — the user selects exact text and leaves a note there, not a generic comment box. Use whenever a doc needs the user's review/consensus and claude.ai/localhost links are not acceptable.
---

# comments-page

Turns a Markdown file into a live, navigable, commentable web page reachable only over Tailscale — no claude.ai, no localhost-only links. The core capability this exists for: the user selects an exact sentence/phrase and leaves a note anchored to it, not a disconnected comment at the bottom of a page. Two independent ad-hoc builds of this pattern already existed on this box (one flat-comment-box-only, one inline-anchored-only) before this skill unified them.

## When to use

Any time you'd otherwise post a doc for the user to review and comment on — PRDs, charters, plans, findings write-ups — and they need to react to *specific* passages, not the doc as a whole.

## One hub per machine, not one server per doc

A hub can live on any machine reachable over the user's tailnet — the box this session is running on, or a separate always-on VPS the user already operates. **Which machine to use is the user's call, not a default to assume** — if it's not already obvious from context, ask, rather than guessing a remote box when the session is running locally (or vice versa). Deploying to a different machine than the one this session is running on requires shell access to *that* machine (ssh or equivalent) — don't assume it's available; confirm before treating that as the plan.

Known hub instances so far (check first — there may be others; ask the user if unsure which one they mean):
- `http://100.66.85.101:7432/` — a standing multi-doc hub on a VPS, hosting several unrelated review docs.
- `http://100.77.245.96:7440/` — a hub on the user's own Mac, hosting the `voiceink` multi-page site (see "Multi-page sites" below).

**Before ever spinning up a new port on a given machine, check whether a hub is already running there** (`ss -tlnp | grep <port>` on Linux / `lsof -i :<port>` on macOS, or `curl -s http://<tailscale-ip>:<port>/api/docs`). A new doc on a machine that already has a hub means adding a subdirectory to the existing hub, not a new instance — port sprawl was the old (wrong) default.

Only create a genuinely separate instance/port on the same machine if the user explicitly asks for an isolated one-off (rare).

## Multi-page sites (grouped docs)

A `meta.json` may set `"group"` (e.g. `"voiceink"`) and `"order"` (int, default 0). Docs sharing a `group` render as one cohesive site rather than independent pages:

- The hub root (`hub.html`) sections grouped docs under a heading per group, sorted by `order` within the group; ungrouped docs still render as a flat list beneath, unchanged from the original behavior.
- Every page in the group (`index.html`) gets a persistent sidebar nav section listing every sibling page (title, sorted by `order`, current page highlighted) — above that page's own local heading TOC. This is what makes it read as a real multi-page site with navigation, not a set of disconnected docs you have to return to the hub root to switch between.

Use this whenever the user wants several related docs (overview, architecture, progress, roadmap, ...) to feel like one site — not a fresh hub per related doc.

## Phase 1: Add a doc to the hub

Inside the hub's `docs/` directory, create `docs/<slug>/`:
- `DOC.md` — the source of truth. Edit this directly for all content changes; the page re-reads it live (polls every 15s), never hand-edit the rendered HTML.
- `annotations.json` — starts as `[]`.
- `meta.json` — `{"title": "..."}`. The server auto-discovers any subdirectory with a `meta.json` — no code changes needed to register a new doc.

The hub's `server.py`, `index.html`, `hub.html`, and `watch_annotations.sh` are generic and shared across all docs — copy them from `server_template.py` / `index_template.html` / `hub_template.html` / `watch_annotations.sh` in this skill dir only when bootstrapping the hub itself or picking up a skill update, never per-doc.

**If the hub isn't running yet** (fresh box, or it was killed): `BIND_HOST` = the machine's Tailscale interface IP (`tailscale ip -4`), never `0.0.0.0`/`127.0.0.1` — this is what makes it Tailscale-only without touching `ufw`. Pick an unused port (check `ss -tlnp`). Launch: `nohup python3 server.py > server.log 2>&1 & disown` from the hub directory.

After adding a doc or restarting, verify both the hub and the specific doc:
```
curl -s -o /dev/null -w "%{http_code}" http://<tailscale-ip>:<port>/
curl -s -o /dev/null -w "%{http_code}" http://<tailscale-ip>:<port>/d/<slug>
```
before telling the user it's live. If you had to restart the server (e.g. to pick up a template change), re-check every existing doc's annotation count hasn't changed and its content still renders — a hub restart must never silently drop another doc's review history.

## Phase 2: Tell the user

Give them the doc's direct URL (`http://<tailscale-ip>:<port>/d/<slug>`) — not just the hub root. Tell them what changed if this is a redeploy of an existing page.

## Phase 3: Watch for annotations

The hub directory's `watch_annotations.sh` polls every `docs/*/annotations.json` (3s interval) and prints one line per new/changed count, tagged with the doc slug — a single `Monitor` on this script covers every doc in the hub, not just the one you just added:

```
chmod +x watch_annotations.sh && ./watch_annotations.sh
```

If a `Monitor` on this script isn't already running for this session, start one immediately after adding/updating a doc — don't wait for the user to ask "did you see my comment." If one is already running (check before starting a duplicate), the new doc is covered automatically since the script globs `docs/*/`.

## Phase 4: Respond actively — every annotation gets a reply, none sit unread

This is the part that matters most and was missing from both prior ad-hoc builds. When a new annotation lands:

1. **Read it in context** — the anchored quote tells you exactly what passage it's about; don't re-derive that from the whole doc.
2. **Actionable and unambiguous** (a clear edit, a settled decision, a typo, an answer that resolves an open question) → make the edit directly in that doc's `DOC.md`, then `POST /api/annotations/reply` (body includes `doc: "<slug>"`) with a short summary of what changed and `status: "resolved"`.
3. **Needs clarification or is a real decision point** → post a `reply` with your recommendation and the specific question, `status` stays `"open"`.
4. **Out of scope for this doc** (wrong page, belongs to a different owner/system) → say so explicitly in the reply, do not act on the underlying thing, `status` stays `"open"` pending the user's direction. (This exact scenario happened once already this session — a comment meant for one PRD landed on a different one; the fix is naming it in the reply, not guessing.)
5. Never batch-defer replies to "when I'm done with everything else" — reply as each annotation arrives, since the Monitor already tells you the moment it lands.

**Hard boundary — editing the doc is not the same as doing the thing the doc describes.** Rule 2's "make the edit directly" means *in `DOC.md` only*: prose, tables, rules, recommendations, proposals. It does NOT license taking real-world action outside the document — installing a service, running a migration, restarting production infrastructure, deleting anything — even when the annotation's ask is completely unambiguous and even when a prior message in the conversation said "go ahead" about the general direction. This happened once already: a deep-dive annotation asking to "fix" a reliability problem led to drafting and nearly installing a systemd unit before the user had actually seen the writeup, purely because the doc-reply loop made "keep going" feel continuous with "keep building." Real-world actions get proposed *in the reply text* (what, why, exact commands/files if relevant) with `status` staying `"open"`, then wait for an explicit, separate go-ahead — same discipline the permission classifier already enforces on risky Bash calls, applied proactively instead of relying on it to catch the overreach after the fact.

Only fire a `PushNotification` when the reply needs the user's attention *now* (a real open question, a decision point) — not for routine acknowledgments.

## API (implemented by server_template.py)

- `GET /` → hub.html (lists every doc under `docs/`, grouped per "Multi-page sites" above)
- `GET /api/docs` → JSON array of `{slug, title, group, order}` for every doc with a `meta.json` (`group`/`order` are `null`/`0` when unset)
- `GET /d/<slug>` → index.html (the doc viewer; front-end JS reads the slug from the URL path)
- `GET /api/<slug>/doc` → raw Markdown text of that doc's `DOC.md`
- `GET /api/<slug>/annotations` → JSON array
- `GET /api/<slug>/title` → `{title}`
- `POST /api/<slug>/annotations` → create. Body: `{type: "inline"|"general", start, end, quote, text, author}`. Server assigns `id`, `ts`, `status: "open"`, `reply: null`.
- `POST /api/annotations/reply` → update. Body: `{doc: "<slug>", id, reply, status}`. Used by Claude, not the page's own UI.

## Navigation

`index_template.html` auto-generates a sticky sidebar table of contents from the rendered doc's headings (h1/h2/h3) — no manual maintenance, works for any doc. Long docs (multi-section PRDs, charters) get real in-page navigation instead of one long scroll. Grouped docs additionally get the cross-page site nav described in "Multi-page sites" above, rendered in the same sidebar.
