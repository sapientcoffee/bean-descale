---
name: adversarial-proofing
description: Test-driven security remediation workflow. Enforces that all security patches are preceded by a failing exploit regression test before verifying clean remediation.
---

<!--
Copyright 2026 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# 🛡️ Skill: Adversarial Proofing (TDD Security Remediation)

You are executing the **Adversarial Proofing** skill. This skill guarantees that no security patch is accepted without empirical verification of vulnerability existence (pre-patch failure) and complete remediation (post-patch success).

## Workflow Protocol

### Step 1: Exploit Test Authoring
Direct the `@security-remediator` subagent to write a targeted regression test reproducing the exploit inside `tests/security/` (e.g. `tests/security/test_cve_replay.py`).

### Step 2: Pre-Patch Failure Verification
Execute the pre-patch verification command using the CLI runner:
```bash
python3 scripts/adversarial_proof.py verify-fail --test-cmd "pytest tests/security/test_cve_replay.py"
```
- **Invariant**: The test **MUST FAIL** on unpatched code (exit code != 0). This confirms that the test accurately captures the vulnerability.
- If the test passes prior to patching, it is invalid and must be rewritten.

### Step 3: Surgical Code Remediation
Direct `@security-remediator` to apply the minimal, surgical security patch to the vulnerable component.

### Step 4: Post-Patch Success Verification
Execute the post-patch verification command:
```bash
python3 scripts/adversarial_proof.py verify-pass --test-cmd "pytest tests/security/test_cve_replay.py"
```
- **Invariant**: The test **MUST PASS** cleanly (exit code 0).
- If the test fails, remediation is incomplete and the patch must be revised.

### Step 5: Check Proof Status
Verify overall proof log status:
```bash
python3 scripts/adversarial_proof.py status
```
Logs are preserved in `.security-audit/adversarial_proof.json`.
