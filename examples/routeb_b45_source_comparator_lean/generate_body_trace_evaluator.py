"""Generate the typed O1 per-body Fourier evaluator from the frozen trace.

This is a source-data transport generator, not a proof checker.  Every emitted
row keeps its body, matrix row/column, six-frequency label, and the numerator /
denominator tags of the real and imaginary rational coefficients.  The Lean
consumer defines the evaluator by an exact finite fold; it does not emit any
equality proof against the DH source.
"""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
WORKFLOW = HERE.parents[1]
CSV = WORKFLOW / "artifacts" / "task_routeb_body_trace_sink_current" / "outputs" / "routeB_fourier_mass_body_trace.csv"
OUT = HERE / "BodyTraceEvaluator.lean"
EXPECTED_SHA256 = "ae1f9cd7978c4cf23626b5c097eaaf4a2c70de9c8b86a31a61db12997cf4c3b9"
EXPECTED_HEADERS = [
    "body", "row", "col", "nu1", "nu2", "nu3", "nu4", "nu5", "nu6",
    "real_num", "real_den", "imag_num", "imag_den",
]


def z(value: str) -> str:
    return f"({int(value)} : ℤ)"


def fin(value: str) -> str:
    return f"({int(value) - 1} : Fin 6)"


def frequency(row: dict[str, str]) -> str:
    values = ", ".join(z(row[f"nu{k}"]) for k in range(1, 7))
    return f"![{values}]"


def rational_tag(row: dict[str, str], prefix: str) -> str:
    return (
        "{ numerator := " + z(row[f"{prefix}_num"]) +
        ", denominator := " + z(row[f"{prefix}_den"]) + " }"
    )


def row_literal(row: dict[str, str]) -> str:
    return (
        "{ body := " + fin(row["body"]) +
        ", row := " + fin(row["row"]) +
        ", col := " + fin(row["col"]) +
        ", frequency := " + frequency(row) +
        ", realCoeff := " + rational_tag(row, "real") +
        ", imagCoeff := " + rational_tag(row, "imag") + " }"
    )


def read_rows() -> list[dict[str, str]]:
    digest = hashlib.sha256(CSV.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"frozen body trace hash drift: {digest}")
    with CSV.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != EXPECTED_HEADERS:
            raise SystemExit(f"unexpected headers: {reader.fieldnames}")
        rows = list(reader)
    if len(rows) != 727:
        raise SystemExit(f"expected 727 body-trace rows, got {len(rows)}")
    for row in rows:
        for key in ("body", "row", "col"):
            value = int(row[key])
            if value not in range(1, 7):
                raise SystemExit(f"{key} outside 1..6: {value}")
        for key in ("real_den", "imag_den"):
            if int(row[key]) == 0:
                raise SystemExit(f"zero rational denominator in {key}")
    return rows


def emit(rows: list[dict[str, str]]) -> str:
    by_body: dict[int, list[dict[str, str]]] = {body: [] for body in range(1, 7)}
    for row in rows:
        by_body[int(row["body"])].append(row)

    lines = [
        "import Mathlib",
        "",
        "set_option autoImplicit false",
        "",
        "namespace RouteBO1PerBodyTraceGenerated",
        "",
        "noncomputable section",
        "",
        "/-- A rational coefficient with its source numerator/denominator labels. -/",
        "structure RationalTag where",
        "  numerator : ℤ",
        "  denominator : ℤ",
        "",
        "def RationalTag.toRat (c : RationalTag) : ℚ :=",
        "  c.numerator / c.denominator",
        "",
        "/-- One frozen source-trace row; no body or frequency label is discarded. -/",
        "structure BodyTraceRow where",
        "  body : Fin 6",
        "  row : Fin 6",
        "  col : Fin 6",
        "  frequency : Fin 6 → ℤ",
        "  realCoeff : RationalTag",
        "  imagCoeff : RationalTag",
        "",
        "/- Generated literally from routeB_fourier_mass_body_trace.csv. -/",
    ]
    block_names: list[str] = []
    for body in range(1, 7):
        name = f"bodyTraceRows{body}"
        block_names.append(name)
        lines += [f"def {name} : List BodyTraceRow :=", "  ["]
        lines += [f"    {row_literal(row)}," for row in by_body[body]]
        lines += ["  ]", ""]
    expression = block_names[0]
    for name in block_names[1:]:
        expression = f"({expression} ++ {name})"
    lines += [
        "def bodyTraceRows : List BodyTraceRow :=",
        f"  {expression}",
        "",
        "def rationalReal (c : RationalTag) : ℝ :=",
        "  (c.toRat : ℝ)",
        "",
        "def rationalImag (c : RationalTag) : ℝ :=",
        "  (c.toRat : ℝ)",
        "",
        "def tracePhase (frequency : Fin 6 → ℤ) (q : Fin 6 → ℝ) : ℝ :=",
        "  ∑ k : Fin 6, (frequency k : ℝ) * q k",
        "",
        "/-- Real-valued lift of one tagged complex Fourier coefficient. -/",
        "def traceAtom (r : BodyTraceRow) (q : Fin 6 → ℝ) : ℝ :=",
        "  rationalReal r.realCoeff * Real.cos (tracePhase r.frequency q) -",
        "    rationalImag r.imagCoeff * Real.sin (tracePhase r.frequency q)",
        "",
        "def traceRowContribution (body row col : Fin 6)",
        "    (q : Fin 6 → ℝ) (r : BodyTraceRow) : ℝ :=",
        "  if r.body = body ∧ r.row = row ∧ r.col = col then",
        "    traceAtom r q",
        "  else 0",
        "",
        "/-- Concrete body-labelled evaluator obtained by an exact finite fold. -/",
        "def bodyTraceEvaluator (body : Fin 6) (q : Fin 6 → ℝ)",
        "    (row col : Fin 6) : ℝ :=",
        "  bodyTraceRows.foldl",
        "    (fun acc r => acc + traceRowContribution body row col q r) 0",
        "",
        "/-- The six concrete body slices used by the O1 adapter. -/",
        "def bodyTraceEvaluator_1 := bodyTraceEvaluator (0 : Fin 6)",
        "def bodyTraceEvaluator_2 := bodyTraceEvaluator (1 : Fin 6)",
        "def bodyTraceEvaluator_3 := bodyTraceEvaluator (2 : Fin 6)",
        "def bodyTraceEvaluator_4 := bodyTraceEvaluator (3 : Fin 6)",
        "def bodyTraceEvaluator_5 := bodyTraceEvaluator (4 : Fin 6)",
        "def bodyTraceEvaluator_6 := bodyTraceEvaluator (5 : Fin 6)",
        "",
        "end",
        "end RouteBO1PerBodyTraceGenerated",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    OUT.write_text(emit(read_rows()), encoding="utf-8", newline="\n")
    print({"output": str(OUT), "rows": 727, "csv_sha256": EXPECTED_SHA256})


if __name__ == "__main__":
    main()
