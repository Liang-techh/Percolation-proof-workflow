"""Fail-closed, read-only validation of a Route-B full-state source manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

STATE_ORDER = [f"q{i}" for i in range(1, 7)] + [f"v{i}" for i in range(1, 7)] + ["w", "c"]
REQUIRED_METADATA = ("domain", "normalization", "fd", "float64_marker")


class ValidationError(ValueError):
    pass


def _required(obj: dict, key: str, where: str):
    if key not in obj:
        raise ValidationError(f"{where}: missing field {key}")
    return obj[key]


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def validate(manifest: dict, receipt: dict, *, source_root: Path) -> dict:
    """Validate only declared evidence; never imports workflow state or writes files."""
    if not isinstance(manifest, dict) or not isinstance(receipt, dict):
        raise ValidationError("manifest and receipt must be JSON objects")
    if _required(manifest, "state_order", "manifest") != STATE_ORDER:
        raise ValidationError("manifest: state_order must be exactly q1..q6,v1..v6,w,c")
    if _required(receipt, "state_order", "receipt") != STATE_ORDER:
        raise ValidationError("receipt: state_order must be exactly q1..q6,v1..v6,w,c")
    for name in REQUIRED_METADATA:
        if _required(manifest, name, "manifest") != _required(receipt, name, "receipt"):
            raise ValidationError(f"{name}: manifest and receipt differ")
    if manifest["float64_marker"] is not True or receipt["float64_marker"] is not True:
        raise ValidationError("float64_marker must be literal true")
    sources = _required(manifest, "sources", "manifest")
    receipt_sources = _required(receipt, "sources", "receipt")
    if not isinstance(sources, list) or not sources or not isinstance(receipt_sources, list):
        raise ValidationError("sources must be non-empty arrays")
    if sources != receipt_sources:
        raise ValidationError("manifest and receipt source declarations differ")
    checked = []
    for i, row in enumerate(sources):
        if not isinstance(row, dict):
            raise ValidationError(f"sources[{i}] must be an object")
        rel = _required(row, "path", f"sources[{i}]")
        expected = _required(row, "sha256", f"sources[{i}]")
        if not isinstance(rel, str) or Path(rel).is_absolute() or ".." in Path(rel).parts:
            raise ValidationError(f"sources[{i}].path is unsafe")
        if not isinstance(expected, str) or len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
            raise ValidationError(f"sources[{i}].sha256 is not lowercase SHA-256")
        path = (source_root / rel).resolve()
        if not path.is_relative_to(source_root.resolve()) or not path.is_file():
            raise ValidationError(f"sources[{i}]: source file missing: {rel}")
        actual = _sha256(path)
        if actual != expected:
            raise ValidationError(f"sources[{i}]: hash mismatch for {rel}")
        checked.append({"path": rel, "sha256": actual})
    return {"schema": "routeb-full-state-source-binding-manifest-report-v1",
            "status": "passed", "state_count": 14, "sources_checked": checked,
            "metadata_checked": list(REQUIRED_METADATA),
            "binding_conclusion": None}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--receipt", type=Path, required=True)
    p.add_argument("--source-root", type=Path, required=True)
    p.add_argument("--report", type=Path)
    args = p.parse_args(argv)
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
        result = validate(manifest, receipt, source_root=args.source_root)
        code = 0
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        result = {"schema": "routeb-full-state-source-binding-manifest-report-v1",
                  "status": "failed", "error": str(exc), "binding_conclusion": None}
        code = 1
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        args.report.write_text(text, encoding="utf-8")
    print(text, end="")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
