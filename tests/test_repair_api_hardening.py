from pathlib import Path
from unittest.mock import patch

import pytest

from percolation_workflow.model import WorkflowState
from percolation_workflow.repair import repair_until_verified
from percolation_workflow.lean import LeanResult


@pytest.mark.parametrize("value", [0, -1, 1.0, True, False, "2", None])
def test_max_rounds_is_a_positive_integer(value):
    state = WorkflowState(project="hardening")
    node = state.add_node("Root", "True")
    with pytest.raises(ValueError, match="positive integer"):
        repair_until_verified(state, node, "agent", ".", "src/nested.lean", lambda *args: None,
                              max_rounds=value)


def test_repair_receipt_preserves_complete_relative_path():
    state = WorkflowState(project="hardening")
    node = state.add_node("Root", "True")
    result = LeanResult(ok=False, command=[], stdout="", stderr="diagnostic", exit_code=1)
    with patch("percolation_workflow.repair.run_lean", return_value=result):
        repair_until_verified(state, node, "agent", Path("."), "proofs/nested.lean",
                              lambda *args: None, max_rounds=1)
    event = next(event for event in state.events if event["kind"] == "repair_requested")
    assert event["disjoint_do"]["path"] == "proofs/nested.lean"
