# Bean-Descale: SRE & Security Hardening Rules

Welcome to **Bean-Descale**, the adversarial security proofing and harness self-healing toolkit for Antigravity (`agy`).

## 1. Safety and Stability
* **Non-Destructive Scanning:** Assessment and scanning tools (`@vulnerability-scanner`) must operate read-only unless an explicit remediation plan is approved.
* **Adversarial Proofing:** Never apply a security patch without proving vulnerability reproduction via a failing test in `tests/security/`, and verifying it passes cleanly post-patch (`skills/adversarial-proofing`).
* **Harness Self-Healing:** When remediation failure loops repeat (>2 retries), trigger `skills/harness-immunizer` (`skills/harness-immunizer/scripts/immunize_harness.py`) to persist an architectural constraint in the target workspace's `.agents/rules/gotchas/<slug>.md` (never mutating the plugin's own directory).
