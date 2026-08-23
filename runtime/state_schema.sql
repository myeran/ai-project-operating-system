CREATE TABLE IF NOT EXISTS project_state (
    project_id TEXT PRIMARY KEY,
    phase TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN (
        'proposed', 'active', 'blocked', 'awaiting_approval',
        'completed', 'cancelled'
    )),
    completed_outputs TEXT NOT NULL DEFAULT '[]',
    missing_items TEXT NOT NULL DEFAULT '[]',
    required_user_action TEXT,
    expected_output TEXT NOT NULL DEFAULT '[]',
    completion_criteria TEXT NOT NULL DEFAULT '[]',
    next_recommended_action TEXT,
    canonical_state TEXT NOT NULL,
    version INTEGER NOT NULL CHECK (version >= 1),
    updated_by TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES project_registry(project_id)
);

CREATE TABLE IF NOT EXISTS state_update_proposals (
    proposal_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    changes TEXT NOT NULL,
    actor TEXT NOT NULL,
    expected_version INTEGER NOT NULL,
    approved_by TEXT,
    status TEXT NOT NULL CHECK (status IN ('pending', 'approved', 'committed', 'rejected')),
    created_at TEXT NOT NULL,
    approved_at TEXT,
    committed_at TEXT,
    committed_by TEXT,
    new_version INTEGER,
    rejected_at TEXT,
    rejected_by TEXT,
    rejection_reason TEXT,
    FOREIGN KEY (project_id) REFERENCES project_registry(project_id)
);

CREATE TABLE IF NOT EXISTS state_audit (
    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL CHECK (event_type IN (
        'state_created', 'state_update_proposed', 'state_updated',
        'version_conflict', 'invalid_transition_rejected',
        'approval_required', 'state_proposal_approved', 'state_proposal_rejected'
    )),
    project_id TEXT NOT NULL,
    actor TEXT NOT NULL,
    event_timestamp TEXT NOT NULL,
    previous_version INTEGER,
    new_version INTEGER,
    details TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_state_audit_project
    ON state_audit(project_id);

CREATE INDEX IF NOT EXISTS idx_state_proposals_project
    ON state_update_proposals(project_id);
