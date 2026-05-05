# landfall-run - Execute a repo-local landfall

## Trigger

Use this when the user asks to run, make, or perform landfall in a repo.

## Instructions

1. Load `landfalls/<name>.yaml`.
2. Restate the landfall's purpose, size, and stop conditions in one sentence.
3. Refresh each source listed in the YAML:
   - local repo paths
   - email commands
   - messages commands
   - finance commands
   - calendar checks
   - safe portal/document checks
4. Answer every question in the `questions:` section.
5. Check whether the landfall is still the right size:
   - If too small, record what broader landfall should run next.
   - If too broad, record what smaller landfall should be split out.
6. Update the listed write targets when evidence is strong:
   - task list
   - evidence files
   - payables
   - wiki summaries
   - calendar notes
7. If evidence is weak, record the uncertainty instead of closing the task.
8. Stop before human-only actions.
9. Finish with:
   - whether this landfall was the right size
   - new facts
   - repo updates made
   - human-only actions
   - next 3-5 actions

## Rules

- Evidence before action.
- Do not submit payments, legal forms, identity checks, credentials, MFA, or bank/wire information.
- A landfall is allowed to update tasks when the evidence is strong enough.
- If source commands fail, record the failure and its consequence.
