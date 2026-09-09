# 🧼 Bean-Descale: SRE & Resilience Rules

Welcome to **Bean-Descale**, the system resilience and modernization toolkit for the Antigravity CLI (`agy`).

## 1. Safety and Stability
* **Non-Destructive Scanning:** Assessment and scanning tools must operate read-only unless an explicit remediation plan is approved.
* **Adversarial Proofing:** Never apply a security patch without proving vulnerability reproduction via a failing test in `tests/security/`, and verifying it passes cleanly post-patch (`skills/adversarial-proofing`).
* **Harness Self-Healing:** When remediation failure loops repeat (>2 retries), trigger `skills/harness-immunizer` to persist an architectural constraint in `rules/gotchas/`.
* **Incident Post-Mortems:** All chaos events and mitigations must be logged with root cause and runbook remediation steps.

