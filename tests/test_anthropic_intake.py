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


def test_declaration_candidates_keep_provenance_and_pending_boundary():
    root = Path(__file__).parents[1] / "artifacts" / "anthropic_fermats_last_theorem"
    snapshot = scan_fermats_repo(root)
    by_declaration = {candidate.declaration: candidate for candidate in snapshot.candidates
                      if candidate.declaration}

    assert by_declaration["Module.continuous_bilinear_of_finite_free"].classification == 1
    assert by_declaration["IsModuleTopology.continuousLinearEquiv"].classification == 2
    assert by_declaration["Submodule.Quotient.continuousLinearEquiv"].source_lines == "5-18"
    assert by_declaration["Submodule.quotientPiContinuousLinearEquiv"].classification == 1
    assert by_declaration["ExtPushout (extPushoutRel, mk, inl, inr, proj, lift, hom_ext)"].classification == 1

    for candidate in by_declaration.values():
        assert candidate.source_commit == snapshot.commit
        assert candidate.source_sha256 and len(candidate.source_sha256) == 64
        assert candidate.path.startswith(("Definitions/",))
        assert candidate.mathlib_revision == snapshot.mathlib_revision
        assert candidate.lean_toolchain == snapshot.lean_toolchain
        assert candidate.admission_status == "pending"


def test_p2m_util_remains_architecture_only():
    root = Path(__file__).parents[1] / "artifacts" / "anthropic_fermats_last_theorem"
    snapshot = scan_fermats_repo(root)
    util = next(candidate for candidate in snapshot.candidates if candidate.path == "P2M/Util.lean")
    assert util.classification == 3
    assert util.reuse_mode == "architecture-only"
    assert util.admission_status == "pending"
    contract = snapshot.architecture["p2m_contract"]
    assert contract["required_behavior"]["clear_aux_decls_instead_of_revert"] is True
    assert contract["required_behavior"]["universe_generalization_check"] is True
    assert contract["registry_promotion"] is False
