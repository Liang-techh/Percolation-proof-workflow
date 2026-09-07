"""Emit a fail-closed support/entry target for the O1 body=6 frontier.

The current body-labelled trace uses label 6 for the 610-row aggregate-shaped
bucket.  This generator records that fact and emits only a machine-readable
support decomposition.  It never treats the bucket as a proved human-body-6
source evaluator.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
WORKFLOW = HERE.parents[1]
TRACE = WORKFLOW / "artifacts" / "task_routeb_body_trace_sink_current" / "outputs" / "routeB_fourier_mass_body_trace.csv"
FROZEN = WORKFLOW / "artifacts" / "task_routeb_body_trace_sink_current" / "source_snapshot" / "routeB_fourier_mass_full_rational.csv"
OUT = HERE / "O1_BODY_6_SUPPORT_TARGET.json"
TRACE_SHA256 = "ae1f9cd7978c4cf23626b5c097eaaf4a2c70de9c8b86a31a61db12997cf4c3b9"
FROZEN_SHA256 = "a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8"
HEADERS = [
    "body", "row", "col", "nu1", "nu2", "nu3", "nu4", "nu5", "nu6",
    "real_num", "real_den", "imag_num", "imag_den",
]


def read_csv(path: Path, *, body_label: str | None = None) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if body_label is None:
            expected = [x for x in HEADERS if x != "body"]
            if reader.fieldnames != expected:
                raise SystemExit(f"unexpected frozen headers: {reader.fieldnames}")
        elif reader.fieldnames != HEADERS:
            raise SystemExit(f"unexpected trace headers: {reader.fieldnames}")
        rows = list(reader)
    if body_label is not None:
        rows = [row for row in rows if row["body"] == body_label]
    return rows


def block(row: int, col: int) -> str:
    distal = {4, 5}
    r_distal = row in distal
    c_distal = col in distal
    if r_distal and c_distal:
        return "B_B"
    if r_distal:
        return "B_D"
    if c_distal:
        return "D_B"
    return "D_D"


def entry_summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    grouped: dict[tuple[int, int], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(int(row["row"]), int(row["col"]))].append(row)
    result: list[dict[str, object]] = []
    for (row, col), values in sorted(grouped.items()):
        frequencies = [tuple(int(value[f"nu{k}"]) for k in range(1, 7)) for value in values]
        result.append({
            "row": row,
            "col": col,
            "block": block(row, col),
            "term_count": len(values),
            "frequency_support_count": len(set(frequencies)),
            "frequency_coordinate_min": [min(freq[k] for freq in frequencies) for k in range(6)],
            "frequency_coordinate_max": [max(freq[k] for freq in frequencies) for k in range(6)],
            "frequency_l1_max": max(sum(abs(x) for x in freq) for freq in frequencies),
            "target": "sum over tagged rows of realCoeff*cos(sum(nu_k*q_k))-imagCoeff*sin(sum(nu_k*q_k))",
        })
    return result


def main() -> None:
    trace_digest = hashlib.sha256(TRACE.read_bytes()).hexdigest()
    frozen_digest = hashlib.sha256(FROZEN.read_bytes()).hexdigest()
    if trace_digest != TRACE_SHA256:
        raise SystemExit(f"body trace hash drift: {trace_digest}")
    if frozen_digest != FROZEN_SHA256:
        raise SystemExit(f"frozen aggregate hash drift: {frozen_digest}")

    body6 = read_csv(TRACE, body_label="6")
    frozen = read_csv(FROZEN)
    if len(body6) != 610:
        raise SystemExit(f"expected the body=6 bucket to contain 610 rows, got {len(body6)}")
    if len(frozen) != 610:
        raise SystemExit(f"expected the frozen aggregate to contain 610 rows, got {len(frozen)}")

    entries = entry_summary(body6)
    blocks: dict[str, dict[str, object]] = {}
    for name in ("D_D", "D_B", "B_D", "B_B"):
        selected = [entry for entry in entries if entry["block"] == name]
        blocks[name] = {
            "entry_count": len(selected),
            "term_count": sum(int(entry["term_count"]) for entry in selected),
            "entries": selected,
        }

    payload = {
        "schema": "routeb.o1.true_dh_exact_typed_mdd_source.body_6_support_entry_target.v1",
        "status": "OPEN_BODY_LABEL_SEMANTIC_MISMATCH",
        "body_label": 6,
        "zero_based_body": 5,
        "source_key": "routeb-exact-fourier-mass:a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8|mu=1/1000000|contract=exp(i*nu*q)",
        "state_key": "routeb-qcell:center=(0,0,0,0,0,0)|radius=1/1000|B=(4,5)|D=(1,2,3,6)|orientation=M_BD[B,D],DeltaM_DB[D,B]|norm=induced_infinity",
        "inputs": {
            "body_trace_path": "artifacts/task_routeb_body_trace_sink_current/outputs/routeB_fourier_mass_body_trace.csv",
            "body_trace_sha256": trace_digest,
            "selected_body_bucket_rows": len(body6),
            "frozen_610_row_path": "artifacts/task_routeb_body_trace_sink_current/source_snapshot/routeB_fourier_mass_full_rational.csv",
            "frozen_610_row_sha256": frozen_digest,
            "frozen_row_count": len(frozen),
            "csv_is_proof": False
        },
        "semantic_boundary": {
            "observed": "body=6 bucket has the complete 610-row aggregate-shaped support, not an isolated human body-6 source slice",
            "body6_source_binding": False,
            "aggregate_binding": False,
            "admissible_as_h_body_6": False,
            "smallest_missing_artifact": "a separately emitted exact Fourier slice for human body 6 with body=6 labels, sourceBodyMass q 5 binding, and its own source comparator key"
        },
        "typed_target_schema": {
            "source_term": "sourceBodyMass q (5 : Fin 6) i j",
            "required_trace_term": "body6TraceEvaluator q i j",
            "entry_target": "forall q i j, sourceBodyMass q 5 i j = body6TraceEvaluator q i j",
            "support_evaluator": "sum tagged rows selected by exact (row,col), with rational real/imag coefficients and phase sum nu_k*q_k",
            "target_status": "BLOCKED_UNTIL_BODY6_SLICE_IS_SEMANTICALLY_BOUND"
        },
        "sparse_block_summary": {
            "matrix_index_convention": "one-based CSV row/col; B=(4,5), D=(1,2,3,6)",
            "blocks": blocks,
            "total_entry_count": len(entries),
            "total_term_count": len(body6)
        },
        "proof_decomposition": [
            {
                "leaf": "L0_body6_label_binding",
                "target": "prove the emitted body=6 rows are the human body-6 term, not aggregate rows",
                "status": "OPEN_REQUIRED_SOURCE_ARTIFACT"
            },
            {
                "leaf": "L1_body6_source_expansion",
                "target": "expand sourceBodyMass q 5 entrywise through bodyMass/bodyJv/bodyJw",
                "status": "BLOCKED_BY_L0"
            },
            {
                "leaf": "L2_body6_trace_reification",
                "target": "define body6TraceEvaluator from the correctly labelled sparse support",
                "status": "BLOCKED_BY_L0"
            },
            {
                "leaf": "L3_entrywise_bridge",
                "target": "prove sourceBodyMass q 5 i j = body6TraceEvaluator q i j for every supported entry and zero complement",
                "status": "BLOCKED_BY_L0_L1_L2"
            },
            {
                "leaf": "L4_h_body_6_composition",
                "target": "compose the source and trace premises into h_body_6",
                "status": "BLOCKED"
            }
        ],
        "fail_closed": {
            "source_expansion_proved": False,
            "trace_fold_proved": False,
            "h_body_6_proved": False,
            "registry_eligible": False,
            "comparator_accepted": False,
            "formal_certificate_allowed": False
        },
        "next_exact_action": "Obtain a separate canonical per-body human-body-6 export; only then generate a Lean body6TraceEvaluator and entrywise source/trace targets."
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print({"output": str(OUT), "status": payload["status"], "selected_rows": len(body6), "entries": len(entries)})


if __name__ == "__main__":
    main()
