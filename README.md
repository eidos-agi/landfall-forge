# landfall-forge

Purpose-specific arrival rituals for AI-operated repos.

## What Is A Landfall?

A landfall is what an agent does when it arrives inside a repo before acting. It refreshes the right evidence, compares it to the repo's current operating state, writes durable updates, and produces the next responsibilities.

The important part: a repo can have many landfalls.

For a house-sale repo:

- `closing-landfall` checks closing portal texts, legal emails, DocuSign, calendar, and human-only actions.
- `payables-landfall` checks invoices, finance searches, payment risk, and payables.
- `listing-landfall` checks realtor messages, photos, measurements, market docs, and launch blockers.
- `heather-landfall` checks the Heather thread and drafts one clean status update.

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
- when to run it
- which sources to refresh
- what questions to answer
- where to write findings
- how to update tasks/payables/wiki
- where to stop for human-only actions
- what counts as done

Landfall outputs go into the repo's existing surfaces. A landfall should update the repo's task list, wiki, payables file, calendar note, or evidence folder. It should not create a second hidden task system.

## Skills

| Skill | Purpose |
| --- | --- |
| `landfall-map` | Inventory candidate landfalls for a repo. |
| `landfall-design` | Write a new `landfalls/<name>.yaml` contract. |
| `landfall-run` | Execute a landfall definition and update repo state. |
| `landfall-audit` | Check landfall coverage, quality, and stale outputs. |

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

## License

MIT - Eidos AGI

