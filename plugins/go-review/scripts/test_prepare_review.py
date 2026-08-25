from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import prepare_review


class PrepareReviewTests(unittest.TestCase):
    def test_creates_portable_artifact_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "results"

            def fake_run(command: list[str], **kwargs: object) -> object:
                check = kwargs["check"]
                self.assertFalse(check)
                inventory_path = Path(command[command.index("--output") + 1])
                inventory_path.write_text(
                    json.dumps({"summary": {"go_file_count": 2, "package_count": 1}})
                )
                self.assertIn("GOCACHE", kwargs["env"])
                return mock.Mock(returncode=0, stdout="{}\n", stderr="")

            with mock.patch("prepare_review.subprocess.run", side_effect=fake_run):
                self.assertEqual(
                    prepare_review.main(
                        ["--repo-root", tmp, "--scope-subpath", ".", "--output-dir", str(output)]
                    ),
                    0,
                )

            for name in ("findings", "findings-index.d", "coverage"):
                self.assertTrue((output / name).is_dir())
            self.assertTrue((output / "go-inventory.json").is_file())


if __name__ == "__main__":
    unittest.main()
