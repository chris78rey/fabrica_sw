import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from fabrica_sw.architect import ARCHITECT_TOOLS, architect_node


class FakeResponse:
    content = "Plan arquitectónico seguro"


class JsonResponse:
    content = '{"summary":"Cambio seguro","impacted_files":["src/auth.py"],"dependencies":["db"],"rules":["mantener API"]}'


class FakeModel:
    def __init__(self):
        self.bound_tools = None
        self.messages = None

    def bind_tools(self, tools):
        self.bound_tools = tools
        return self

    def invoke(self, messages):
        self.messages = messages
        return FakeResponse()


class JsonModel(FakeModel):
    def invoke(self, messages):
        self.messages = messages
        return JsonResponse()


class ArchitectNodeTests(unittest.TestCase):
    def test_consults_graphify_before_invoking_model(self):
        model = FakeModel()
        with patch(
            "fabrica_sw.architect.graphify_query_tool",
            return_value="Graphify: auth.py depende de db.py",
        ) as query:
            result = architect_node({"user_requirement": "reforzar autenticación"}, model)

        query.assert_called_once()
        self.assertEqual("planned", result["architecture_blueprint"]["status"])
        self.assertIn("Graphify", model.messages[1]["content"])
        self.assertEqual("Plan arquitectónico seguro", result["architecture_blueprint"]["last_architect_thought"])
        bound_names = {getattr(tool, "name", getattr(tool, "__name__", "")) for tool in model.bound_tools}
        expected_names = {getattr(tool, "name", getattr(tool, "__name__", "")) for tool in ARCHITECT_TOOLS}
        self.assertEqual(bound_names, expected_names)
        self.assertNotIn("write_file_tool", bound_names)

    def test_parses_structured_blueprint(self):
        with patch("fabrica_sw.architect.graphify_query_tool", return_value="contexto"):
            result = architect_node({"user_requirement": "reforzar autenticación"}, JsonModel())

        blueprint = result["architecture_blueprint"]
        self.assertEqual(["src/auth.py"], blueprint["impacted_files"])
        self.assertEqual(["db"], blueprint["dependencies"])
        self.assertIn("mantener API", blueprint["rules"])
        self.assertEqual("Cambio seguro", blueprint["summary"])

    def test_runs_without_langchain_model(self):
        with patch("fabrica_sw.architect.graphify_query_tool", return_value="contexto local"):
            result = architect_node({"user_requirement": "crear endpoint"})

        self.assertEqual([], result["architecture_blueprint"]["impacted_files"])
        self.assertIn("contexto local", result["architecture_blueprint"]["last_architect_thought"])

    def test_rejects_blank_requirement(self):
        with self.assertRaisesRegex(ValueError, "user_requirement"):
            architect_node({"user_requirement": " "})


if __name__ == "__main__":
    unittest.main()
