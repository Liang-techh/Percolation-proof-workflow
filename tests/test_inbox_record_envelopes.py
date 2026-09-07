import json

from scripts.integrate_agent_reviews import inbox_records, record_header, record_kind


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
