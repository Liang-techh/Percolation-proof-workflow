"""Check the generated O1 body-trace transport without claiming Lean proof."""
from __future__ import annotations

import csv
from hashlib import sha256
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "artifacts/task_routeb_body_trace_sink_current/outputs/routeB_fourier_mass_body_trace.csv"
LEAN = ROOT / "examples/routeb_b45_source_comparator_lean/BodyTraceEvaluator.lean"
OUT = ROOT / "examples/routeb_b45_source_comparator_lean/O1_BODY_TRACE_EVALUATOR_CHECK.json"
EXPECTED_CSV_SHA256 = "AE1F9CD7978C4CF23626B5C097EAAF4A2C70DE9C8B86A31A61DB12997CF4C3B9"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    if digest(CSV) != EXPECTED_CSV_SHA256:
        raise AssertionError("body trace CSV hash drift")
    text = LEAN.read_text(encoding="utf-8")
    with CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 727:
        raise AssertionError(f"expected 727 rows, got {len(rows)}")
    counts = {str(body): sum(int(row["body"]) == body for row in rows)
              for body in range(1, 7)}
    if sum(counts.values()) != 727 or any(value == 0 for value in counts.values()):
        raise AssertionError(f"invalid body distribution: {counts}")
    if text.count("structure BodyTraceRow where") != 1:
        raise AssertionError("BodyTraceRow definition missing or duplicated")
    if text.count("structure RationalTag where") != 1:
        raise AssertionError("RationalTag definition missing or duplicated")
    for token in ("def bodyTraceEvaluator", "bodyTraceRows.foldl", "traceAtom",
                  "frequency : Fin 6 → ℤ", "realCoeff : RationalTag",
                  "imagCoeff : RationalTag"):
        if token not in text:
            raise AssertionError(f"generated evaluator missing {token}")
    section_counts: dict[str, int] = {}
    for body in range(1, 7):
        start = text.index(f"def bodyTraceRows{body} :")
        end = min((text.index(f"def bodyTraceRows{next_body} :", start)
                   for next_body in range(body + 1, 7)), default=text.index("def bodyTraceRows :", start))
        section = text[start:end]
        section_counts[str(body)] = len(re.findall(rf"body := \({body - 1} : Fin 6\)", section))
    if section_counts != counts:
        raise AssertionError(f"generated body section mismatch: {section_counts} != {counts}")
    receipt = {
        "schema": "routeb.o1.body_trace_evaluator.check.v1",
        "status": "PASS_GENERATED_TYPED_EVALUATOR_FAIL_CLOSED",
        "csv_sha256": digest(CSV),
        "lean_sha256": digest(LEAN),
        "row_count": len(rows),
        "body_counts": counts,
        "labels_retained": ["body", "row", "col", "frequency", "realCoeff", "imagCoeff"],
        "finite_fold_present": True,
        "lean_compiled": False,
        "h_body_proven": False,
        "source_binding_proven": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(receipt)


if __name__ == "__main__":
    main()
