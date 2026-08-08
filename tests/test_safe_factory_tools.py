import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from fabrica_sw.safe_factory_tools import (
    list_directory_tool,
    read_file_tool,
    write_file_tool,
)
import fabrica_sw.safe_paths as safe_paths


class SafeFactoryToolsTests(unittest.TestCase):
    def workspace(self):
        return TemporaryDirectory()

    def test_read_file_returns_utf8_content(self):
        with self.workspace() as temp_dir:
            workspace = Path(temp_dir)
            target = workspace / "docs" / "requisitos.txt"
            target.parent.mkdir()
            target.write_text("seguridad y ñandú", encoding="utf-8")
            with patch.object(safe_paths, "WORKSPACE_DIR", workspace):
                self.assertEqual(read_file_tool(str(target)), "seguridad y ñandú")

    def test_read_file_reports_missing_and_directory(self):
        with self.workspace() as temp_dir:
            workspace = Path(temp_dir)
            with patch.object(safe_paths, "WORKSPACE_DIR", workspace):
                self.assertIn("no existe", read_file_tool(str(workspace / "missing.txt")))
                self.assertIn("no es un archivo", read_file_tool(str(workspace)))

    def test_write_file_creates_parent_directories(self):
        with self.workspace() as temp_dir:
            workspace = Path(temp_dir)
            target = workspace / "src" / "nested" / "module.py"
            with patch.object(safe_paths, "WORKSPACE_DIR", workspace):
                result = write_file_tool(str(target), "print('hola')\n")
            self.assertIn("Archivo escrito correctamente", result)
            self.assertEqual(target.read_text(encoding="utf-8"), "print('hola')\n")

    def test_directory_listing_is_sorted_and_typed(self):
        with self.workspace() as temp_dir:
            workspace = Path(temp_dir)
            (workspace / "z.txt").write_text("z", encoding="utf-8")
            (workspace / "a.txt").write_text("a", encoding="utf-8")
            (workspace / "docs").mkdir()
            with patch.object(safe_paths, "WORKSPACE_DIR", workspace):
                result = list_directory_tool(str(workspace))
            self.assertEqual(result.splitlines(), ["[FILE] a.txt", "[DIR] docs", "[FILE] z.txt"])

    def test_all_file_tools_reject_external_paths(self):
        with self.workspace() as workspace_dir, self.workspace() as outside_dir:
            workspace = Path(workspace_dir)
            outside = Path(outside_dir) / "outside.txt"
            with patch.object(safe_paths, "WORKSPACE_DIR", workspace):
                self.assertIn("Error leyendo", read_file_tool(str(outside)))
                self.assertIn("Error escribiendo", write_file_tool(str(outside), "no"))
                self.assertIn("Error listando", list_directory_tool(str(outside_dir)))


if __name__ == "__main__":
    unittest.main()
