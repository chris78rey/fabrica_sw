import tempfile
import unittest
from pathlib import Path

from fabrica_sw.test_profiles import detect_test_command


class TestProfileDetectionTests(unittest.TestCase):
    def test_detects_common_project_commands(self):
        cases = {
            "package.json": ["npm", "test"],
            "go.mod": ["go", "test", "./..."],
            "Cargo.toml": ["cargo", "test"],
            "pom.xml": ["mvn", "test", "-q"],
            "project.godot": ["godot", "--headless", "--path", ".", "--editor", "--quit"],
        }
        for marker, expected in cases.items():
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as directory:
                Path(directory, marker).write_text("", encoding="utf-8")
                self.assertEqual(detect_test_command(Path(directory)), expected)

    def test_detects_python_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "tests").mkdir()
            self.assertEqual(
                detect_test_command(Path(directory)),
                ["python", "-m", "unittest", "discover", "-s", "tests", "-q"],
            )


if __name__ == "__main__":
    unittest.main()
