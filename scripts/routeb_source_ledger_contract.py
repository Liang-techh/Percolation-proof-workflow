"""Reusable, fail-closed Route-B source-ledger contract.

This module records provenance only.  It never evaluates Julia, invents a
numeric cell, edits the workflow state, or promotes anything to a registry.
An optional numeric receipt is accepted only when it is keyed to the emitted
manifest and every field carries source-file/hash/cell/index provenance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


SCHEMA = "routeb.source_ledger.contract.v1"
RECEIPT_SCHEMA = "routeb.source_ledger.numeric_receipt.v1"

# These are the fields named by the existing GAK audit.  They are required
# numeric payloads, not declarations: source text alone cannot fill them.
REQUIRED_NUMERIC_FIELDS = (
    "q_box",
    "dq_box",
    "w_box",
    "M_q",
    "inverse_guard",
    "Cdq",
    "Gq",
    "a",
    "f",
    "l_true",
    "l_true_square_bounds",
    "kappa",
    "h_lo",
    "h_hi",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


# Paths are relative to the preserved original-target snapshot.  The final
# entry is intentionally absent from this workspace: the GAK audit records an
# expected digest for it, but no local bytes are substituted for that source.
SOURCE_SPECS = (
    {
        "path": "original_target/dhport_lib.jl",
        "role": "deployed DH/frame/mass/potential/central-FD/solve implementation",
        "expected_sha256": "aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936",
        "anchors": {
            "parameters": [5, 29], "frames": [31, 43], "mass": [46, 60],
            "potential": [63, 70], "central_fd": [73, 99], "solve": [102, 109],
        },
    },
    {
        "path": "original_target/routeB_export_traj.jl",
        "role": "trajectory cell generation, limits, source force, true residual and bound",
        "expected_sha256": "35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf",
        "anchors": {
            "block_and_domain": [35, 58], "limits": [81, 87],
            "source_force_and_residual": [169, 181],
            "manifest_semantics": [221, 240],
        },
    },
    {
        "path": "original_target/routeB_pmi_certificate.jl",
        "role": "PMI model and its explicit kc cross-term candidate",
        "expected_sha256": "235f4876ed1a3343f6d84f83c0079b4d279886585dc36aeb55b9fc0289177a77",
        "anchors": {
            "model_force": [91, 100], "domain": [104, 108],
            "runtime_source_force": [603, 606],
        },
    },
    {
        "path": "original_target/routeB_fourier_rational_probe.py",
        "role": "exact Fourier sidecar construction and source-order block projection",
        "expected_sha256": "9460181770e47be0ecbde43a8a29ef285da1168c3121fab18d5378c671401a7b",
        "anchors": {
            "constants": [17, 24], "frame_mass_build": [110, 150],
            "block_projection": [161, 175],
        },
    },
    {
        "path": "original_target/routeB_Mq_M0.csv",
        "role": "q=0 literal reference only; never a functional source receipt",
        "expected_sha256": "28d98ad71d1d6c2cbe830872cad9077f2f7b4e2d932794217eb68868fd2e2b40",
        "anchors": {"literal_table": [1, 7]},
    },
    {
        "path": "original_target/routeB_fourier_mass_full_rational.csv",
        "role": "exact Fourier coefficient sidecar; not a deployed Float64 receipt",
        "expected_sha256": "a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8",
        "anchors": {"coefficient_table": [1, 611]},
    },
    {
        "path": "current_exact/routeB_fourier_potential_rational.csv",
        "role": "exact potential coefficient sidecar; not a deployed Float64 receipt",
        "expected_sha256": "4ebbb10e32639f54b18f259cbb762c04f2be842a856cae85e1fe94dad5478b6c",
        "anchors": {"coefficient_table": [1, 18]},
    },
    {
        "path": "original_target/routeB_interval_bounds.jl",
        "role": "required interval cell evaluator referenced by GAK; no local substitute",
        "expected_sha256": "d51f7c43a1389edb4c4d5e1d6c492a864bcb55229f99e7032a1ec9c9239f99f1",
        "anchors": {"mass_interval": [179, 421], "cg_interval": [594, 628],
                    "box_metrics": [1198, 1364]},
    },
)


FIELD_SPECS = {
    "q_box": ("original_target/routeB_export_traj.jl", "initial state q coordinates and q limits", [45, 46], "q[1..6]"),
    "dq_box": ("original_target/routeB_export_traj.jl", "initial state dq coordinates", [141, 149], "dq[1..6]"),
    "w_box": ("original_target/routeB_export_traj.jl", "ramp disturbance coefficient and w(t)", [149, 166], "w scalar"),
    "M_q": ("original_target/dhport_lib.jl", "mass_matrix(q; regularization)", [46, 60], "M[1..6,1..6]"),
    "inverse_guard": ("original_target/dhport_lib.jl", "Mq \\ rhs implementation; residual/conditioning receipt required", [102, 109], "solve guard"),
    "Cdq": ("original_target/dhport_lib.jl", "central-FD Christoffel contraction", [73, 92], "Cdq[1..6]"),
    "Gq": ("original_target/dhport_lib.jl", "central-FD potential gradient", [93, 99], "Gq[1..6]"),
    "a": ("original_target/dhport_lib.jl", "exact_ddq returned acceleration", [102, 109], "a[1..6]"),
    "f": ("original_target/routeB_pmi_certificate.jl", "PMI candidate f1/f2; kc mismatch must remain explicit", [98, 99], "f[4],f[5]"),
    "l_true": ("original_target/routeB_export_traj.jl", "lv = Ival*f - M0_BB*a_ex", [173, 177], "l[4],l[5]"),
    "l_true_square_bounds": ("original_target/routeB_export_traj.jl", "bound and l2 emitted per trajectory sample", [178, 181], "bound,l2"),
    "kappa": ("original_target/routeB_export_traj.jl", "ratio l2/max(bound,...) is observational only", [180, 181], "scalar ratio"),
    "h_lo": ("original_target/routeB_interval_bounds.jl", "interval lower endpoint from box_metrics", [1198, 1364], "cell interval"),
    "h_hi": ("original_target/routeB_interval_bounds.jl", "interval upper endpoint from box_metrics", [1198, 1364], "cell interval"),
}


def _source_record(source_root: Path, spec: dict[str, Any]) -> dict[str, Any]:
    path = (source_root / spec["path"]).resolve()
    record = {
        "path": spec["path"],
        "role": spec["role"],
        "anchors": spec["anchors"],
        "expected_sha256": spec.get("expected_sha256"),
        "sha256": None,
        "exists": path.is_file(),
    }
    if path.is_file():
        record["sha256"] = sha256_file(path)
        record["hash_matches_expected"] = (
            not spec.get("expected_sha256") or record["sha256"] == spec["expected_sha256"]
        )
    else:
        record["hash_matches_expected"] = False
    return record


def _field_record(source_by_path: dict[str, dict[str, Any]], name: str) -> dict[str, Any]:
    path, description, lines, index = FIELD_SPECS[name]
    source = source_by_path[path]
    return {
        "name": name,
        "required": True,
        "value": None,
        "value_status": "missing_numeric_receipt",
        "source": {
            "path": path,
            "sha256": source["sha256"],
            "expected_sha256": source["expected_sha256"],
            "description": description,
            "line_anchors": lines,
            "index": index,
        },
    }


def _finite_numeric_tree(value: Any) -> bool:
    if isinstance(value, bool) or value is None:
        return False
    if isinstance(value, (int, float)):
        return math.isfinite(float(value))
    if isinstance(value, list):
        return bool(value) and all(_finite_numeric_tree(item) for item in value)
    if isinstance(value, dict):
        return bool(value) and all(_finite_numeric_tree(item) for item in value.values())
    return False


def _validate_receipt(receipt: Any, manifest: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    reasons: list[str] = []
    if not isinstance(receipt, dict) or receipt.get("schema") != RECEIPT_SCHEMA:
        return None, ["receipt schema is missing or unsupported"]
    if receipt.get("contract_sha256") != manifest["contract_sha256"]:
        reasons.append("receipt is not bound to this contract hash")
    cell = receipt.get("cell")
    if not isinstance(cell, dict):
        reasons.append("receipt cell is missing")
    else:
        for key in ("cell_id", "q_box", "dq_box", "w_box"):
            if key not in cell:
                reasons.append(f"receipt cell missing key: {key}")
    fields = receipt.get("fields")
    if not isinstance(fields, dict):
        reasons.append("receipt fields object is missing")
        return None, reasons
    source_by_path = {row["path"]: row for row in manifest["sources"]}
    for name in REQUIRED_NUMERIC_FIELDS:
        row = fields.get(name)
        if not isinstance(row, dict) or "value" not in row:
            reasons.append(f"receipt missing numeric field: {name}")
            continue
        if not _finite_numeric_tree(row["value"]):
            reasons.append(f"receipt field is not finite numeric data: {name}")
        provenance = row.get("provenance")
        if not isinstance(provenance, dict):
            reasons.append(f"receipt field missing provenance: {name}")
            continue
        path = provenance.get("path")
        source = source_by_path.get(path)
        if source is None:
            reasons.append(f"receipt field source is not in manifest: {name}")
            continue
        if provenance.get("sha256") != source.get("sha256") or not source.get("exists"):
            reasons.append(f"receipt field source hash is not current: {name}")
        if provenance.get("cell_id") != (cell or {}).get("cell_id"):
            reasons.append(f"receipt field cell binding mismatch: {name}")
        if not provenance.get("index") or not provenance.get("extractor"):
            reasons.append(f"receipt field index/extractor provenance missing: {name}")
    if reasons:
        return None, reasons
    return receipt, []


def build_manifest(source_root: Path, *, receipt: dict[str, Any] | None = None,
                   exporter_path: Path | None = None) -> dict[str, Any]:
    source_root = source_root.resolve(strict=True)
    sources = [_source_record(source_root, spec) for spec in SOURCE_SPECS]
    source_by_path = {row["path"]: row for row in sources}
    fields = [_field_record(source_by_path, name) for name in REQUIRED_NUMERIC_FIELDS]
    missing_sources = [row["path"] for row in sources
                       if not row["exists"] or not row["hash_matches_expected"]]
    missing_fields = [row["name"] for row in fields]
    manifest: dict[str, Any] = {
        "schema": SCHEMA,
        "contract_version": 1,
        "status": "FAIL_CLOSED",
        "sidecar_only": True,
        "verified": False,
        "registry_eligible": False,
        "source_root": str(source_root),
        "source_order": "Julia 1-based q/dq order [1,2,3,4,5,6]; block B=[4,5], complement D=[1,2,3,6]",
        "cell_key": ["cell_id", "eta", "sf", "q_box", "dq_box", "w_box"],
        "cell_index_contract": {
            "dimension": 6,
            "q_index": "q[1..6] and Lean Fin 6 values 0..5 require an explicit +1 adapter",
            "block45_julia": [4, 5],
            "block45_lean": [3, 4],
            "numeric_receipt_required": True,
        },
        "semantics": {
            "numeric_type": "Float64",
            "mass_regularization": "1e-6*I6",
            "fd_step": "1e-5 central FD for M and potential",
            "rounding": None,
            "coverage": "not established by this contract",
            "pmi_kc_mismatch": "PMI f1/f2 contains kc cross terms; dhport_lib tau does not",
        },
        "sources": sources,
        "numeric_fields": fields,
        "missing_source_bindings": missing_sources,
        "missing_numeric_fields": missing_fields,
        "numeric_receipt": None,
        "receipt_rejection_reasons": [],
    }
    if exporter_path is not None and exporter_path.is_file():
        manifest["exporter"] = {"path": str(exporter_path.resolve()),
                                 "sha256": sha256_file(exporter_path)}
    # Bind receipts to the structural contract before adding the receipt
    # summary.  This avoids a self-hash cycle in manifest_sha256.
    manifest["contract_sha256"] = canonical_sha256(manifest)
    if receipt is not None:
        accepted, reasons = _validate_receipt(receipt, manifest)
        if accepted is not None:
            manifest["status"] = "READY_FOR_COMPARATOR"
            manifest["missing_numeric_fields"] = []
            by_name = {row["name"]: row for row in manifest["numeric_fields"]}
            for name, payload in receipt["fields"].items():
                if name in by_name:
                    by_name[name]["value"] = payload["value"]
                    by_name[name]["value_status"] = "receipt_supplied_unverified"
            manifest["numeric_receipt"] = {
                "receipt_sha256": canonical_sha256(receipt),
                "cell": receipt["cell"],
                "status": "unverified_external_payload",
            }
        else:
            manifest["receipt_rejection_reasons"] = reasons
    payload = dict(manifest)
    manifest["manifest_sha256"] = canonical_sha256(payload)
    return manifest


def write_manifest(manifest: dict[str, Any], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args(argv)
    receipt = None
    if args.receipt:
        receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    manifest = build_manifest(args.source_root, receipt=receipt,
                              exporter_path=Path(__file__))
    write_manifest(manifest, args.output)
    print(json.dumps({"status": manifest["status"], "output": str(args.output.resolve()),
                      "missing_sources": manifest["missing_source_bindings"],
                      "missing_numeric_fields": manifest["missing_numeric_fields"]},
                     ensure_ascii=False, indent=2))
    return 0 if manifest["status"] == "READY_FOR_COMPARATOR" else 2


if __name__ == "__main__":
    raise SystemExit(main())
