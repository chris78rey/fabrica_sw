import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from fabrica_sw.safe_factory_tools import execute_test_command


class ExecuteTestCommandTests(unittest.TestCase):
    def test_runs_allowed_command_without_shell(self):
        completed = subprocess.CompletedProcess(
            args=["python", "-m", "unittest", "discover", "-q"],
            returncode=0,
            stdout="ok\n",
            stderr="",
        )
        with patch("fabrica_sw.safe_factory_tools.subprocess.run", return_value=completed) as run:
            result = execute_test_command(["python", "-m", "unittest", "discover", "-q"])

        self.assertIn("--- STDOUT ---\nok", result)
        self.assertIn("código de salida 0", result)
        run.assert_called_once_with(
            ["python", "-m", "unittest", "discover", "-q"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(Path.cwd().resolve()),
            shell=False,
            check=False,
        )

    def test_rejects_empty_or_invalid_arguments(self):
        self.assertIn("No se proporcionaron", execute_test_command([]))
        self.assertIn("No se proporcionaron", execute_test_command("python"))
        self.assertIn("textos no vacíos", execute_test_command(["python", ""]))

    def test_rejects_command_outside_allowlist(self):
        with patch("fabrica_sw.safe_factory_tools.subprocess.run") as run:
            result = execute_test_command(["powershell", "-Command", "Write-Output unsafe"])
        self.assertIn("Acceso Denegado", result)
        run.assert_not_called()

    def test_rejects_python_code_execution(self):
        with patch("fabrica_sw.safe_factory_tools.subprocess.run") as run:
            result = execute_test_command(["python", "-c", "print('unsafe')"])
        self.assertIn("Acceso Denegado", result)
        run.assert_not_called()

    def test_reports_timeout(self):
        with patch(
            "fabrica_sw.safe_factory_tools.subprocess.run",
            side_effect=subprocess.TimeoutExpired(["python", "-m", "unittest"], 30),
        ):
            result = execute_test_command(["python", "-m", "unittest"])
        self.assertIn("Tiempo de espera agotado (30s)", result)


if __name__ == "__main__":
    unittest.main()
