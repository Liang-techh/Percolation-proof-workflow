"""Materialize validated sparse Route-B cell receipts.

This is deliberately a data-shaping boundary: it never computes or invents
geometry, rho, inverse, or source evidence.
"""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Iterable

BASE = 33
REQUIRED = ("cell_index", "source_hash", "geometry", "rho", "inverse", "outward")


class ReceiptInputError(ValueError):
    pass


def _records(path: Path) -> Iterable[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
        if isinstance(data, dict):
            data = data.get("records")
        if not isinstance(data, list):
            raise ReceiptInputError("JSON source must be an array or {records: [...]}")
        rows = data
    else:
        rows = [json.loads(line) for line in text.splitlines() if line.strip()]
    for n, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            raise ReceiptInputError(f"record {n}: expected object")
        yield row


def _index(value: Any) -> tuple[int, int, int, int]:
    if isinstance(value, dict):
        try:
            value = [value[k] for k in ("a2", "a3", "a4", "a5")]
        except KeyError as exc:
            raise ReceiptInputError("cell_index object requires a2,a3,a4,a5") from exc
    if not isinstance(value, list) or len(value) != 4:
        raise ReceiptInputError("cell_index must contain exactly four coordinates")
    if any(isinstance(x, bool) or not isinstance(x, int) or not 0 <= x < BASE for x in value):
        raise ReceiptInputError("cell_index coordinates must be integers in [0,32]")
    return tuple(value)


def normalize(row: dict[str, Any]) -> dict[str, Any]:
    missing = [k for k in REQUIRED if k not in row]
    if missing:
        raise ReceiptInputError("missing fields: " + ", ".join(missing))
    if row["outward"] is not True:
        raise ReceiptInputError("only outward=true records are accepted")
    if not isinstance(row["source_hash"], str) or not row["source_hash"].strip():
        raise ReceiptInputError("source_hash must be a non-empty string")
    if not isinstance(row["geometry"], dict) or not row["geometry"]:
        raise ReceiptInputError("geometry must be a non-empty object")
    if not isinstance(row["rho"], dict) or not row["rho"]:
        raise ReceiptInputError("rho must be a non-empty object")
    if not isinstance(row["inverse"], dict) or not row["inverse"]:
        raise ReceiptInputError("inverse must be a non-empty object")
    a2, a3, a4, a5 = _index(row["cell_index"])
    rank = a2 + BASE * a3 + BASE**2 * a4 + BASE**3 * a5
    return {
        "schema": "routeb-indexed-receipt-v1",
        "leaf_id": f"cell16/a2={a2}/a3={a3}/a4={a4}/a5={a5}",
        "rank": rank,
        "cell_index": [a2, a3, a4, a5],
        "source_hash": row["source_hash"],
        "geometry": row["geometry"],
        "rho": row["rho"],
        "inverse": row["inverse"],
        "outward": True,
    }


def materialize(source: Path, output: Path) -> int:
    if not source.is_file():
        raise ReceiptInputError(f"input does not exist: {source}")
    result = []
    seen: set[tuple[int, int, int, int]] = set()
    for row in _records(source):
        item = normalize(row)
        key = tuple(item["cell_index"])
        if key in seen:
            raise ReceiptInputError(f"duplicate address: {key}")
        seen.add(key)
        result.append(item)
    if not result:
        raise ReceiptInputError("input contains no records")
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=output.name + ".", dir=output.parent, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            for item in result:
                handle.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")
        os.replace(tmp, output)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    return len(result)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        count = materialize(args.input, args.output)
    except (OSError, json.JSONDecodeError, ReceiptInputError) as exc:
        parser.error(str(exc))
    print(json.dumps({"status": "written", "records": count, "output": str(args.output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
