# 🧼 Bean-Descale: SRE & Resilience Rules

Welcome to **Bean-Descale**, the system resilience and modernization toolkit for the Antigravity CLI (`agy`).

## 1. Safety and Stability
* **Non-Destructive Scanning:** Assessment and scanning tools must operate read-only unless an explicit remediation plan is approved.
* **Verified Security Patches:** Never apply a security patch without running the project's linter and test suite.
* **Incident Post-Mortems:** All chaos events and mitigations must be logged with root cause and runbook remediation steps.
