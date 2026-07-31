# Skill: Wiki-Mesh
Use this skill to participate in a "Project War Room" by tagging critical findings and retrieving synthesized project context.

## When to Use
- When you discover information that belongs to a specific project.
- When you need a high-level summary of a project's state without reading all raw logs.

## Tagging Protocol
To contribute to a War Room, you MUST append the following tag to the bottom of your markdown files:
`#wiki-target: [[ProjectName]]`

## Tooling
This skill includes the `wiki-mesh` CLI toolset:
- `wiki-mesh ingest`: Scans for new tags and moves findings to the project inbox.
- `wiki-mesh flush <ProjectName>`: (NEW) Triggers an immediate ingestion and synthesis, then signals that the session context is ready to be flushed for a clean handoff.

## Constraints
- **Do not** manually edit War Room files in `_wiki/war-rooms/`. They are managed by the automated synthesis engine.
- **Do not** tag private/blacklisted information.
