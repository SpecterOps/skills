from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import finalize_run


class FinalizeRunTests(unittest.TestCase):
    def test_empty_plan_creates_complete_empty_report_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            (output / "findings").mkdir()
            (output / "findings-index.d").mkdir()
            (output / "plan.json").write_text(json.dumps({"workers": []}))
            with mock.patch("finalize_run.subprocess.run") as run:
                self.assertEqual(finalize_run.main([str(output)]), 0)
            run.assert_called_once()
            self.assertEqual((output / "findings-index.txt").read_text(), "")
            self.assertIn("No capability-gated", (output / "run-summary.md").read_text())
            for name in ("dedup-summary.md", "fp-summary.md", "REPORT.md"):
                self.assertTrue((output / name).is_file())

    def test_orphan_finding_is_retained(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            (output / "findings").mkdir()
            (output / "findings-index.d").mkdir()
            orphan = output / "findings" / "TEST-001.md"
            orphan.write_text("---\nid: TEST-001\n---\n")
            (output / "plan.json").write_text(json.dumps({"workers": []}))
            findings, warnings = finalize_run.reconcile(output)
            self.assertEqual(findings, [orphan.resolve()])
            self.assertTrue(any("orphan finding retained" in item for item in warnings))

    def test_out_of_bounds_shard_path_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            (output / "findings").mkdir()
            (output / "findings-index.d").mkdir()
            (output / "findings-index.d" / "worker-1.txt").write_text("/etc/passwd\n")
            (output / "plan.json").write_text(json.dumps({"workers": [{"worker_n": 1}]}))
            findings, warnings = finalize_run.reconcile(output)
            self.assertEqual(findings, [])
            self.assertTrue(any("out-of-bounds" in item for item in warnings))

    def test_orphan_symlink_outside_findings_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            findings_dir = output / "findings"
            findings_dir.mkdir()
            (output / "findings-index.d").mkdir()
            outside = output / "outside.md"
            outside.write_text("---\nid: OUTSIDE-001\n---\n")
            (findings_dir / "LINK-001.md").symlink_to(outside)
            (output / "plan.json").write_text(json.dumps({"workers": []}))

            findings, warnings = finalize_run.reconcile(output)

            self.assertEqual(findings, [])
            self.assertNotIn(str(outside.resolve()), (output / "findings-index.txt").read_text())
            self.assertTrue(any("out-of-bounds orphan" in item for item in warnings))

    def test_broken_orphan_symlink_keeps_empty_report_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            findings_dir = output / "findings"
            findings_dir.mkdir()
            (output / "findings-index.d").mkdir()
            (findings_dir / "BROKEN-001.md").symlink_to(output / "missing.md")
            (output / "plan.json").write_text(json.dumps({"workers": []}))

            with mock.patch("finalize_run.subprocess.run") as run:
                self.assertEqual(finalize_run.main([str(output)]), 0)

            run.assert_called_once()
            self.assertEqual((output / "findings-index.txt").read_text(), "")
            self.assertTrue(any("out-of-bounds orphan" in item for item in (output / "run-summary.md").read_text().splitlines()))


if __name__ == "__main__":
    unittest.main()
