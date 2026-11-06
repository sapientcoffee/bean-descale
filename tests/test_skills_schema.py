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
Skill, Agent, and Harness Immunizer Test Suite for bean-descale.
"""

import os
import subprocess
import sys
import tempfile
import unittest
import yaml


def find_repo_root():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(script_dir, ".."))


def parse_frontmatter(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if not content.startswith("---"):
        raise ValueError(f"{path} does not start with YAML frontmatter delimiter '---'")
    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{path} frontmatter delimiter '---' is not closed")
    return yaml.safe_load(parts[1]), parts[2]


class TestSkillsSchema(unittest.TestCase):

    def setUp(self):
        self.repo_root = find_repo_root()
        self.skills_dir = os.path.join(self.repo_root, "skills")
        self.agents_dir = os.path.join(self.repo_root, "agents")
        self.rules_dir = os.path.join(self.repo_root, "rules")

    def test_expected_skills_exist_and_removed_absent(self):
        expected = {"adversarial-proofing", "harness-immunizer"}
        actual = {
            d for d in os.listdir(self.skills_dir)
            if os.path.isdir(os.path.join(self.skills_dir, d)) and not d.startswith(".")
        }
        self.assertEqual(actual, expected)
        for removed in ("skills/deploy-app", "skills/dev", "skills/chaos-mitigation", "scripts/adversarial_proof.py", "scripts/immunize_harness.py", "gemini-extension.json"):
            self.assertFalse(os.path.exists(os.path.join(self.repo_root, removed)), f"Removed file still present: {removed}")

    def test_all_skills_have_skill_md_and_valid_frontmatter(self):
        for skill_name in ("adversarial-proofing", "harness-immunizer"):
            skill_md_path = os.path.join(self.skills_dir, skill_name, "SKILL.md")
            with self.subTest(skill=skill_name):
                self.assertTrue(os.path.exists(skill_md_path))
                data, _ = parse_frontmatter(skill_md_path)
                self.assertEqual(data.get("name"), skill_name)
                self.assertTrue(data.get("description"))

    def test_agents_schema_and_normalized_tools(self):
        expected_agents = {"killchain-analyzer.md", "security-remediator.md", "vulnerability-scanner.md"}
        actual_agents = {f for f in os.listdir(self.agents_dir) if f.endswith(".md")}
        self.assertEqual(actual_agents, expected_agents)

        allowed_tools = {"read_file", "write_file", "edit_file", "run_command"}
        for agent_file in sorted(expected_agents):
            agent_path = os.path.join(self.agents_dir, agent_file)
            with self.subTest(agent=agent_file):
                data, body = parse_frontmatter(agent_path)
                self.assertEqual(data.get("kind"), "local")
                self.assertIs(data.get("subagent"), True)
                self.assertIs(data.get("mainAgent"), False)
                self.assertEqual(data.get("model"), "inherit")
                tools = data.get("tools", [])
                self.assertGreater(len(tools), 0)
                for t in tools:
                    self.assertIn(t, allowed_tools, f"Non-normalized tool '{t}' in {agent_file}")
                self.assertGreater(len(body.strip()), 50)

    def test_rules_exist(self):
        for rule_file in ("AGENTS.md", "general.md"):
            rule_path = os.path.join(self.rules_dir, rule_file)
            self.assertTrue(os.path.exists(rule_path))
            with open(rule_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertFalse(content.startswith("---"))

    def test_immunize_harness_writes_to_workspace_output_dir(self):
        script_path = os.path.join(self.skills_dir, "harness-immunizer", "scripts", "immunize_harness.py")
        self.assertTrue(os.path.exists(script_path))

        with tempfile.TemporaryDirectory() as tmpdir:
            # 1. Test default .agents/rules/gotchas in target workspace CWD
            res = subprocess.run(
                [
                    sys.executable,
                    script_path,
                    "--issue-title", "JWT Clock Skew",
                    "--root-cause", "Unsynchronized clocks",
                    "--remediation", "Add 60s leeway",
                    "--rule-slug", "jwt-clock-skew",
                ],
                cwd=tmpdir,
                capture_output=True,
                text=True,
            )
            self.assertEqual(res.returncode, 0, f"stderr: {res.stderr}")
            default_rule = os.path.join(tmpdir, ".agents", "rules", "gotchas", "jwt-clock-skew.md")
            self.assertTrue(os.path.exists(default_rule))

            # 2. Test explicit --output-dir
            custom_dir = os.path.join(tmpdir, "custom-gotchas")
            res2 = subprocess.run(
                [
                    sys.executable,
                    script_path,
                    "--issue-title", "Custom Rule",
                    "--root-cause", "Root cause text",
                    "--output-dir", custom_dir,
                ],
                cwd=tmpdir,
                capture_output=True,
                text=True,
            )
            self.assertEqual(res2.returncode, 0, f"stderr: {res2.stderr}")
            self.assertTrue(os.path.exists(os.path.join(custom_dir, "custom-rule.md")))


if __name__ == "__main__":
    unittest.main()
