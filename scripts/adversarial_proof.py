#!/usr/bin/env python3
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Adversarial Proofing CLI Runner.
Enforces test-driven security remediation:
Phase 1 (verify-fail): Exploit test runs against unpatched code and MUST FAIL (exit code != 0).
Phase 2 (verify-pass): Exploit test runs against patched code and MUST PASS (exit code == 0).
"""

import argparse
import datetime
import json
import os
import subprocess
import sys


def load_state(state_file: str) -> dict:
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "status": "INITIALIZED",
        "fail_verified": False,
        "pass_verified": False,
        "history": [],
    }


def save_state(state_file: str, state: dict):
    os.makedirs(os.path.dirname(os.path.abspath(state_file)), exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def run_command(cmd_str: str, cwd: str) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd_str,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=180,
        )
        return proc.returncode, proc.stdout
    except subprocess.TimeoutExpired:
        return -1, "Command execution timed out after 180s."
    except Exception as e:
        return -1, f"Failed to execute command: {e}"


def main():
    parser = argparse.ArgumentParser(description="Adversarial Proofing Runner for Security Remediations")
    subparsers = parser.add_subparsers(dest="command")

    # verify-fail
    fail_parser = subparsers.add_parser("verify-fail", help="Verify exploit test FAILS on unpatched code")
    fail_parser.add_argument("--test-cmd", required=True, help="Test command to execute")
    fail_parser.add_argument("--proof-dir", default=".security-audit", help="Directory to store proof logs")

    # verify-pass
    pass_parser = subparsers.add_parser("verify-pass", help="Verify exploit test PASSES on patched code")
    pass_parser.add_argument("--test-cmd", required=True, help="Test command to execute")
    pass_parser.add_argument("--proof-dir", default=".security-audit", help="Directory to store proof logs")

    # status
    status_parser = subparsers.add_parser("status", help="Check current proofing status")
    status_parser.add_argument("--proof-dir", default=".security-audit", help="Directory to store proof logs")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    proof_dir = os.path.abspath(args.proof_dir)
    state_file = os.path.join(proof_dir, "adversarial_proof.json")
    state = load_state(state_file)

    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    if args.command == "verify-fail":
        print(f"[adversarial-proofing] Executing pre-patch test: {args.test_cmd}")
        code, output = run_command(args.test_cmd, cwd=os.getcwd())
        print(output)
        if code != 0:
            print(f"[adversarial-proofing] ✅ SUCCESS: Exploit test failed as expected (exit code {code}). Flaw reproduced.")
            state["fail_verified"] = True
            state["status"] = "FAIL_VERIFIED_AWAITING_PATCH"
            state["history"].append({
                "phase": "verify-fail",
                "timestamp": now_iso,
                "command": args.test_cmd,
                "exit_code": code,
                "result": "PASSED_EXPECTED_FAILURE",
            })
            save_state(state_file, state)
            sys.exit(0)
        else:
            print("[adversarial-proofing] ❌ ERROR: Exploit test passed unexpectedly on unpatched code! Test does not reproduce vulnerability.")
            sys.exit(1)

    elif args.command == "verify-pass":
        if not state.get("fail_verified"):
            print("[adversarial-proofing] ⚠️ WARNING: Phase 1 (verify-fail) has not been verified! You must prove exploit failure before validating fix.")
        print(f"[adversarial-proofing] Executing post-patch test: {args.test_cmd}")
        code, output = run_command(args.test_cmd, cwd=os.getcwd())
        print(output)
        if code == 0:
            print(f"[adversarial-proofing] ✅ SUCCESS: Exploit test passed cleanly (exit code 0). Flaw successfully remediated.")
            state["pass_verified"] = True
            state["status"] = "REMEDIATION_PROOF_COMPLETE" if state.get("fail_verified") else "PASS_VERIFIED_WITHOUT_FAIL_PROOF"
            state["history"].append({
                "phase": "verify-pass",
                "timestamp": now_iso,
                "command": args.test_cmd,
                "exit_code": code,
                "result": "PASSED_CLEAN",
            })
            save_state(state_file, state)
            sys.exit(0)
        else:
            print(f"[adversarial-proofing] ❌ ERROR: Exploit test failed after patch (exit code {code}). Fix is incomplete.")
            sys.exit(1)

    elif args.command == "status":
        print(f"Adversarial Proofing Status: {state.get('status')}")
        print(f"Pre-Patch Failure Proven: {state.get('fail_verified')}")
        print(f"Post-Patch Success Proven: {state.get('pass_verified')}")


if __name__ == "__main__":
    main()
