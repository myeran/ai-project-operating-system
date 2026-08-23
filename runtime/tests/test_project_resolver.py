import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).parents[1]))

from bootstrap_handler import BootstrapRequest, ProjectInstanceBootstrapHandler  # noqa: E402
from project_resolver import ProjectResolver  # noqa: E402
from registry_adapter import ProjectRegistryAdapter  # noqa: E402
from runtime_gateway import RuntimeEntryGateway  # noqa: E402
from state_adapter import StateAdapter  # noqa: E402


class ProjectResolverMVPTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = str(Path(self.temp_dir.name) / "resolver.sqlite3")
        self.registry = ProjectRegistryAdapter(self.database)
        self.state = StateAdapter(self.database)
        self.bootstrap = ProjectInstanceBootstrapHandler(self.registry, self.state)
        self.gateway = RuntimeEntryGateway()
        self.project = self.bootstrap.initialize(
            BootstrapRequest(
                project_name="Resolver Test Project",
                owner="owner-1",
                os_version="v1.0",
                actor="test",
            )
        )
        self.resolver = ProjectResolver(self.registry)

    def tearDown(self):
        self.state.close()
        self.registry.close()
        self.temp_dir.cleanup()

    def test_resolve_by_exact_project_id(self):
        request = self.gateway.receive(
            "Continue Project",
            project_id=self.project["project_id"],
        )

        result = self.resolver.resolve(request)

        self.assertEqual(result.status, "RESOLVED")
        self.assertEqual(result.project_id, self.project["project_id"])
        self.assertEqual(result.current_phase, "Discovery")
        self.assertEqual(result.current_status, "proposed")
        self.assertEqual(result.os_version, "v1.0")

    def test_resolve_by_exact_project_name(self):
        request = self.gateway.receive("Continue Project: Resolver Test Project")

        result = self.resolver.resolve(request)

        self.assertEqual(result.status, "RESOLVED")
        self.assertEqual(result.project_id, self.project["project_id"])
        self.assertEqual(result.project_name, "Resolver Test Project")

    def test_no_match_does_not_create_project(self):
        request = self.gateway.receive("Continue Project: Missing Project")

        result = self.resolver.resolve(request)

        self.assertEqual(result.status, "NOT_FOUND")
        self.assertEqual(result.project_name, "Missing Project")
        self.assertEqual(self.registry.find_projects(project_name="Missing Project"), [])

    def test_multiple_matches_are_ambiguous(self):
        registry = Mock()
        registry.find_projects.return_value = [
            {
                "project_id": "project-1",
                "project_name": "Shared Name",
                "current_phase": "Discovery",
                "status": "proposed",
                "os_version": "v1.0",
                "location": "projects/one",
            },
            {
                "project_id": "project-2",
                "project_name": "Shared Name",
                "current_phase": "Planning",
                "status": "active",
                "os_version": "v1.0",
                "location": "projects/two",
            },
        ]
        resolver = ProjectResolver(registry)
        request = self.gateway.receive("Continue Project: Shared Name")

        result = resolver.resolve(request)

        self.assertEqual(result.status, "AMBIGUOUS")
        self.assertEqual(len(result.matches), 2)
        self.assertIn("Multiple", result.reason)

    def test_id_and_name_mismatch_is_ambiguous(self):
        request = self.gateway.receive(
            "Continue Project: Other Name",
            project_id=self.project["project_id"],
        )

        result = self.resolver.resolve(request)

        self.assertEqual(result.status, "AMBIGUOUS")

    def test_missing_identifier_returns_not_found(self):
        request = self.gateway.receive("Continue Project")

        result = self.resolver.resolve(request)

        self.assertEqual(result.status, "NOT_FOUND")


if __name__ == "__main__":
    unittest.main()
