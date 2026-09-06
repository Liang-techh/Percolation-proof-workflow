"""Persist host-dispatch integration and attempt-history rebind repair."""
import hashlib
import shutil

from record_routeb_port_progress import ROOT, ref
from percolation_workflow.store import StateStore


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    assert state.revision == 120 and not state.registry
    bridge = ROOT / "src/percolation_workflow/agent_bridge.py"
    model = ROOT / "src/percolation_workflow/model.py"
    tests = ROOT / "tests/test_agent_bridge.py"
    scheduler_tests = ROOT / "tests/test_scheduler_policy.py"
    backup = ROOT / "artifacts/routeb_storage_checkpoint_20260905/state-before-revision121.json"
    for path in (bridge, model, tests, scheduler_tests):
        assert path.is_file(), path
    bridge_text = bridge.read_text(encoding="utf-8")
    model_text = model.read_text(encoding="utf-8")
    tests_text = tests.read_text(encoding="utf-8")
    assert "rank_frontier" in bridge_text
    assert "obstruction-aware scheduler" in bridge_text
    assert "rebind_attempt" in bridge_text and "def rebind_attempt" in model_text
    assert "test_prepare_requests_uses_obstruction_aware_dispatch_policy" in tests_text
    assert "test_prepare_requests_deduplicates_explicit_candidate_identity" in tests_text

    shutil.copy2(store.path, backup)
    state.event(
        "routeb_host_dispatch_scheduler_integrated",
        bridge=ref(bridge), model=ref(model), tests=ref(tests),
        scheduler_tests=ref(scheduler_tests), bridge_sha256=sha(bridge),
        model_sha256=sha(model), tests_sha256=sha(tests),
        scheduler_tests_sha256=sha(scheduler_tests),
        targeted_test_command="PYTHONPATH=src python -m pytest tests/test_agent_bridge.py tests/test_scheduler_policy.py -q",
        targeted_tests_passed=17, broad_regression_run=False,
        obstruction_aware_host_dispatch=True, explicit_candidate_dedup=True,
        attempt_history_rebind_consistent=True, registry_promotions=0,
        formal_certificate_allowed=False,
    )
    store.save(state)
    print({"revision": state.revision, "registry": len(state.registry),
           "formal_certificate_allowed": False})


if __name__ == "__main__":
    main()
