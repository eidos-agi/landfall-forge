# landfall-audit - Check landfall quality and coverage

## Trigger

Use this when the user asks whether a repo's landfalls are good, complete, overlapping, stale, or correctly written.

## Instructions

1. List `landfalls/*.yaml`.
2. For each landfall, check:
   - has unique purpose
   - declares a valid size: `micro`, `focused`, `broad`, or `strategic`
   - includes inference notes and alternatives considered
   - has `when_to_run`
   - has ownership and non-ownership boundary
   - has split/expand hints when scope may drift
   - lists concrete sources
   - asks operational questions
   - declares write targets
   - includes human-only stop conditions
   - defines done criteria
3. Compare landfalls against repo responsibilities and recent repeated work.
4. Flag:
   - missing landfalls
   - overlapping landfalls
   - landfalls that are too broad for their purpose
   - landfalls that are too small to answer their stated questions
   - vague source definitions
   - no write targets
   - unsafe missing stop conditions
   - landfalls that cannot be run because required CLIs/tools are missing

## Output

```text
Landfall audit: <repo>

PASS:
- <landfall>

WARN:
- <issue>

FAIL:
- <issue>

Recommended fixes:
1. <fix>
```

## Rules

- Read-only unless the user asks to fix.
- A landfall without write targets is only a checklist; flag it.
- A landfall without stop conditions is unsafe; flag it.
- A landfall without size is ambiguous; flag it.
- A landfall that does not preserve alternatives considered will be hard to refine later; warn on it.
