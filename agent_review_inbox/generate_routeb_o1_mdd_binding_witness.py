"""Fail-closed generator for the minimal Route-B O1 M_DD binding witness.

This is a source-receipt adapter generator, not a proof checker.  It emits a
Lean target only after exact key/order/statement fields are present.  It never
infers a matrix equality from hashes, dimensions, or a determinant number.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_']*$")
EXPECTED_ORDER = [1, 2, 3, 6]
EXPECTED_DIDX = [0, 1, 2, 5]


def _text(value: Any) -> str | None:
    return value if isinstance(value, str) and value.strip() else None


def _ident(value: Any, name: str, missing: list[str]) -> str | None:
    result = _text(value)
    if result is None:
        missing.append(name)
    elif not IDENT.fullmatch(result):
        missing.append(f"{name}_not_a_Lean_identifier")
    return result


def _same(component: dict[str, Any], field: str, anchor: Any,
          missing: list[str], label: str) -> None:
    value = component.get(field)
    if value != anchor:
        missing.append(f"{label}.{field}_mismatch")


def _expected_statements(m: str, mu: str, q: str,
                         mdd: str, inv: str) -> dict[str, str]:
    block = f"{mdd} = M_DD45_at {m} {mu} {q}"
    projected = f"M_DD45_at {m} {mu} {q}"
    return {
        "h_MDD_def": block,
        "h_inv_def": f"{inv} = ({projected})⁻¹",
        "hdet": f"({projected}).det ≠ 0",
        "h_left": f"{inv} * {projected} = (1 : Matrix (Fin 4) (Fin 4) ℝ)",
    }


def generate_witness(receipt: dict[str, Any]) -> dict[str, Any]:
    """Return a ready-to-compile target or a precise fail-closed obstruction."""

    missing: list[str] = []
    path = receipt.get("path")
    if path not in {"A", "B"}:
        missing.append("path_must_be_A_or_B")

    components = receipt.get("components")
    if not isinstance(components, dict):
        return {
            "status": "OPEN_MISSING_SAME_KEY_MDD_SOURCE_RECEIPT",
            "missing": ["components.source", "components.block",
                        "components.inverse"],
            "lean": None,
        }

    source = components.get("source")
    block = components.get("block")
    inverse = components.get("inverse")
    for label, component in (("source", source), ("block", block),
                             ("inverse", inverse)):
        if not isinstance(component, dict):
            missing.append(f"components.{label}")

    if missing:
        return {
            "status": "OPEN_MISSING_SAME_KEY_MDD_SOURCE_RECEIPT",
            "missing": sorted(set(missing)),
            "lean": None,
        }

    m = _ident(source.get("M_ident"), "source.M_ident", missing)
    mu = _ident(source.get("mu_ident"), "source.mu_ident", missing)
    q = _ident(source.get("q_ident"), "source.q_ident", missing)
    mdd = _ident(block.get("M_DD_ident"), "block.M_DD_ident", missing)
    inv = _ident(inverse.get("M_DD_inv_ident"),
                 "inverse.M_DD_inv_ident", missing)

    source_key = _text(source.get("source_key"))
    state_key = _text(source.get("state_key"))
    if source_key is None:
        missing.append("source.source_key")
    if state_key is None:
        missing.append("source.state_key")
    source_hash = _text(source.get("source_sha256"))
    if source_hash is None:
        missing.append("source.source_sha256")

    for label, component in (("block", block), ("inverse", inverse)):
        _same(component, "source_key", source_key, missing, label)
        _same(component, "state_key", state_key, missing, label)
        _same(component, "mu_ident", mu, missing, label)
        _same(component, "q_ident", q, missing, label)
        _same(component, "block_order_one_based", EXPECTED_ORDER,
              missing, label)
        _same(component, "didx_zero_based", EXPECTED_DIDX, missing, label)

    if source.get("block_order_one_based") != EXPECTED_ORDER:
        missing.append("source.block_order_one_based")
    if source.get("didx_zero_based") != EXPECTED_DIDX:
        missing.append("source.didx_zero_based")

    if m is not None and mu is not None and q is not None and \
            mdd is not None and inv is not None:
        expected = _expected_statements(m, mu, q, mdd, inv)
        if block.get("h_MDD_def_statement") != expected["h_MDD_def"]:
            missing.append("block.h_MDD_def_statement")
        if path == "A":
            if inverse.get("h_inv_def_statement") != expected["h_inv_def"]:
                missing.append("inverse.h_inv_def_statement")
            if source.get("hdet_statement") != expected["hdet"]:
                missing.append("source.hdet_statement")
        elif inverse.get("h_left_statement") != expected["h_left"]:
            missing.append("inverse.h_left_statement")

    if missing:
        return {
            "status": "OPEN_MISSING_SAME_KEY_MDD_SOURCE_RECEIPT",
            "missing": sorted(set(missing)),
            "lean": None,
            "required_path": path,
        }

    assert m is not None and mu is not None and q is not None
    assert mdd is not None and inv is not None
    projected = f"M_DD45_at {m} {mu} {q}"
    if path == "A":
        lean = f"""import Mathlib.LinearAlgebra.Matrix.NonsingularInverse

theorem generated_typed_MDD_left_inverse
    (h_MDD_def : {mdd} = {projected})
    (h_inv_def : {inv} = ({projected})⁻¹)
    (hdet : ({projected}).det ≠ 0) :
    {inv} * {mdd} = (1 : Matrix (Fin 4) (Fin 4) ℝ) := by
  rw [h_inv_def, h_MDD_def]
  exact Matrix.nonsing_inv_mul _ (isUnit_iff_ne_zero.mpr hdet)
"""
        status = "READY_TYPED_PATH_A_TARGET_NOT_VERIFIED"
    else:
        lean = f"""theorem generated_direct_same_key_left_inverse
    (h_MDD_def : {mdd} = {projected})
    (h_left : {inv} * {projected} =
      (1 : Matrix (Fin 4) (Fin 4) ℝ)) :
    {inv} * {mdd} = (1 : Matrix (Fin 4) (Fin 4) ℝ) := by
  rw [h_MDD_def]
  exact h_left
"""
        status = "READY_TYPED_PATH_B_TARGET_NOT_VERIFIED"

    return {
        "status": status,
        "missing": [],
        "keys": {
            "source_key": source_key,
            "state_key": state_key,
            "source_sha256": source_hash,
            "mu": mu,
            "q": q,
            "block_order_one_based": EXPECTED_ORDER,
            "didx_zero_based": EXPECTED_DIDX,
        },
        "lean": lean,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: generate_routeb_o1_mdd_binding_witness.py RECEIPT.json",
              file=sys.stderr)
        return 2
    payload = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(generate_witness(payload), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
