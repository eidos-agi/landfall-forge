# landfall-map - Inventory useful landfalls for a repo

## Trigger

Use this when the user asks what landfalls a repo should have, whether responsibilities are covered, or how to split arrival rituals.

## Instructions

1. Read the repo's README, task files, wiki/work folders, data files, and recent project context.
2. Identify operating domains where freshness matters.
3. Infer what landfalls the user probably needs from:
   - repeated user steering
   - recent task friction
   - stale or contradictory repo state
   - source surfaces the user keeps asking to refresh
   - human-only boundaries the user keeps correcting
   - the current work context
4. For each domain, propose 2-4 possible landfall shapes at different sizes:
   - `micro`: one notification, portal, person, or payment
   - `focused`: one workstream
   - `broad`: one domain across several workstreams
   - `strategic`: the whole operating picture
5. For each candidate landfall, include:
   - purpose
   - size
   - sources
   - write targets
   - human-only stops
   - adjacent landfalls it should not own
   - tradeoff
6. Recommend the best next landfall to write.
7. Compare proposed landfalls to existing `landfalls/*.yaml`.
8. Report missing, overlapping, and stale landfalls.

## Output

Use this shape:

```text
Recommended landfalls:
- <name> (<size>): <purpose>
  Sources: <sources>
  Writes: <targets>
  Stops: <human-only stops>
  Tradeoff: <tradeoff>

Coverage gaps:
- <gap>

Options:
- Small: <name>
- Medium: <name>
- Broad: <name>
- Strategic: <name>

Recommended next definition:
- <name>
```

## Rules

- Prefer several sharp landfalls over one mushy one.
- Name landfalls by job, not storage: `payables-landfall`, not `json-landfall`.
- Treat repeated human steering as evidence for a missing landfall.
- Do not pretend the first inferred topology is certainly right. Suggest options and recommend one.
- Always include at least one smaller and one larger option when designing a new landfall family.
