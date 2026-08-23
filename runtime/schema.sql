PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS project_registry (
    project_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    project_name_key TEXT NOT NULL UNIQUE,
    owner TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN (
        'proposed', 'active', 'blocked', 'awaiting_approval',
        'completed', 'cancelled'
    )),
    current_phase TEXT NOT NULL,
    os_version TEXT NOT NULL,
    location TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    last_activity TEXT NOT NULL,
    version INTEGER NOT NULL CHECK (version >= 1),
    audit_metadata TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS registry_audit (
    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL CHECK (event_type IN (
        'project_created', 'project_updated',
        'duplicate_rejected', 'version_conflict'
    )),
    project_id TEXT,
    actor TEXT NOT NULL,
    event_timestamp TEXT NOT NULL,
    previous_version INTEGER,
    new_version INTEGER,
    details TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_project_registry_name_key
    ON project_registry(project_name_key);

CREATE INDEX IF NOT EXISTS idx_registry_audit_project
    ON registry_audit(project_id);
