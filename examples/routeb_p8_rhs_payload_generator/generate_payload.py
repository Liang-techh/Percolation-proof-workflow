"""Generate a provenance-bound, fail-closed P8 RHS payload template.

This tool reads the selected Route-B Julia source but never imports, executes,
or writes to that external project.  It emits a local metadata file and a
receipt template.  Numerical endpoint intervals must come from a separately
authenticated producer and are rejected by the companion checker while they
are missing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


COORDINATE_ORDER = [*(f"q{i}" for i in range(1, 7)),
                    *(f"v{i}" for i in range(1, 7)), "w", "c"]
SOURCE_SPECS = (
    "robot_final/cross_validation/routeB_reachability_full_dh_probe.jl",
    "robot_final/dhport_lib.jl",
)
LOCAL_BOX = {
    "id": "p8-local-zero-cell-qv-w-1e-2-c-2",
    "lo": ["-0.01"] * 12 + ["-0.01", "-2"],
    "hi": ["0.01"] * 12 + ["0.01", "2"],
    "meaning": (
        "one explicit full-state box only; q/v/w are a small zero-centered "
        "cell and c uses the conservative P8 adapter range [-2,2]"
    ),
}
PARAMETERS = {
    "horizon_T": "1",
    "initial_radius": "0.15",
    "eta_star": "5.6",
    "disturbance_bound": "sqrt(3)",
    "mass_regularizer": "1e-6",
    "fd_step": "1e-5",
    "arithmetic": "IEEE-754 Float64 source arithmetic",
}
ROUNDING = {
    "source_runtime": "Float64",
    "endpoint_rounding": "not_authenticated",
    "direction": "unspecified",
    "endpoint_encoding": "exact_decimal_or_rational_text_required",
    "note": (
        "source Float64 evaluation is provenance only; no outward-rounding "
        "claim is made by this generator"
    ),
}

REQUIRED_PROBE_FRAGMENTS = (
    "function full_rhs!(du, u, p, t)",
    "q = u[1:6]",
    "dq = u[7:12]",
    "w = u[13]",
    "du[i] = dq[i]",
    "du[i + 6] = acc[i]",
    "du[13] = z0",
    "return du",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_contract(probe_text: str) -> dict[str, object]:
    missing = [fragment for fragment in REQUIRED_PROBE_FRAGMENTS
               if fragment not in probe_text]
    if missing:
        raise ValueError(
            "fail-closed: selected full_rhs! source is missing required "
            f"contract fragments: {missing}"
        )
    return {
        "julia_state_dimension": 13,
        "payload_dimension": 14,
        "source_function": "full_rhs!",
        "source_state_order": [*(f"q{i}" for i in range(1, 7)),
                                *(f"v{i}" for i in range(1, 7)), "w"],
        "lifted_tail": {"c": "sidecar parameter; not consumed by full_rhs!"},
        "source_literal_tail": {"w_rhs": "0", "c_rhs": "unbound"},
        "required_fragments_checked": list(REQUIRED_PROBE_FRAGMENTS),
        "ramp_binding": "OPEN",
    }


def coordinate_mapping() -> list[dict[str, object]]:
    rows = []
    for index, name in enumerate(COORDINATE_ORDER):
        if index < 6:
            expression = f"u[{index + 1}]"
            role = "q"
        elif index < 12:
            expression = f"u[{index + 1}]"
            role = "dq"
        elif index == 12:
            expression = "u[13]"
            role = "w"
        else:
            expression = None
            role = "c_sidecar"
        rows.append({
            "payload_index_zero_based": index,
            "payload_index_one_based": index + 1,
            "name": name,
            "role": role,
            "julia_full_rhs_input": expression,
            "julia_full_rhs_output": (
                f"du[{index + 1}]" if index < 13 else None
            ),
            "binding_status": "source-text-only" if index < 13 else "OPEN",
        })
    return rows


def build_documents(routeb_root: Path) -> tuple[dict[str, object], dict[str, object]]:
    root = routeb_root.resolve()
    probe = root / Path(SOURCE_SPECS[0])
    if not probe.is_file():
        raise FileNotFoundError(f"missing selected full_rhs! source: {probe}")
    probe_text = probe.read_text(encoding="utf-8")
    contract = source_contract(probe_text)
    sources = []
    for relative in SOURCE_SPECS:
        path = root / Path(relative)
        if not path.is_file():
            raise FileNotFoundError(f"missing declared source: {path}")
        sources.append({"path": relative, "sha256": sha256(path)})

    metadata = {
        "schema": "routeb-p8-rhs-payload-metadata-v1",
        "candidate_id": "robot_final/full_dh_probe+dhport_lib",
        "candidate_scope": "file-level source snapshot; overall canonicality OPEN",
        "source_root_description": "external 6dof_sos_optimized working tree",
        "source_hashes": sources,
        "coordinate_order": COORDINATE_ORDER,
        "coordinate_mapping": coordinate_mapping(),
        "local_box": LOCAL_BOX,
        "parameters": PARAMETERS,
        "rounding": ROUNDING,
        "source_contract": contract,
        "formal_boundary": {
            "theorem": False,
            "LEAN_VERIFIED": False,
            "registry_mutation": False,
            "global_branch_and_bound": False,
            "solver": False,
            "regression": False,
            "conclusion": None,
        },
    }
    intervals = []
    for name in COORDINATE_ORDER:
        # The tail literals are source-text facts, but they are not a complete
        # endpoint enclosure.  Keeping them visible makes the 13/14 mismatch
        # auditable without fabricating the twelve dynamic intervals.
        if name == "w":
            lower = upper = "0"
            evidence = "source_literal_du13_equals_zero"
        elif name == "c":
            lower = upper = None
            evidence = "OPEN_sidecar_not_consumed_by_full_rhs"
        else:
            lower = upper = None
            evidence = "OPEN_external_endpoint_evaluator_required"
        intervals.append({
            "coordinate": name,
            "lower": lower,
            "upper": upper,
            "evidence": evidence,
        })
    receipt = {
        "schema": "routeb-p8-rhs-endpoint-receipt-v1",
        "receipt_status": "pending_endpoint_payload",
        "formal_admission": "not_theorem",
        "LEAN_VERIFIED": False,
        "candidate_id": metadata["candidate_id"],
        "coordinate_order": COORDINATE_ORDER,
        "dimension": 14,
        "local_box": LOCAL_BOX,
        "source_hashes": sources,
        "parameters": PARAMETERS,
        "rounding": ROUNDING,
        "source_contract": contract,
        "coordinate_mapping": coordinate_mapping(),
        "rhs_endpoint_intervals": intervals,
        "binding_status": "source-text-snapshot-only",
        "binding_conclusion": None,
        "note": (
            "Template only. A concrete receipt must replace every null endpoint "
            "with exact decimal/rational text and provide authenticated outward "
            "rounding evidence."
        ),
    }
    return metadata, receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--routeb-root",
        type=Path,
        default=Path(r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized"),
    )
    parser.add_argument(
        "--output-dir", type=Path,
        default=Path(__file__).resolve().parent,
    )
    args = parser.parse_args(argv)
    metadata, receipt = build_documents(args.routeb_root)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "SOURCE_METADATA.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (args.output_dir / "receipt.template.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": "generated_pending_endpoint_payload",
        "output_dir": str(args.output_dir.resolve()),
        "source_count": len(metadata["source_hashes"]),
        "coordinate_count": metadata["coordinate_order"].__len__(),
        "formal_admission": None,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
