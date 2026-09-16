import ast
from pathlib import Path
import unittest


def load_nodes():
    """Read the data-only flow definition without importing Streamlit."""
    tree = ast.parse(Path(__file__).with_name("app.py").read_text(encoding="utf-8"))
    for statement in tree.body:
        if isinstance(statement, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "NODES" for target in statement.targets):
                return ast.literal_eval(statement.value)
    raise RuntimeError("NODES flow definition was not found")


NODES = load_nodes()


class FlowchartTests(unittest.TestCase):
    def follow(self, answers):
        node_id = "power_up"
        for answer in answers:
            while NODES[node_id]["type"] == "action":
                node_id = NODES[node_id]["next"]
            node_id = NODES[node_id]["options"][answer]
        while NODES[node_id]["type"] == "action":
            node_id = NODES[node_id]["next"]
        return node_id

    def test_no_power_after_checks(self):
        self.assertEqual(
            self.follow(["No", "Yes", "No"]),
            "replace_motor_followup",
        )

    def test_blend_error(self):
        self.assertEqual(
            self.follow(["Yes", "No", "BLEND ERROR"]),
            "replace_blade_cage",
        )

    def test_spin_vibration(self):
        self.assertEqual(
            self.follow(["Yes", "Yes", "No", "No error message", "Yes"]),
            "replace_blade_cage",
        )


if __name__ == "__main__":
    unittest.main()
