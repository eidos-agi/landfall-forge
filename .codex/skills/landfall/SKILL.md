---
name: landfall
description: >-
  Use when the user asks to run, design, map, audit, or rely on landfalls in a repo.
  A landfall is a repo-local arrival ritual: refresh the right sources, compare them
  to current repo state, update declared task/wiki/evidence/payable surfaces, and
  stop before human-only actions. If the repo has no landfall definitions, fall back
  through forge-forge to find landfall-forge and design repo-local landfalls instead
  of inventing a generic one.
---

# Landfall

## Core Rule

The skill is universal; the landfalls are local.

Do not put domain-specific behavior in this skill. Read it from the current repo's `landfalls/` directory. If the repo has no landfalls, use `landfall` / `forge-forge` to locate `landfall-forge`, then map/design landfalls for this repo.

## CLI Front Door

Prefer the `landfall` CLI first:

```bash
landfall doctor
landfall list
landfall brief <name-or-request>
landfall audit
```

The CLI is not the domain brain. It is the router:

- local repo has `landfalls/*.yaml` -> read and brief those contracts
- local repo has no landfalls -> call forge-forge for `landfall-forge`
- ambiguous request -> infer the best local landfall from the user's wording and the YAML identity/purpose

After `landfall brief` or `landfall run`, the LLM executes the brief safely. The CLI intentionally does not submit forms, move money, send messages, or make legal/tax/financial judgments.

## Workflow

1. Identify the current repo root.
2. Run `landfall doctor` if available.
3. Look for:
   - `landfalls/README.md`
   - `landfalls/*.yaml`
4. If landfalls exist:
   - read the relevant YAML definitions
   - use `landfall brief <request>` to choose/brief when the right landfall is not obvious
   - infer the best fit from the user's request, browser context, recent repo state, and source freshness
   - if ambiguous, present 2-4 options by size: `micro`, `focused`, `broad`, `strategic`
   - run the selected landfall
5. If no landfalls exist:
   - do not improvise a hidden task system
   - run `landfall forge-info` or ask `forge-forge` for `landfall-forge`
   - use `landfall-forge`'s map/design pattern to create repo-local `landfalls/` definitions
6. Write results only to the repo surfaces declared by the landfall:
   - tasks
   - wiki/work notes
   - evidence files
   - payables/status data
   - calendar notes or drafts when explicitly listed
7. Stop before human-only actions.

## Forge-Fallback Commands

Try these in order when a repo has no usable `landfalls/` directory:

```bash
forge info landfall-forge
```

If `forge` is not on `PATH`, try Daniel's common local checkout:

```bash
~/repos-eidos-agi/forge-forge/.venv/bin/forge info landfall-forge
```

If that works, read or copy the forge patterns from:

```text
~/repos-eidos-agi/landfall-forge/.claude/skills/landfall-map.md
~/repos-eidos-agi/landfall-forge/.claude/skills/landfall-design.md
~/repos-eidos-agi/landfall-forge/.claude/skills/landfall-run.md
~/repos-eidos-agi/landfall-forge/.claude/skills/landfall-audit.md
~/repos-eidos-agi/landfall-forge/templates/landfall.yaml
~/repos-eidos-agi/landfall-forge/templates/landfalls-README.md
```

If local checkout paths differ, use the repo named by `forge info landfall-forge`.

## Running An Existing Landfall

For a repo-local landfall:

1. Load `landfalls/<name>.yaml`.
2. Restate its purpose, size, and stop conditions in one sentence.
3. Refresh the YAML-listed sources:
   - repo files
   - email commands
   - message commands
   - finance commands
   - calendar checks
   - safe portal/document checks
4. Answer every listed question.
5. Check whether the landfall is still the right size.
6. Update declared write targets only when evidence is strong.
7. If evidence is weak, record uncertainty instead of closing the task.
8. Finish with:
   - whether this was the right size
   - new facts
   - repo updates made
   - human-only actions
   - next 3-5 actions

## Designing A Missing Landfall

When creating a new repo-local landfall:

1. Read the repo's existing operating surfaces before writing.
2. Infer candidate landfalls from repeated user steering, stale state, source-refresh pain, human-only boundaries, and current context.
3. Offer at least one smaller and one larger shape before recommending one.
4. Name by job, not storage: `payables-landfall`, not `json-landfall`.
5. Create or update:
   - `landfalls/README.md`
   - `landfalls/<name>.yaml`
6. Use the repo's existing task/wiki/evidence/payable systems as write targets.

## Human-Only Stop Conditions

Stop before:

- credentials
- MFA or one-time codes
- identity verification
- legal certifications or signatures
- tax/legal/financial judgment calls
- bank details or wire instructions
- payment submission or money movement
- irreversible portal submission

Record the stop, the evidence, and the exact next human action.

## Anti-Patterns

- Do not make one universal landfall for every repo.
- Do not make a second hidden task system.
- Do not bury source refresh commands in prose if a YAML should own them.
- Do not silently choose topology when size/scope is ambiguous.
- Do not close tasks from weak evidence.
