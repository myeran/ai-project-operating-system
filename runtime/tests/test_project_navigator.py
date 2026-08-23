import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from runtime_api import RuntimeAPIApplication  # noqa: E402


class ProjectNavigatorTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.api = RuntimeAPIApplication(str(Path(self.temp_dir.name) / "navigator.sqlite3"))

    def tearDown(self):
        self.api.close()
        self.temp_dir.cleanup()

    def create_project(self, name):
        return self.api.handle("POST", "/projects/start", {
            "project_name": name, "owner": "owner", "project_type": "Product",
            "project_goal": "Roadmap", "expected_outcome": "Roadmap", "current_stage": "Discovery",
        })[1]

    def test_navigator_reflects_canonical_state_and_is_read_only(self):
        created = self.create_project("Navigator Project")
        before = self.api.state.get_state(created["project_id"])
        status, navigator = self.api.handle("POST", "/projects/navigator", {"project_id": created["project_id"]})
        after = self.api.state.get_state(created["project_id"])
        self.assertEqual(status, 200)
        self.assertEqual(navigator["current_phase"], before["phase"])
        self.assertEqual(navigator["state_version"], before["version"])
        self.assertEqual(navigator["current_skill"], "Discovery Skill")
        self.assertEqual(navigator["steps"][0]["status"], "current")
        self.assertFalse(navigator["can_advance"])
        self.assertTrue(navigator["read_only"])
        self.assertEqual(after["version"], before["version"])

    def test_completed_phase_returns_next_skill_without_transitioning(self):
        created = self.create_project("Navigator Next Skill")
        proposal = self.api.state.propose_state_update(created["project_id"], {"status": "completed"}, actor="owner")
        self.api.state.commit_state_update(proposal["proposal_id"], expected_version=1)
        _, navigator = self.api.handle("POST", "/projects/navigator", {"project_id": created["project_id"]})
        self.assertEqual(navigator["next_phase"], "Strategy")
        self.assertEqual(navigator["next_skill"], "Product Strategy Skill")
        self.assertEqual(navigator["next_action"], "הפעל את השלב הבא")
        self.assertTrue(navigator["can_advance"])
        self.assertEqual(self.api.state.get_state(created["project_id"])["phase"], "Discovery")


if __name__ == "__main__":
    unittest.main()
