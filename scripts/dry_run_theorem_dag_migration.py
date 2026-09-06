"""Run the proposal-only L0-L6 theorem-DAG migration audit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.dry_run_migrator import dry_run_migrate  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path,
                        default=ROOT / "artifacts/routeb_6dof/state.json")
    parser.add_argument("--proposal", type=Path,
                        default=ROOT / "artifacts/routeb_agent_entry_dag_mapping_20260906T110000Z/proposed_patch.json")
    parser.add_argument("--output", type=Path,
                        default=ROOT / "artifacts/theorem_dag_l0_l6_dry_run_20260906/report.json")
    args = parser.parse_args()
    report = dry_run_migrate(args.state, args.proposal)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = [
        "# L0-L6 theorem-DAG migration dry-run",
        "",
        "This is an independent, proposal-only audit artifact. It never saves workflow state or registry entries.",
        "",
        f"- safe_to_install: `{report['safe_to_install']}`",
        f"- state revision observed: `{report['input']['state_revision']}`",
        f"- state SHA-256: `{report['input']['state_sha256']}`",
        f"- proposed nodes: `{report['invariants']['proposed_node_count']}`",
        f"- checks passed: `{sum(c['status'] == 'pass' for c in report['checks'])}`",
        f"- checks failed: `{len(report['failures'])}`",
        "",
        "## Gate result",
        "",
        ("Installation is blocked by: " + ", ".join(f"`{x}`" for x in report['failures'])
         if report['failures'] else "All dry-run gates pass; an explicit later mutation step would still be required."),
        "",
        "The snapshot gate is fail-closed: a proposal prepared against another revision or byte hash is not rebased automatically.",
        "Parent closure remains blocked while proposed children are open; no proposed child is treated as verified evidence.",
    ]
    (args.output.parent / "REPORT.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(json.dumps({"safe_to_install": report["safe_to_install"],
                      "failures": report["failures"], "artifact": str(args.output)},
                     ensure_ascii=False))
    return 0 if report["safe_to_install"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
