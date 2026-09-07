from percolation_workflow.routeb_residual_l1_contract import (
    EXPECTED_THEOREMS,
    RESIDUAL_L1_LEAN_RECEIPT_SCHEMA,
    audit_routeb_residual_l1_lean_receipt,
)


def complete_receipt():
    return {
        "schema": RESIDUAL_L1_LEAN_RECEIPT_SCHEMA,
        "compile_status": "passed",
        "exit_code": 0,
        "compile_command": ["lake", "env", "lean", "GramResidual.lean"],
        "source_sha256": "a" * 64,
        "coefficient_artifact_sha256": "b" * 64,
        "theorem_names": list(EXPECTED_THEOREMS),
        "axioms": {name: [] for name in EXPECTED_THEOREMS},
        "sorry_free": True,
        "admit_free": True,
        "forbidden_tokens": [],
        "lean_toolchain": "v4.32.0",
        "mathlib_commit": "mathlib-test-pin",
        "coefficient_term_count": 12,
        "residual_l1": "1/100",
        "rational_lower_bound": "3/100",
        "scaled_margin": "1/50",
    }


def candidate():
    return {
        "status": "EXACT_RATIONAL_GRAM_RECONSTRUCTION_CANDIDATE",
        "artifact_sha256": "b" * 64,
        "residual_term_count": 12,
        "residual_l1": "1/100",
        "rational_lower_bound": "3/100",
        "certified_scaled_margin": "1/50",
    }


def test_missing_authoritative_bindings_stays_pending():
    result = audit_routeb_residual_l1_lean_receipt(complete_receipt(), candidate_receipt=candidate())
    assert result.status == "PENDING"
    assert "source_sha256_not_authoritatively_bound" in result.pending
    assert result.formal_certificate_allowed is False
    assert result.registry_eligible is False


def test_complete_receipt_accepts_only_with_coordinator_bindings():
    result = audit_routeb_residual_l1_lean_receipt(
        complete_receipt(),
        expected_source_sha256="a" * 64,
        expected_coefficient_artifact_sha256="b" * 64,
        expected_lean_toolchain="v4.32.0",
        expected_mathlib_commit="mathlib-test-pin",
        candidate_receipt=candidate(),
    )
    assert result.status == "ACCEPTED"
    assert result.errors == ()
    assert result.pending == ()
    assert result.registry_eligible is False


def test_failed_or_mismatched_receipt_is_rejected():
    receipt = complete_receipt()
    receipt["exit_code"] = 1
    receipt["source_sha256"] = "c" * 64
    result = audit_routeb_residual_l1_lean_receipt(
        receipt,
        expected_source_sha256="a" * 64,
        expected_coefficient_artifact_sha256="b" * 64,
        expected_lean_toolchain="v4.32.0",
        expected_mathlib_commit="mathlib-test-pin",
        candidate_receipt=candidate(),
    )
    assert result.status == "REJECTED"
    assert "exit_code_not_zero" in result.errors
    assert "source_sha256_mismatch" in result.errors


def test_non_mapping_receipt_is_rejected():
    result = audit_routeb_residual_l1_lean_receipt([])  # type: ignore[arg-type]
    assert result.status == "REJECTED"
    assert result.errors == ("receipt_not_mapping",)
