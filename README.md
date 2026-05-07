# landfall-forge

Purpose-specific arrival rituals for AI-operated repos.

## What Is A Landfall?

A landfall is what an agent does when it arrives inside a repo before acting. It refreshes the right evidence, compares it to the repo's current operating state, writes durable updates, and produces the next responsibilities.

The important part: a repo can have many landfalls, and they can be different sizes.

For a house-sale repo:

- `closinglock-landfall` can be tiny: only the secure portal, MFA stops, and open tasks.
- `payables-landfall` can be medium: invoices, finance searches, payment risk, and payables.
- `listing-landfall` can be broad: realtor messages, photos, measurements, market docs, launch blockers, and drafts.
- `house-sale-landfall` can be strategic: the whole operating picture, what changed, what Daniel owns, what must be delegated, and what is unsafe for an agent.

Each landfall has a unique purpose, evidence map, stop conditions, and write targets.

## How Landfalls Are Written To Repos

Target repos carry landfalls under:

```text
landfalls/
  README.md
  closing-landfall.yaml
  payables-landfall.yaml
```

The YAML definition is the contract. It says:

- why the landfall exists
- how large its scope is
- when to run it
- which sources to refresh
- what questions to answer
- where to write findings
- how to update tasks/payables/wiki
- where to stop for human-only actions
- what counts as done

Landfall outputs go into the repo's existing surfaces. A landfall should update the repo's task list, wiki, payables file, calendar note, or evidence folder. It should not create a second hidden task system.

## Size And Scope

Landfalls should be as small as they can be while still doing the job.

| Size | Use When | Example |
| --- | --- | --- |
| `micro` | One notification, portal, person, or payment needs a safe refresh. | `closinglock-landfall` |
| `focused` | One workstream has multiple sources and task outputs. | `payables-landfall` |
| `broad` | A domain needs a full refresh across messages, email, repo, and tasks. | `listing-landfall` |
| `strategic` | The agent needs an operating picture and next responsibilities across the system. | `house-sale-landfall` |

The agent should infer candidate landfalls from the user's past steering, repeated pain, repo shape, task history, and current context. But it should not silently decide the topology. It should suggest options with tradeoffs:

- small and precise
- medium and operational
- broad and coordinating
- strategic and slower

Then it should recommend one.

## Skills

| Skill | Purpose |
| --- | --- |
| `landfall-map` | Inventory candidate landfalls for a repo. |
| `landfall-design` | Write a new `landfalls/<name>.yaml` contract. |
| `landfall-run` | Execute a landfall definition and update repo state. |
| `landfall-audit` | Check landfall coverage, quality, and stale outputs. |

## Codex Skill

This forge also carries a Codex wrapper skill:

```text
.codex/skills/landfall/SKILL.md
```

That skill is intentionally generic. It teaches Codex the landfall protocol, then reads the target repo's own `landfalls/*.yaml` files for domain behavior.

If a target repo has no landfalls yet, the Codex skill falls back to `forge-forge`:

```bash
forge info landfall-forge
```

or, from Daniel's usual local checkout:

```bash
~/repos-eidos-agi/forge-forge/.venv/bin/forge info landfall-forge
```

The fallback exists so agents discover the canonical forge instead of inventing a one-off generic landfall.

## CLI

`landfall` is the universal front door. It is generic on purpose:

- If the current repo has `landfalls/*.yaml`, it reads those definitions.
- If the current repo has no landfalls, it calls `forge-forge` for `landfall-forge` and tells the agent how to design repo-local landfalls.
- It does not contain house-sale, finance, legal, or vendor-specific behavior. That belongs in the target repo's YAML.

Install from the local checkout on Daniel's machine:

```bash
cd ~/repos-eidos-agi/landfall-forge
pipx install -e . --force
```

Homebrew Python may reject direct global `pip install -e .` because of PEP 668. `pipx`
keeps the CLI isolated while still putting `landfall` on PATH.

Then from any repo:

```bash
landfall doctor
landfall list
landfall brief payables-landfall
landfall audit
```

The `run` command is intentionally an agent brief, not a blind automation engine:

```bash
landfall run heather-landfall
```

The LLM executes the brief, refreshes the YAML-listed sources, writes only to declared repo targets, and stops before credentials, MFA, signatures, legal/tax/financial judgment, bank details, wire instructions, payment submission, or irreversible portal submission.

## Usage

Copy or symlink the skills into a project:

```bash
cp ~/repos-eidos-agi/landfall-forge/.claude/skills/landfall-*.md .claude/skills/
```

Then ask an agent:

```text
/landfall-map
/landfall-design payables-landfall
/landfall-run payables-landfall
/landfall-audit
```

For Codex, install or symlink the wrapper skill:

```bash
mkdir -p ~/.codex/skills
ln -s ~/repos-eidos-agi/landfall-forge/.codex/skills/landfall ~/.codex/skills/landfall
```

## License

MIT - Eidos AGI
