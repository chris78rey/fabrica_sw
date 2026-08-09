import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from fabrica_sw.safe_factory_tools import (
    SAFE_DEVELOPMENT_TOOLS,
    execute_test_command,
    install_project_dependencies_tool,
    graphify_query_tool,
    graphify_shortest_path_tool,
    list_directory_tool,
    read_file_tool,
    write_file_tool,
)


class ToolRegistryTests(unittest.TestCase):
    def test_registers_all_safe_tools_in_documented_order(self):
        self.assertEqual(
            [
                read_file_tool,
                write_file_tool,
                list_directory_tool,
                execute_test_command,
                install_project_dependencies_tool,
                graphify_query_tool,
                graphify_shortest_path_tool,
            ],
            SAFE_DEVELOPMENT_TOOLS,
        )

    def test_registry_contains_unique_callables(self):
        self.assertEqual(len(SAFE_DEVELOPMENT_TOOLS), len(set(SAFE_DEVELOPMENT_TOOLS)))
        self.assertTrue(all(callable(tool) for tool in SAFE_DEVELOPMENT_TOOLS))


if __name__ == "__main__":
    unittest.main()
