# ☕ Bean-Descale

> **Security Operations, Killchain Analysis & Harness Gotcha Immunity Engine.**

---

## ☕ Why "The Descaler"?

Over time, espresso machines accumulate limescale and mineral deposits that choke pipes, drop pressure, and sour flavor. Descaling strips away harmful mineral build-up and restores peak performance. In software systems, **`bean-descale`** strips out vulnerabilities, models exploit killchains, enforces adversarial TDD fixes, and inoculates developer environments against repeated bugs by writing self-healing gotcha rules into `.agents/rules/gotchas/`.

---

## 🚀 Capabilities & Agents

| Capability / Agent | Description |
| :--- | :--- |
| **`@killchain-analyzer`** | Synthesizes end-to-end exploit attack trees (`docs/security/attack_tree.md`) from vulnerability scans to pinpoint defense chokepoints. |
| **`@vulnerability-scanner`** | Performs static analysis and pattern matching for OWASP Top 10 vulnerabilities. |
| **`@security-remediator`** | Surgical test-driven security remediation preventing regressions. |
| **`adversarial-proofing`** | Verifies pre-patch exploit failure, surgical fix, and post-patch exploit pass. |
| **`harness-immunizer`** | Evaluates failure root causes on repeated retries (>2) and writes permanent architectural gotcha rules to `.agents/rules/gotchas/<slug>.md`. |

---

## 🛠️ Testing

```bash
python3 -m unittest discover -s tests -v
```
