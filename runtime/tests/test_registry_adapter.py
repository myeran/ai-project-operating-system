import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from registry_adapter import (  # noqa: E402
    DuplicateProjectError,
    ProjectMetadata,
    ProjectNotFoundError,
    ProjectRegistryAdapter,
    VersionConflictError,
)


class RegistryAdapterMVPTests(unittest.TestCase):
    def setUp(self):
        self.registry = ProjectRegistryAdapter(":memory:")
        self.metadata = ProjectMetadata(
            project_name="Personal Habit Tracker",
            owner="owner-1",
            location="projects/personal-habit-tracker",
            os_version="v1.0",
        )

    def tearDown(self):
        self.registry.close()

    def test_1_create(self):
        project = self.registry.create_project(self.metadata, actor="system")

        self.assertTrue(project["project_id"])
        self.assertEqual(project["project_name"], "Personal Habit Tracker")
        self.assertEqual(project["version"], 1)
        self.assertEqual(project["status"], "proposed")
        self.assertEqual(self.registry.audit_events(project["project_id"])[0]["event_type"], "project_created")

    def test_2_read(self):
        created = self.registry.create_project(self.metadata, actor="system")

        loaded = self.registry.get_project(created["project_id"])

        self.assertEqual(loaded, created)

    def test_3_find_by_name(self):
        created = self.registry.create_project(self.metadata, actor="system")

        found = self.registry.find_projects(project_name=" personal   HABIT tracker ")

        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["project_id"], created["project_id"])

    def test_4_duplicate_is_rejected_and_audited(self):
        created = self.registry.create_project(self.metadata, actor="system")

        with self.assertRaises(DuplicateProjectError):
            self.registry.create_project(self.metadata, actor="system")

        self.assertEqual(
            [event["event_type"] for event in self.registry.audit_events()],
            ["project_created", "duplicate_rejected"],
        )
        self.assertEqual(self.registry.get_project(created["project_id"])["version"], 1)

    def test_5_update_increments_version(self):
        created = self.registry.create_project(self.metadata, actor="system")

        updated = self.registry.update_project_metadata(
            created["project_id"],
            expected_version=1,
            actor="orchestrator",
            status="active",
            current_phase="Discovery",
        )

        self.assertEqual(updated["version"], 2)
        self.assertEqual(updated["status"], "active")
        self.assertEqual(self.registry.audit_events()[-1]["event_type"], "project_updated")

    def test_6_version_conflict_is_rejected(self):
        created = self.registry.create_project(self.metadata, actor="system")
        self.registry.update_project_metadata(
            created["project_id"],
            expected_version=1,
            actor="orchestrator",
            status="active",
        )

        with self.assertRaises(VersionConflictError):
            self.registry.update_project_metadata(
                created["project_id"],
                expected_version=1,
                actor="stale-worker",
                location="projects/changed",
            )

        self.assertEqual(self.registry.get_project(created["project_id"])["version"], 2)
        self.assertEqual(self.registry.audit_events()[-1]["event_type"], "version_conflict")

    def test_missing_project_is_explicit(self):
        with self.assertRaises(ProjectNotFoundError):
            self.registry.get_project("missing-project")


if __name__ == "__main__":
    unittest.main()
