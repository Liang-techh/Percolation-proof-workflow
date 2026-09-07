from percolation_workflow.routeb_o2_receipt import audit_routeb_o2_runtime_receipt


SOURCE = "A" * 64
SCHEDULE = "B" * 64


def complete_receipt() -> dict:
    return {
        "source_sha256": SOURCE,
        "operation_schedule_hash": SCHEDULE,
        "runtime": {
            "julia_version": "1.x", "os_architecture": "x86_64",
            "blas": "pinned", "libm": "pinned", "rounding_mode": "nearest",
            "fastmath_fma_threading": "disabled/recorded",
        },
        "constants": {
            "mu_bits": "mu", "h_bits": "h", "two_h_bits": "2h",
            "pi_bits": "pi", "pi_over_two_bits": "pi/2",
        },
        "operation_schedule": ["T_prev*A_i"],
        "source_line_range_hashes": {
            "fk_frames": "1", "mass_matrix": "2", "potential": "3",
            "arm_MCG": "4", "exact_ddq": "5",
        },
        "boxes": [{
            "input_box": "q-box", "output_enclosure": "M/P/C/G",
            "dependency_ids": ["P3", "O2.4"],
        }],
        "coverage": {"all_boxes_covered": True},
        "finite_non_nan_no_overflow": True,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }


def test_complete_receipt_is_only_ready_for_coordinator_admission() -> None:
    result = audit_routeb_o2_runtime_receipt(
        complete_receipt(), expected_source_sha256=SOURCE,
        expected_operation_schedule_hash=SCHEDULE,
    )
    assert result.status == "READY_FOR_COORDINATOR_ADMISSION"
    assert result.formal_certificate_allowed is False
    assert result.registry_promoted is False


def test_missing_runtime_and_coverage_stays_pending() -> None:
    receipt = complete_receipt()
    del receipt["runtime"]["libm"]
    receipt["coverage"]["all_boxes_covered"] = False
    result = audit_routeb_o2_runtime_receipt(
        receipt, expected_source_sha256=SOURCE,
        expected_operation_schedule_hash=SCHEDULE,
    )
    assert result.status == "PENDING_REQUIRED_FIELDS"
    assert "runtime.libm" in result.missing
    assert "coverage.all_boxes_covered" in result.missing


def test_hash_or_boundary_mismatch_is_rejected() -> None:
    receipt = complete_receipt()
    receipt["source_sha256"] = "C" * 64
    receipt["formal_certificate_allowed"] = True
    result = audit_routeb_o2_runtime_receipt(
        receipt, expected_source_sha256=SOURCE,
        expected_operation_schedule_hash=SCHEDULE,
    )
    assert result.status == "REJECTED"
    assert "source_hash_mismatch" in result.errors
    assert "formal_gate_boundary_violation" in result.errors
