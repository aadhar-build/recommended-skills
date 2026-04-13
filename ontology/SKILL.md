# Skill: Ontology-Mesh (Phase 3)
Use this skill to anchor ephemeral project thinking to a permanent semantic backbone.

## When to Use
- When a project discovery defines a core entity (person, company, technology).
- When you need a "Ground Truth" definition that persists across multiple projects.

## Anchoring Protocol
1. **Link to Ontology:** Always use double-bracket links to ontology entities (e.g., `[[OpenClaw]]`).
2. **Freshness Check:** Check the `last_verified` date in the entity's YAML frontmatter. If >90 days, trigger a "Lazy-Validation" sync.
3. **Drafting:** New entities should be proposed in `_ontology/inbox/` as draft markdown files.

## Tooling
- `ontology-mesh graph`: Generates a Mermaid visual graph from the current schema.
- `ontology-mesh anchor`: Verifies project links against the permanent ontology.
