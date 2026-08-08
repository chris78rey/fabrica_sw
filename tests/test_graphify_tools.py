import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from fabrica_sw.safe_factory_tools import (
    graphify_query_tool,
    graphify_shortest_path_tool,
)
import fabrica_sw.safe_factory_tools as safe_tools


class GraphifyToolsTests(unittest.TestCase):
    def test_query_reports_missing_graph(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_graph = Path(temp_dir) / "graph.json"
            with patch.object(safe_tools, "GRAPH_PATH", missing_graph), patch(
                "fabrica_sw.safe_factory_tools.subprocess.run"
            ) as run:
                result = graphify_query_tool("¿Cómo se relacionan auth y db?")
        self.assertIn("No se encuentra graphify-out/graph.json", result)
        run.assert_not_called()

    def test_query_invokes_project_graphify(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            graph_path = Path(temp_dir) / "graph.json"
            graph_path.write_text("{}", encoding="utf-8")
            completed = subprocess.CompletedProcess(
                args=[], returncode=0, stdout="resultado\n", stderr=""
            )
            with patch.object(safe_tools, "GRAPH_PATH", graph_path), patch(
                "fabrica_sw.safe_factory_tools.subprocess.run",
                return_value=completed,
            ) as run:
                result = graphify_query_tool("¿Cómo se relacionan auth y db?")
        self.assertEqual("resultado\n", result)
        run.assert_called_once_with(
            [safe_tools.GRAPHIFY_COMMAND, "query", "¿Cómo se relacionan auth y db?", "--graph", str(graph_path)],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(safe_tools.WORKSPACE_COMMAND_DIR),
            shell=False,
            check=False,
        )

    def test_query_reports_cli_error_and_validates_question(self):
        self.assertIn("texto no vacío", graphify_query_tool(" "))
        completed = subprocess.CompletedProcess(
            args=[], returncode=2, stdout="", stderr="consulta inválida"
        )
        with patch("fabrica_sw.safe_factory_tools.subprocess.run", return_value=completed):
            result = graphify_query_tool("pregunta")
        self.assertIn("consulta inválida", result)

    def test_shortest_path_invokes_project_graphify(self):
        completed = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="auth -> db\n", stderr=""
        )
        with patch("fabrica_sw.safe_factory_tools.subprocess.run", return_value=completed) as run:
            result = graphify_shortest_path_tool("auth", "db")
        self.assertEqual("auth -> db\n", result)
        self.assertEqual(
            [safe_tools.GRAPHIFY_COMMAND, "path", "auth", "db", "--graph", str(safe_tools.GRAPH_PATH)],
            run.call_args.args[0],
        )
        self.assertEqual(15, run.call_args.kwargs["timeout"])

    def test_shortest_path_validates_symbols(self):
        self.assertIn("source_symbol", graphify_shortest_path_tool("", "db"))
        self.assertIn("target_symbol", graphify_shortest_path_tool("auth", ""))


if __name__ == "__main__":
    unittest.main()
