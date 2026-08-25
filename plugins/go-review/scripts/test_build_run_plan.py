from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import build_run_plan


class BuildRunPlanTests(unittest.TestCase):
    def test_library_without_service_selects_other_capabilities(self) -> None:
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / "prompts/clusters/manifest.json").read_text())
        flags = dict.fromkeys(build_run_plan.CAPABILITY_FLAGS, False)
        flags["has_crypto_auth"] = True

        selected = build_run_plan.build_selection(
            manifest, plugin_root=root, flags=flags, threat_model="BOTH"
        )

        self.assertEqual([item["cluster_id"] for item in selected], ["crypto-session"])

    def test_package_with_no_detected_capabilities_has_empty_plan(self) -> None:
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / "prompts/clusters/manifest.json").read_text())
        flags = dict.fromkeys(build_run_plan.CAPABILITY_FLAGS, False)
        self.assertEqual(
            build_run_plan.build_selection(
                manifest, plugin_root=root, flags=flags, threat_model="BOTH"
            ),
            [],
        )

    def test_empty_plan_does_not_create_cache_primer(self) -> None:
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            (output / "context.md").write_text("---\nseverity_filter: all\n---\n")
            args = [
                "--plugin-root",
                str(root),
                "--output-dir",
                str(output),
                "--threat-model",
                "BOTH",
                "--severity-filter",
                "all",
                "--scope-subpath",
                ".",
            ]
            for flag in build_run_plan.CAPABILITY_FLAGS:
                args.extend([f"--{flag.replace('_', '-')}", "false"])
            self.assertEqual(build_run_plan.main(args), 0)
            plan = json.loads((output / "plan.json").read_text())
            self.assertEqual(plan["workers"], [])
            self.assertNotIn("cache_primer", plan)
            self.assertFalse(plan["run"]["cache_primer"])


if __name__ == "__main__":
    unittest.main()
