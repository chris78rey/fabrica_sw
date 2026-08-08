import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from fabrica_sw.git_policy import ensure_commit_approved


class GitPolicyTests(unittest.TestCase):
    def test_allows_commit_after_explicit_approval(self):
        self.assertIsNone(ensure_commit_approved({"is_approved": True}))

    def test_blocks_commit_without_approval(self):
        with self.assertRaisesRegex(PermissionError, "Commit bloqueado"):
            ensure_commit_approved({"is_approved": False})

    def test_blocks_missing_or_non_boolean_approval(self):
        for value in ({}, {"is_approved": 1}, {"is_approved": "true"}):
            with self.subTest(value=value):
                with self.assertRaises(PermissionError):
                    ensure_commit_approved(value)

    def test_rejects_non_mapping_state(self):
        with self.assertRaises(TypeError):
            ensure_commit_approved(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
