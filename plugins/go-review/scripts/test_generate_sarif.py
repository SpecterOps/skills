from __future__ import annotations

import unittest

import generate_sarif


class SeverityFilterTests(unittest.TestCase):
    def test_all_includes_low(self) -> None:
        self.assertTrue(generate_sarif.severity_allowed("LOW", "all"))

    def test_medium_excludes_low(self) -> None:
        self.assertFalse(generate_sarif.severity_allowed("LOW", "medium"))
        self.assertTrue(generate_sarif.severity_allowed("MEDIUM", "medium"))

    def test_high_excludes_medium(self) -> None:
        self.assertFalse(generate_sarif.severity_allowed("MEDIUM", "high"))
        self.assertTrue(generate_sarif.severity_allowed("HIGH", "high"))


if __name__ == "__main__":
    unittest.main()
