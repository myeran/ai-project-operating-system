import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from lifecycle_artifact_service import LifecycleArtifactService  # noqa: E402


class LifecycleArtifactServiceTests(unittest.TestCase):
    def test_generates_mermaid_and_html_with_current_status(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            service = LifecycleArtifactService(temp_dir)
            paths = service.generate(
                "projects/demo",
                {"project_id": "project-1", "phase": "Discovery"},
            )

            mermaid = Path(paths["mermaid"]).read_text(encoding="utf-8")
            html = Path(paths["html"]).read_text(encoding="utf-8")
            self.assertTrue(Path(paths["mermaid"]).exists())
            self.assertTrue(Path(paths["html"]).exists())
            self.assertIn("flowchart TB", mermaid)
            self.assertIn("class D current", mermaid)
            self.assertIn("class S,P,U,E,V,L,K future", mermaid)
            self.assertIn("mermaid", html)
            self.assertIn("נוצר אוטומטית", html)
            self.assertIsNone(service.existing_paths("projects/missing"))
            self.assertEqual(service.existing_paths("projects/demo"), paths)

    def test_completed_phases_are_blue_when_phase_advances(self):
        service = LifecycleArtifactService("/tmp")
        mermaid = service._render_mermaid({"project_id": "project-2", "phase": "Execution"})
        self.assertIn("class E current", mermaid)
        self.assertIn("class D,S,P,U completed", mermaid)
        self.assertIn("class V,L,K future", mermaid)


if __name__ == "__main__":
    unittest.main()
