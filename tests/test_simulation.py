import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import simulate_factory_run


class SimulationCleanupTests(unittest.TestCase):
    def test_simulation_removes_temporary_sandbox(self):
        with tempfile.TemporaryDirectory(
            dir=simulate_factory_run.PROJECT_ROOT,
            prefix="test_simulation_",
        ) as temp_dir:
            sandbox = Path(temp_dir) / "sandbox_test_repo"
            requirements = sandbox / "requirements_checklist.txt"
            source = sandbox / "auth_security.py"

            with patch.object(simulate_factory_run, "SANDBOX", sandbox), patch.object(
                simulate_factory_run, "REQUIREMENTS", requirements
            ), patch.object(simulate_factory_run, "SOURCE", source):
                self.assertEqual(simulate_factory_run.main(), 0)

            self.assertFalse(sandbox.exists())


if __name__ == "__main__":
    unittest.main()
