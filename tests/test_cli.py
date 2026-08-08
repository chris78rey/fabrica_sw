import unittest

from fabrica_sw.cli import build_parser


class CliTests(unittest.TestCase):
    def test_parser_accepts_repository_and_requirement(self):
        args = build_parser().parse_args(
            ["--repository", ".", "--requirement", "crear una función"]
        )
        self.assertEqual(str(args.repository), ".")
        self.assertEqual(args.requirement, "crear una función")
        self.assertEqual(args.max_iterations, 4)


if __name__ == "__main__":
    unittest.main()
