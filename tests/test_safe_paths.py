import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from fabrica_sw.safe_paths import validate_safe_path


class SafePathTests(unittest.TestCase):
    def test_relative_path_inside_workspace_is_allowed(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir).resolve()
            self.assertEqual(
                validate_safe_path(workspace / "src" / "module.py", workspace),
                workspace / "src" / "module.py",
            )

    def test_parent_escape_is_rejected(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir).resolve()
            with self.assertRaisesRegex(ValueError, "fuera del directorio"):
                validate_safe_path(workspace / ".." / "outside.txt", workspace)

    def test_absolute_path_outside_workspace_is_rejected(self) -> None:
        with TemporaryDirectory() as workspace_dir, TemporaryDirectory() as outside_dir:
            outside_path = Path(outside_dir) / "secret.txt"
            with self.assertRaises(ValueError):
                validate_safe_path(outside_path, workspace_dir)

    def test_symlink_to_external_target_is_rejected_when_supported(self) -> None:
        with TemporaryDirectory() as workspace_dir, TemporaryDirectory() as outside_dir:
            workspace = Path(workspace_dir)
            outside = Path(outside_dir)
            external_file = outside / "secret.txt"
            external_file.write_text("secret", encoding="utf-8")
            link = workspace / "link.txt"
            try:
                link.symlink_to(external_file)
            except (OSError, NotImplementedError):
                self.skipTest("El sistema no permite crear enlaces simbólicos")
            with self.assertRaises(ValueError):
                validate_safe_path(link, workspace)

    def test_blank_path_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_safe_path(" ")


if __name__ == "__main__":
    unittest.main()
