from pathlib import Path

from percolation_workflow.anthropic_intake import scan_fermats_repo


def test_anthropic_fermats_snapshot_is_catalogued_without_promotion():
    root = Path(__file__).parents[1] / "artifacts" / "anthropic_fermats_last_theorem"
    snapshot = scan_fermats_repo(root)
    assert snapshot.commit == "aa2d8b34692b16c70f699536de0d8e75b9a3e9ef"
    assert snapshot.lean_toolchain == "leanprover/lean4:v4.33.1"
    assert snapshot.mathlib_revision == "db584cd6d46c92f209a44c0f1c829460d327499d"
    assert snapshot.source_counts["Theorems"] == 29511
    assert snapshot.source_counts["Definitions"] == 1450
    assert {candidate.classification for candidate in snapshot.candidates} == {1, 2, 3}
    assert any(candidate.path.endswith("Module_Quotient.lean")
               and candidate.classification == 2 for candidate in snapshot.candidates)
    assert any(candidate.path.endswith("S_ContinuousLinearMap_map_eigenspace_orthogonal_le_of_commute.lean")
               and candidate.classification == 1 for candidate in snapshot.candidates)
