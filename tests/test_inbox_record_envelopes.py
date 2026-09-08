import json

from scripts.integrate_agent_reviews import (
    TASK_TARGETS,
    artifact_binding_audit,
    inbox_records,
    record_header,
    record_kind,
    resolve_task_id,
    is_retired_agent,
)


def test_task_target_routes_are_two_field_fail_closed_bindings():
    """Replacement lanes must not crash the harvester during tuple unpacking."""
    for task_id, binding in TASK_TARGETS.items():
        assert isinstance(task_id, str) and task_id
        assert isinstance(binding, tuple) and len(binding) == 2
        target, classification = binding
        assert isinstance(classification, str) and classification
        if target is not None:
            assert isinstance(target, str) and target


def test_artifact_binding_audit_is_fail_closed(tmp_path):
    artifact = tmp_path / "candidate.lean"
    artifact.write_text("theorem candidate : True := True.intro\n", encoding="utf-8")
    import hashlib
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest().upper()

    bound = artifact_binding_audit(
        {"candidate_path": "candidate.lean", "candidate_sha256": digest},
        root=tmp_path,
    )
    assert bound["status"] == "BOUND"
    assert bound["actual_sha256"] == digest

    rejected = artifact_binding_audit(
        {"candidate_path": "candidate.lean", "candidate_sha256": "0" * 64},
        root=tmp_path,
    )
    assert rejected["status"] == "REJECTED"
    assert rejected["reason"] == "artifact_sha256_mismatch"


def test_artifact_binding_audit_keeps_missing_or_external_evidence_pending(tmp_path):
    missing = artifact_binding_audit(
        {"candidate_path": "missing.lean", "candidate_sha256": "a" * 64},
        root=tmp_path,
    )
    assert missing == {
        "status": "PENDING", "reason": "artifact_missing", "path": "missing.lean"
    }

    outside = artifact_binding_audit(
        {"candidate_path": str(tmp_path.parent / "outside.lean"),
         "candidate_sha256": "a" * 64},
        root=tmp_path,
    )
    assert outside["status"] == "PENDING"
    assert outside["reason"] == "artifact_outside_workspace"


def test_md_handoff_and_json_companion_are_discoverable(tmp_path):
    handoff = tmp_path / "handoff-T-P4-012.md"
    handoff.write_text(
        "---\nkind: handoff\ntask_id: T-P4-012\nsource_agent: agent-x\n---\n",
        encoding="utf-8",
    )
    companion = tmp_path / "companion-T-P4-012.json"
    companion.write_text(json.dumps({
        "kind": "companion_log", "task_id": "T-P4-012",
        "source_agent": "agent-y",
    }), encoding="utf-8")

    paths = inbox_records(tmp_path)
    assert paths == [companion, handoff]
    assert record_kind(handoff, record_header(handoff)) == "handoff"
    assert record_header(companion)["task_id"] == "T-P4-012"
    assert record_kind(companion, record_header(companion)) == "companion_log"


def test_planning_and_claim_files_are_not_records(tmp_path):
    claim = tmp_path / "claim-T-P4-012.md"
    claim.write_text("kind: task_claim\ntask_id: T-P4-012\n", encoding="utf-8")
    plan = tmp_path / "task_plan.md"
    plan.write_text("kind: task_plan\n", encoding="utf-8")
    assert inbox_records(tmp_path) == []


def test_descriptive_new_review_is_discovered_from_bounded_envelope(tmp_path):
    review = tmp_path / "NEW_REVIEW_T-P4-012_20260908.md"
    review.write_text(
        "---\ntask_id: T-P4-012\nstatus: OPEN_UNCOMPILED\n"
        "admission: pending\n---\nbody text\n",
        encoding="utf-8",
    )
    assert inbox_records(tmp_path) == [review]
    assert record_kind(review, record_header(review)) == "review_result"


def test_bare_task_id_without_review_fields_is_not_inferred(tmp_path):
    claim = tmp_path / "NEW_TASK_T-P4-012.md"
    claim.write_text("---\ntask_id: T-P4-012\n---\n", encoding="utf-8")
    assert inbox_records(tmp_path) == []


def test_claim_status_without_kind_is_not_inferred(tmp_path):
    claim = tmp_path / "claim-T-P4-012-agent.md"
    claim.write_text("---\ntask_id: T-P4-012\nstatus: claimed\n---\n", encoding="utf-8")
    assert inbox_records(tmp_path) == []


def test_retired_agent_labels_are_rejected_without_rewriting_history():
    assert is_retired_agent({"source_agent": "流川枫"}) is True
    assert is_retired_agent({"agent": "Flowchuanfeng"}) is True
    assert is_retired_agent({"source_agent": "Poincare the 6th"}) is False


def test_record_id_recovers_known_task_without_scanning_body(tmp_path):
    review = tmp_path / "review-T-P4-038-agent-20260907T1558.md"
    review.write_text(
        "---\nkind: review_result\nreview_id: review-T-P4-038-agent-20260907T1558\n"
        "---\nThis body mentions T-P3-009 but must not affect routing.\n",
        encoding="utf-8",
    )
    header = record_header(review)
    assert resolve_task_id(review, header) == "T-P4-038"


def test_longest_known_task_prefix_wins(tmp_path):
    review = tmp_path / "review-T-P4-033-O1-body6-slice-agent-20260907T1600.md"
    review.write_text(
        "---\nkind: review_result\nreview_id: review-T-P4-033-O1-body6-slice-agent-20260907T1600\n"
        "---\n",
        encoding="utf-8",
    )
    assert resolve_task_id(review, record_header(review)) == "T-P4-033-O1-body6-slice"


def test_known_handoff_task_id_date_suffix_normalizes(tmp_path):
    review = tmp_path / "handoff-T-FLT-S1-AVERAGING-CLM-20270101.md"
    review.write_text(
        "---\nkind: handoff\ntask_id: T-FLT-S1-AVERAGING-CLM-HANDOFF-20270101\n"
        "review_id: H-FLT-S1-20270101\n---\n",
        encoding="utf-8",
    )
    assert resolve_task_id(review, record_header(review)) == "T-FLT-S1-AVERAGING-CLM"


def test_unknown_handoff_task_id_remains_unrouted(tmp_path):
    review = tmp_path / "handoff-T-UNKNOWN-20270101.md"
    review.write_text(
        "---\nkind: handoff\ntask_id: T-UNKNOWN-HANDOFF-20270101\n---\n",
        encoding="utf-8",
    )
    assert resolve_task_id(review, record_header(review)) == "T-UNKNOWN-HANDOFF-20270101"


def test_known_date_suffixed_task_id_normalizes(tmp_path):
    review = tmp_path / "handoff-T-FLT-T1-L1-MINIMAL-ADAPTER-20270101.md"
    review.write_text(
        "---\nkind: handoff\ntask_id: T-FLT-T1-L1-MINIMAL-ADAPTER-20270101\n"
        "review_id: H-FLT-T1-L1-20270101\n---\n",
        encoding="utf-8",
    )
    assert resolve_task_id(review, record_header(review)) == "T-FLT-T1-L1-MINIMAL-ADAPTER"
