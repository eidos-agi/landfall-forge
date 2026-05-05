# landfall-design - Write a repo-local landfall definition

## Trigger

Use this when the user asks to create, define, write, or formalize a landfall for a repo.

## Instructions

1. Identify the target repo and the landfall's unique purpose.
2. Check for existing landfalls:
   ```bash
   find landfalls -maxdepth 1 -type f -name '*.yaml' 2>/dev/null
   ```
3. Decide the boundary:
   - What this landfall owns.
   - What adjacent landfalls own.
   - Which human-only actions force a stop.
4. Create `landfalls/` if missing.
5. If `landfalls/README.md` is missing, create it from `templates/landfalls-README.md`.
6. Write `landfalls/<name>.yaml` from `templates/landfall.yaml`.
7. Add source commands that are real for the repo, such as `reeves-email`, `reeves-messages`, `reeves-finance`, calendar tools, local files, or portal URLs.
8. Add write targets that match the repo's existing task/wiki/payable structure.
9. Run a quick audit of the new definition.

## Rules

- Do not create a generic catch-all landfall if the repo needs several named landfalls.
- Do not invent a new task system. Point to the repo's existing task surface.
- Do not hide source refresh in prose. Put commands and search terms in YAML.
- Stop conditions must include credentials, MFA, identity verification, bank/wire details, legal judgment, and payment submission when relevant.

