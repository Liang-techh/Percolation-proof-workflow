"""Read-only Route-B provenance audit; writes only a new receipt directory.

Historical source recovery never re-labels a historical output as a fresh run.
This is an engineering audit, not a theorem or an interval correctness proof.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib
import zipfile


HISTORICAL_SOURCE = "de7049d96eb253ec2a96dad74847677f488580214aec3a7b6d662262678d24ca"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def audit(root: Path, *, run_checker: bool = False) -> dict:
    root = root.resolve(strict=True)
    delivery = root / "robot_final"
    manifest = tomllib.loads((delivery / "routeB_certificate_manifest.toml").read_text(encoding="utf-8"))
    current_sources = {
        folder: digest((root / folder / "routeB_interval_bounds.jl").read_bytes())
        for folder in ("robot_final", "routeB_dense_Mq")
    }
    archive_path = root / "routeB_reform_handoff.zip"
    recovered = []
    # Only two small, explicitly named members are read. No archive extraction.
    with zipfile.ZipFile(archive_path) as archive:
        for folder in current_sources:
            member = f"{folder}/routeB_interval_bounds.jl"
            info = archive.getinfo(member)
            if info.file_size > 2_000_000:
                raise ValueError(f"unexpectedly large source member: {member}")
            sha = digest(archive.read(info))
            recovered.append({"archive": str(archive_path), "member": member,
                              "sha256": sha, "matches_historical_source": sha == HISTORICAL_SOURCE})
    historical_available = all(row["matches_historical_source"] for row in recovered)
    reports = []
    for folder in current_sources:
        for backup in sorted((root / folder).glob("*.backup_20260905_pre_provenance_sync")):
            report = Path(str(backup).removesuffix(".backup_20260905_pre_provenance_sync"))
            data = report.read_bytes()
            text = data.decode("utf-8")
            match = re.search(r"^- source_sha256: `([0-9a-f]{64})`", text, re.MULTILINE)
            source = match.group(1) if match else None
            reports.append({
                "path": report.relative_to(root).as_posix(), "sha256": digest(data),
                "source_sha256": source,
                "original_text_restored": report.read_text(encoding="utf-8") == backup.read_text(encoding="utf-8"),
                "original_bytes_restored": data == backup.read_bytes(),
                "historical_source_available": historical_available and source == HISTORICAL_SOURCE,
                "bound_to_current_source": source == current_sources[folder],
                "fresh_computation": False,
            })
    formal = json.loads((root / "robot_formal_v1/manifest.json").read_text(encoding="utf-8"))
    index_drift = []
    for row in formal.get("artifacts", []):
        path = (root / row["path"]).resolve()
        if not path.is_relative_to(root):
            raise ValueError("unsafe path in target artifact index")
        actual = digest(path.read_bytes()) if path.is_file() else None
        if actual != row.get("sha256"):
            index_drift.append({"path": row["path"], "recorded": row.get("sha256"), "actual": actual})
    issues = []
    if manifest.get("interval_candidate_sha256") != current_sources["robot_final"]:
        issues.append("current_delivery_source_does_not_match_historical_manifest")
    if current_sources["robot_final"] != current_sources["routeB_dense_Mq"]:
        issues.append("authoritative_and_delivery_interval_sources_differ")
    if index_drift:
        issues.append("target_artifact_index_is_stale")
    if not reports or not all(r["original_text_restored"] and r["historical_source_available"] for r in reports):
        issues.append("historical_report_recovery_incomplete")
    checker = None
    if run_checker:
        command = [sys.executable, str(delivery / "verify_all.py")]
        proc = subprocess.run(command, cwd=delivery, env={**os.environ, "PYTHONUTF8": "1"},
                              capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=120, check=False)
        checker = {"command": command, "cwd": str(delivery), "exit_code": proc.returncode,
                   "stdout": proc.stdout, "stderr": proc.stderr}
        if proc.returncode:
            issues.append("current_delivery_checker_failed")
    else:
        issues.append("current_delivery_checker_not_run")
    return {
        "schema": "routeb-provenance-correction-audit-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(), "target_root": str(root),
        "evidence_level": "engineering_audit_only", "registry_eligible": False,
        "audit_script_sha256": digest(Path(__file__).read_bytes()),
        "manifest_interval_source": manifest.get("interval_candidate_sha256"),
        "current_sources": current_sources, "historical_source_recovery": recovered,
        "historical_reports": reports, "target_index_drift": index_drift,
        "current_gate": formal.get("current_gate"), "checker": checker,
        "issues": issues, "current_baseline_complete": not issues,
        "historical_result_replay_performed": False,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True, help="New output directory; existing paths are refused")
    parser.add_argument("--run-checker", action="store_true")
    args = parser.parse_args()
    if args.out.resolve().is_relative_to(args.target_root.resolve()):
        parser.error("receipts must be outside the audited target tree")
    args.out.mkdir(parents=True, exist_ok=False)
    result = audit(args.target_root, run_checker=args.run_checker)
    (args.out / "receipt.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if result["checker"]:
        for stream in ("stdout", "stderr"):
            (args.out / f"checker.{stream}.log").write_text(result["checker"][stream], encoding="utf-8")
    print(json.dumps({"receipt": str((args.out / "receipt.json").resolve()),
                      "historical_reports": len(result["historical_reports"]),
                      "issues": result["issues"], "baseline_complete": result["current_baseline_complete"]},
                     ensure_ascii=False, indent=2))
    return 0 if result["current_baseline_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
