"""Fail-closed intake of new external Route-B artifact directories.

This is deliberately a catalog step, not theorem admission.  It watches the
external workspace for agent-produced ``task_*`` directories, records stable
file hashes and a coarse evidence class in the persistent event log, and
leaves theorem-node creation and registry promotion to an explicit review.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
ARTIFACT_ROOT = ROUTE_B / "artifacts"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore


TRACKED_NAMES = {
    "contract.json", "VERIFICATION.md", "RECEIPT.md", "README.md",
    "REPORT.md", "AUDIT.md", "PINNED_ENVIRONMENT.md", "OBLIGATIONS.csv",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def classify(text: str, has_contract: bool) -> str:
    upper = text.upper()
    if "LEAN_VERIFIED" in upper and ("EXIT CODE: 0" in upper or
                                      "EXIT CODE `0`" in upper or
                                      "COMPILE_STATUS" in upper):
        return "lean_verified_abstract_candidate"
    if "NOT RUN" in upper or "DESIGN ARTIFACT" in upper:
        return "pending_validation_design"
    if has_contract:
        return "contract_present_pending_review"
    return "unclassified_external_artifact"


def manifest_for(root: Path) -> dict:
    files = []
    for path in sorted(root.iterdir(), key=lambda item: item.name.lower()):
        if path.is_file() and path.name in TRACKED_NAMES:
            files.append({"name": path.name, "sha256": digest(path),
                          "bytes": path.stat().st_size})
    contract = None
    contract_path = root / "contract.json"
    if contract_path.is_file():
        try:
            value = json.loads(contract_path.read_text(encoding="utf-8"))
            if isinstance(value, dict):
                contract = {
                    "status": value.get("status"),
                    "artifact": value.get("artifact"),
                    "theorems": value.get("theorems"),
                    "formal_certificate_allowed": value.get(
                        "formal_certificate_allowed"),
                    "physical_certificate_allowed": value.get(
                        "physical_certificate_allowed"),
                }
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            contract = {"parse_error": True}
    text_parts = []
    for entry in files:
        if entry["name"].lower().endswith((".md", ".json", ".csv")):
            path = root / entry["name"]
            try:
                text_parts.append(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError):
                pass
    combined = "\n".join(text_parts)
    canonical = json.dumps(
        {"artifact": root.name, "files": files, "contract": contract},
        sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return {
        "artifact": root.name,
        "path": str(root.resolve()),
        "manifest_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest().upper(),
        "files": files,
        "contract": contract,
        "evidence_class": classify(combined, contract is not None),
        "admission_effect": "none",
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    }


def main() -> int:
    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    if not ARTIFACT_ROOT.is_dir():
        print({"status": "external_artifact_root_missing",
               "path": str(ARTIFACT_ROOT.resolve()),
               "state_revision": state.revision})
        return 0

    known = {
        event.get("artifact"): event.get("manifest_sha256")
        for event in state.events
        if event.get("kind") == "external_routeb_artifact_intake"
    }
    manifests = []
    changed = []
    for root in sorted(ARTIFACT_ROOT.glob("task_*"), key=lambda item: item.name):
        if not root.is_dir():
            continue
        manifest = manifest_for(root)
        manifests.append(manifest)
        if known.get(root.name) != manifest["manifest_sha256"]:
            state.event("external_routeb_artifact_intake", **manifest)
            changed.append(root.name)
    if changed:
        store.save(state)
    print({"status": "updated" if changed else "unchanged",
           "changed_artifacts": changed,
           "scanned_artifacts": len(manifests),
           "evidence_classes": {
               key: sum(item["evidence_class"] == key for item in manifests)
               for key in sorted({item["evidence_class"] for item in manifests})
           },
           "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
