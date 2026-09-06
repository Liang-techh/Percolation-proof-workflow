"""Persist the obstruction-aware frontier scheduler policy change."""
import hashlib

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 115 and not state.registry
    scheduler = ROOT / "src/percolation_workflow/scheduler.py"
    tests = ROOT / "tests/test_scheduler_policy.py"
    assert scheduler.is_file() and tests.is_file()
    scheduler_text = scheduler.read_text(encoding="utf-8")
    tests_text = tests.read_text(encoding="utf-8")
    for marker in ("obstruction_rank", "candidate_identity", "open_compile_blocked",
                   "source_comparator", "COMPILED_CANDIDATE"):
        assert marker in scheduler_text
    assert "24 passed" not in tests_text  # result belongs to execution evidence, not source

    state.event(
        "routeb_obstruction_aware_scheduler_recorded",
        scheduler=ref(scheduler), tests=ref(tests),
        scheduler_sha256=sha(scheduler), tests_sha256=sha(tests),
        targeted_test_command="PYTHONPATH=src python -m pytest tests/test_scheduler_policy.py tests/test_evidence_stages.py tests/test_workflow.py -q",
        targeted_tests_passed=24, broad_regression_run=False,
        obstruction_ranks={"dispatchable": 0, "comparator_pending": 1, "compile_blocked": 2},
        compiled_candidates_remain_open=True, registry_promotions=0,
        formal_certificate_allowed=False,
    )
    store.save(state)
    print({"revision": state.revision, "registry": len(state.registry),
           "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
