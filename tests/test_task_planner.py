import unittest

from fabrica_sw.task_planner import build_tasks


class TaskPlannerTests(unittest.TestCase):
    def test_extracts_checkbox_tasks_and_status(self):
        tasks = build_tasks("""# Plan
- [ ] Crear escena
- [x] Configurar proyecto
""")

        self.assertEqual([task["id"] for task in tasks], ["TASK-001", "TASK-002"])
        self.assertFalse(tasks[0]["completed"])
        self.assertTrue(tasks[1]["completed"])

    def test_extracts_numbered_requirements(self):
        tasks = build_tasks("""1. Crear jugador
2. Añadir puntuación
""")

        self.assertEqual([task["title"] for task in tasks], ["Crear jugador", "Añadir puntuación"])

    def test_creates_fallback_task_for_plain_requirement(self):
        tasks = build_tasks("Crear un inventario funcional")

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["id"], "TASK-001")
        self.assertEqual(tasks[0]["title"], "Crear un inventario funcional")


if __name__ == "__main__":
    unittest.main()
