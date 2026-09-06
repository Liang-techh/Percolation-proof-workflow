"""Emit the isolated Route-B source-ledger contract sidecar.

The recorder writes only a new artifact directory.  It deliberately does not
load or save state.json and has no code path that writes a verified registry.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from routeb_source_ledger_contract import build_manifest, write_manifest


def report_text(manifest: dict) -> str:
    missing_sources = manifest["missing_source_bindings"]
    missing_fields = manifest["missing_numeric_fields"]
    lines = [
        "# Route-B source-ledger contract",
        "",
        f"Status: **{manifest['status']}**",
        "",
        "This is a deterministic, sidecar-only provenance export. It does not",
        "verify Julia execution, prove interval coverage, or write a registry.",
        "",
        f"- Manifest SHA-256: `{manifest['manifest_sha256']}`",
        f"- Source root: `{manifest['source_root']}`",
        f"- Verified: `{manifest['verified']}`",
        f"- Registry eligible: `{manifest['registry_eligible']}`",
        f"- Source bindings missing or drifted: `{len(missing_sources)}`",
        f"- Numeric receipt fields missing: `{len(missing_fields)}`",
        "",
        "## Fail-closed interpretation",
        "",
        "A source declaration, q=0 CSV, exact Fourier sidecar, Monte Carlo row,",
        "or symbolic/Lean adapter is not copied into a numeric receipt. A future",
        "receipt must bind the manifest hash, cell_id, source SHA-256, index and",
        "extractor for every required field. Any mismatch keeps this export closed.",
        "",
        "## Missing physical/runtime fields",
        "",
    ]
    lines.extend(f"- `{name}`" for name in missing_fields)
    if not missing_fields:
        lines.extend(["- none (payload is still unverified and comparator-pending)"])
    lines.extend(["", "## Missing source bindings", ""])
    lines.extend(f"- `{name}`" for name in missing_sources)
    if not missing_sources:
        lines.extend(["- none"])
    lines.extend([
        "", "## Explicit semantic seams", "",
        "- `dhport_lib.jl` uses Float64 DH, mass regularization `1e-6`, and central FD `1e-5`.",
        "- `routeB_pmi_certificate.jl` adds `kc*q5`/`kc*q4` to the PMI candidate force, while the deployed `tau` does not; this remains a residual mismatch.",
        "- `Mq \\ rhs` needs a residual/conditioning binding; a finite vector alone is not an exact-real solve theorem.",
        "- No registry or persistent DAG state was modified by this recorder.",
        "",
    ])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=False)
    manifest = build_manifest(args.source_root, exporter_path=Path(__file__).resolve())
    write_manifest(manifest, output_dir / "manifest.json")
    (output_dir / "REPORT.md").write_text(report_text(manifest), encoding="utf-8")
    print(json.dumps({"status": manifest["status"], "manifest": str((output_dir / "manifest.json").resolve()),
                      "report": str((output_dir / "REPORT.md").resolve()),
                      "missing_sources": manifest["missing_source_bindings"],
                      "missing_numeric_fields": manifest["missing_numeric_fields"]},
                     ensure_ascii=False, indent=2))
    return 0 if manifest["status"] == "READY_FOR_COMPARATOR" else 2


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
