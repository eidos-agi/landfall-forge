# landfall-map - Inventory useful landfalls for a repo

## Trigger

Use this when the user asks what landfalls a repo should have, whether responsibilities are covered, or how to split arrival rituals.

## Instructions

1. Read the repo's README, task files, wiki/work folders, data files, and recent project context.
2. Identify operating domains where freshness matters.
3. For each domain, propose a named landfall with:
   - purpose
   - sources
   - write targets
   - human-only stops
   - adjacent landfalls it should not own
4. Compare proposed landfalls to existing `landfalls/*.yaml`.
5. Report missing, overlapping, and stale landfalls.

## Output

Use this shape:

```text
Recommended landfalls:
- <name>: <purpose>
  Sources: <sources>
  Writes: <targets>
  Stops: <human-only stops>

Coverage gaps:
- <gap>

Recommended next definition:
- <name>
```

## Rules

- Prefer several sharp landfalls over one mushy one.
- Name landfalls by job, not storage: `payables-landfall`, not `json-landfall`.
- Treat repeated human steering as evidence for a missing landfall.

