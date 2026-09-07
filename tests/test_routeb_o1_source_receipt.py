from fractions import Fraction
import hashlib

from percolation_workflow.routeb_o1_source_receipt import (
    O1_SOURCE_RECEIPT_SCHEMA,
    audit_routeb_o1_artifact_bindings,
    audit_routeb_o1_source_receipt,
)


def valid_receipt(*, source_binding_proven: bool = False) -> dict:
    return {
        "schema": O1_SOURCE_RECEIPT_SCHEMA,
        "source_key": "routeb-exact-fourier-mass:abc",
        "state_key": "routeb-qcell:center=(0,0,0,0,0,0)",
        "mu_exact": "1/1000000",
        "q_domain": {"kind": "exact_point_cell", "radius": "1/1000"},
        "matrix_type": "Matrix (Fin 6) (Fin 6) ℝ",
        "evaluator_definition": "M_exact",
        "regularization": "M_authoritative = M_fourier + mu * I",
        "block_order_one_based": [1, 2, 3, 6],
        "didx_zero_based": [0, 1, 2, 5],
        "bidx_zero_based": [3, 4],
        "projection_type": "Matrix (Fin 4) (Fin 4) ℝ",
        "projection_term": "M_DD45_at q",
        "binding_theorem": "h_MDD_def",
        "source_binding_theorem": "h_source_mass",
        "source_binding_proven": source_binding_proven,
        "lean_file_hash": "a" * 64,
        "coefficient_payload_hash": "b" * 64,
        "deployed_source_hash": "c" * 64,
    }


def test_typed_export_is_conditional_until_source_binding_is_proven():
    audit = audit_routeb_o1_source_receipt(valid_receipt())
    assert audit.status == "CONDITIONAL_TYPED_SOURCE_EXPORT"
    assert audit.mu_exact == Fraction(1, 1_000_000)
    assert audit.formal_certificate_allowed is False
    assert audit.registry_eligible is False


def test_typed_export_reaches_intake_boundary_but_not_registry():
    audit = audit_routeb_o1_source_receipt(
        valid_receipt(source_binding_proven=True)
    )
    assert audit.status == "READY_FOR_TYPED_SOURCE_INTAKE"
    assert audit.comparator_status == "pending"
    assert audit.formal_certificate_allowed is False
    assert audit.registry_eligible is False


def test_typed_export_rejects_wrong_index_map_and_hash():
    receipt = valid_receipt()
    receipt["didx_zero_based"] = [0, 1, 2, 3]
    receipt["lean_file_hash"] = "bad"
    audit = audit_routeb_o1_source_receipt(receipt)
    assert audit.status == "REJECTED"
    assert "didx_zero_based_mismatch" in audit.errors
    assert any("sha256" in error for error in audit.errors)


def test_typed_export_reports_missing_contract_fields():
    receipt = valid_receipt()
    del receipt["source_binding_theorem"]
    del receipt["q_domain"]
    audit = audit_routeb_o1_source_receipt(receipt)
    assert audit.status == "PENDING_REQUIRED_FIELDS"
    assert set(audit.missing) == {"q_domain", "source_binding_theorem"}


def test_artifact_binding_recomputes_declared_file_hash(tmp_path):
    artifact = tmp_path / "source.lean"
    artifact.write_text("theorem t : True := by trivial\n", encoding="utf-8")
    digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
    receipt = valid_receipt()
    receipt["artifacts"] = {
        "lean_file": str(artifact),
        "lean_sha256": digest,
    }
    audit = audit_routeb_o1_artifact_bindings(receipt)
    assert audit.status == "ARTIFACT_BINDINGS_VERIFIED"
    assert audit.verified == ("lean_file",)
    assert audit.formal_certificate_allowed is False


def test_artifact_binding_keeps_hash_only_metadata_pending(tmp_path):
    receipt = valid_receipt()
    receipt["artifacts"] = {
        "lean_sha256": "a" * 64,
        "mass_csv_sha256": "b" * 64,
    }
    audit = audit_routeb_o1_artifact_bindings(receipt)
    assert audit.status == "PENDING_ARTIFACT_PATHS"
    assert set(audit.missing) == {"artifacts.lean_file", "artifacts.mass_csv"}


def test_artifact_binding_rejects_content_hash_mismatch(tmp_path):
    artifact = tmp_path / "source.lean"
    artifact.write_text("changed\n", encoding="utf-8")
    receipt = valid_receipt()
    receipt["artifacts"] = {
        "lean_file": str(artifact),
        "lean_sha256": "a" * 64,
    }
    audit = audit_routeb_o1_artifact_bindings(receipt)
    assert audit.status == "REJECTED"
    assert "content hash mismatch" in audit.errors[0]
