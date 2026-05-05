# landfall-design - Write a repo-local landfall definition

## Trigger

Use this when the user asks to create, define, write, or formalize a landfall for a repo.

## Instructions

1. Identify the target repo and the landfall's unique purpose.
2. Check for existing landfalls:
   ```bash
   find landfalls -maxdepth 1 -type f -name '*.yaml' 2>/dev/null
   ```
3. Read the user's current ask, recent steering, and repo context. Infer what kind of landfall the user probably needs, then suggest options:
   - `micro`: smallest safe ritual
   - `focused`: one workstream
   - `broad`: one domain
   - `strategic`: whole operating picture
4. Recommend one shape and explain why.
5. Decide the boundary:
   - What this landfall owns.
   - What adjacent landfalls own.
   - Which human-only actions force a stop.
6. Create `landfalls/` if missing.
7. If `landfalls/README.md` is missing, create it from `templates/landfalls-README.md`.
8. Write `landfalls/<name>.yaml` from `templates/landfall.yaml`.
9. Include:
   - `size`
   - `inference.why_this_landfall_probably_exists`
   - `inference.alternatives_considered`
   - `scope.can_expand_to`
   - `scope.can_split_into`
10. Add source commands that are real for the repo, such as `reeves-email`, `reeves-messages`, `reeves-finance`, calendar tools, local files, or portal URLs.
11. Add write targets that match the repo's existing task/wiki/payable structure.
12. Run a quick audit of the new definition.

## Rules

- Do not create a generic catch-all landfall if the repo needs several named landfalls.
- Do not invent a new task system. Point to the repo's existing task surface.
- Do not hide source refresh in prose. Put commands and search terms in YAML.
- Stop conditions must include credentials, MFA, identity verification, bank/wire details, legal judgment, and payment submission when relevant.
- Landfall topology is a design decision. Infer, suggest options, then recommend.
- Variable size is allowed; unclear size is not.
