"""Generate a Lean data payload from the frozen Route-B rational mass CSV.

This is a transport/checking script, not a proof.  Its output is deliberately
only literal Lean data; the Lean file supplies the kernel-checked table
invariants and conditional map theorem.  It never emits a theorem identifying
the exactized DH map with the CSV map.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKFLOW = HERE.parents[1]
CSV = WORKFLOW / "examples" / "routeb_source_binding_audit" / "snapshots" / "current_exact" / "routeB_fourier_mass_full_rational.csv"
OUT = HERE / "PayloadRows.lean"
META = HERE / "PAYLOAD_METADATA.json"
FACTS = HERE / "PayloadFacts.lean"
EXPECTED_SHA256 = "a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8"


def lean_int(value: str) -> str:
    return value


def lean_rat(num: str, den: str) -> str:
    # Keep every CSV rational visible in the generated source.  The expected
    # type is supplied by the Row.coefficient field, so no theorem is hidden
    # behind an opaque parser or a floating-point conversion.
    return f"({num} : ℚ) / {den}"


def row_literal(row: dict[str, str]) -> str:
    freq = " ".join(f"({lean_int(row[f'nu{k}'])})" for k in range(1, 7))
    real = lean_rat(row["real_num"], row["real_den"])
    imag = lean_rat(row["imag_num"], row["imag_den"])
    return (
        "{ entry := ("
        f"{int(row['row']) - 1}, {int(row['col']) - 1}"
        "), frequency := freq "
        f"{freq}, coefficient := ({real}, {imag}) }}"
    )


def main() -> None:
    digest = hashlib.sha256(CSV.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"frozen CSV hash drift: {digest}")
    with CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 610:
        raise SystemExit(f"expected 610 rows, got {len(rows)}")
    keys = [
        (
            int(r["row"]),
            int(r["col"]),
            *(int(r[f"nu{k}"]) for k in range(1, 7)),
        )
        for r in rows
    ]
    if len(set(keys)) != len(keys):
        raise SystemExit("CSV contains duplicate matrix-entry/frequency keys")
    entries = {(r["row"], r["col"]) for r in rows}
    expected_entries = {(str(i), str(j)) for i in range(1, 7) for j in range(1, 7)}
    missing = sorted(expected_entries - entries, key=lambda x: (int(x[0]), int(x[1])))
    if missing != [("4", "5"), ("5", "4"), ("5", "6"), ("6", "5")]:
        raise SystemExit(f"unexpected missing entries: {missing}")

    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    entry_order: list[tuple[str, str]] = []
    for row in rows:
        entry = (row["row"], row["col"])
        if entry not in grouped:
            grouped[entry] = []
            entry_order.append(entry)
        grouped[entry].append(row)
    lines = [
        "import FiniteTableReification",
        "",
        "set_option autoImplicit false",
        "",
        "namespace RouteBFourierPayloadLean",
        "",
        "open RouteBFourierSourceBinding",
        "",
        "/-- Six-coordinate literal constructor used by the generated payload. -/",
        "def freq (a₁ a₂ a₃ a₄ a₅ a₆ : ℤ) : Frequency :=",
        "  ![a₁, a₂, a₃, a₄, a₅, a₆]",
        "",
        "/- Generated from the frozen CSV by generate_payload.py. -/",
    ]
    block_names: list[str] = []
    for index, entry in enumerate(entry_order):
        name = f"payloadRows{int(entry[0]) - 1}{int(entry[1]) - 1}"
        block_names.append(name)
        chunk = grouped[entry]
        lines.append(f"def {name} : List Row :=")
        lines.append("  [")
        lines.extend(f"    {row_literal(row)}," for row in chunk)
        lines.append("  ]")
        lines.append("")
    lines.append("def payloadRows : List Row :=")
    expression = block_names[0]
    for block_name in block_names[1:]:
        expression = f"({expression} ++ {block_name})"
    lines.append(f"  {expression}")
    lines.append("")
    entries_literal = ", ".join(
        f"({int(row) - 1}, {int(col) - 1})" for row, col in entry_order
    )
    lines.append("def payloadNonemptyEntries : Finset Entry :=")
    lines.append(f"  [{entries_literal}].toFinset")
    lines.append("")
    lines.append("end RouteBFourierPayloadLean")
    lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")

    fact_lines = [
        "import FiniteTableReification",
        "import PayloadRows",
        "",
        "set_option autoImplicit false",
        "set_option maxRecDepth 100000",
        "set_option maxHeartbeats 100000000",
        "",
        "namespace RouteBFourierPayloadLean",
        "",
        "open RouteBFourierSourceBinding",
        "",
        "/-- Entry labels are used only to compose the per-entry key proofs. -/",
        "def EntriesDisjoint (xs ys : List Row) : Prop :=",
        "  (xs.map Row.entry).toFinset ∩ (ys.map Row.entry).toFinset = ∅",
        "",
        "theorem append_keys_nodup {xs ys : List Row}",
        "    (hx : (xs.map Row.key).Nodup)",
        "    (hy : (ys.map Row.key).Nodup)",
        "    (hxy : EntriesDisjoint xs ys) :",
        "    ((xs ++ ys).map Row.key).Nodup := by",
        "  rw [List.map_append]",
        "  apply List.nodup_append.mpr",
        "  refine ⟨hx, hy, ?_⟩",
        "  intro k hk l hl",
        "  rcases List.mem_map.mp hk with ⟨r, hr, hkr⟩",
        "  rcases List.mem_map.mp hl with ⟨s, hs, hks⟩",
        "  intro heq",
        "  have hrEntry : r.entry ∈ (xs.map Row.entry).toFinset := by",
        "    exact List.mem_toFinset.mpr (List.mem_map.mpr ⟨r, hr, rfl⟩)",
        "  have hsEntry : r.entry ∈ (ys.map Row.entry).toFinset := by",
        "    have heqEntry : r.entry = s.entry :=",
        "      congrArg Prod.fst (hkr.trans (heq.trans hks.symm))",
        "    rw [heqEntry]",
        "    exact List.mem_toFinset.mpr (List.mem_map.mpr ⟨s, hs, rfl⟩)",
        "  have hboth : r.entry ∈ (xs.map Row.entry).toFinset ∩",
        "      (ys.map Row.entry).toFinset := Finset.mem_inter.mpr ⟨hrEntry, hsEntry⟩",
        "  rw [hxy] at hboth",
        "  simp at hboth",
        "",
    ]
    block_nodup_names: list[str] = []
    for name in block_names:
        theorem_name = f"{name}_keys_nodup"
        block_nodup_names.append(theorem_name)
        fact_lines.extend(
            [
                f"theorem {theorem_name} : ({name}.map Row.key).Nodup := by",
                "  decide",
                "",
            ]
        )
    prefix_name = block_nodup_names[0]
    prefix_expr = block_names[0]
    for index in range(1, len(block_names)):
        block_name = block_names[index]
        next_prefix = f"payload_prefix_{index:02d}_keys_nodup"
        fact_lines.extend(
            [
                f"theorem {next_prefix} :",
                f"    (({prefix_expr} ++ {block_name}).map Row.key).Nodup := by",
                f"  apply append_keys_nodup {prefix_name} {block_nodup_names[index]} ",
                f"  change ({prefix_expr}.map Row.entry).toFinset ∩",
                f"      ({block_name}.map Row.entry).toFinset = ∅",
                "  decide",
                "",
            ]
        )
        prefix_expr = f"({prefix_expr} ++ {block_name})"
        prefix_name = next_prefix
    fact_lines.extend(
        [
            "theorem payload_keys_nodup : (payloadRows.map Row.key).Nodup := by",
            f"  exact {prefix_name}",
            "",
            "end RouteBFourierPayloadLean",
            "",
        ]
    )
    FACTS.write_text("\n".join(fact_lines), encoding="utf-8")
    META.write_text(
        json.dumps(
            {
                "status": "LITERAL_PAYLOAD_GENERATED_FROM_FROZEN_CSV",
                "csv_sha256": digest,
                "csv_rows": len(rows),
                "unique_keys": len(set(keys)),
                "nonempty_matrix_entries": len(entries),
                "full_matrix_entries": 36,
                "missing_zero_entries": ["(4,5)", "(5,4)", "(5,6)", "(6,5)"],
                "per_entry_blocks": len(block_names),
                "generator_is_proof": False,
                "exactized_dh_map_equality_proved_in_lean": False,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"generated={OUT}")
    print(f"csv_sha256={digest}")
    print(f"csv_rows={len(rows)}")
    print(f"unique_keys={len(set(keys))}")
    print(f"nonempty_matrix_entries={len(entries)}")


if __name__ == "__main__":
    main()
