# landfall-forge

Landfall-forge is a knowledge forge for designing, auditing, and running repo-local landfalls.

## What This Forge Contains

- `.claude/skills/landfall-design.md` - design a named landfall and write it to a repo.
- `.claude/skills/landfall-run.md` - execute a landfall from a repo-local definition.
- `.claude/skills/landfall-audit.md` - check whether a repo has the right landfalls and whether each is well formed.
- `.claude/skills/landfall-map.md` - inventory candidate landfalls for a repo.
- `templates/landfall.yaml` - portable landfall definition template.

## Repo Writing Contract

Landfalls are written into the target repo under:

```text
landfalls/
  README.md
  <landfall-name>.yaml
```

Use `landfalls/*.yaml` for definitions. Use the repo's existing wiki/tasks/payables/calendar/doc surfaces for outputs. The landfall definition should point to those outputs; it should not invent a shadow project system.

## Guardrails

- Do not create software in this forge.
- Do not treat one landfall as universal.
- Do not hide source refresh logic in prose only; encode it in the YAML.
- Stop on human-only actions: credentials, MFA, identity verification, bank/wire data, legal judgment, and money movement.

