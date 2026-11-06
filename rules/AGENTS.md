# Bean-Descale Agent & Skill Routing Rules

## Subagents
All local subagents in `agents/*.md` use `kind: local`, `subagent: true`, `mainAgent: false`, `model: inherit`, and normalized tool names (`read_file`, `write_file`, `edit_file`, `run_command`):
- `vulnerability-scanner`: Read-only static vulnerability and QA scanner (`tools: [read_file]`).
- `killchain-analyzer`: Synthesizes end-to-end attack trees into `docs/security/attack_tree.md` (`tools: [read_file, write_file, run_command]`).
- `security-remediator`: Implements surgical security patches and validates exploit tests (`tools: [read_file, edit_file, write_file, run_command]`).

## Skills
- `adversarial-proofing`: Enforces pre-patch failing exploit tests and post-patch passing verification via `skills/adversarial-proofing/scripts/adversarial_proof.py`.
- `harness-immunizer`: Writes self-healing gotcha rules into the target workspace's `.agents/rules/gotchas/<slug>.md` (configurable via `--output-dir`, defaulting to `.agents/rules/gotchas`) via `skills/harness-immunizer/scripts/immunize_harness.py`.
