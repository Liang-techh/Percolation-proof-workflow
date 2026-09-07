"""Record the resolved-cell Frobenius port bound as a fail-closed P4 leaf.

The upstream ledger is a rigorous-numerical candidate, not a Lean theorem.
This importer checks its finite-cell accounting and exact rational budget
reduction, then records provenance without changing registry or admission.
"""
from __future__ import annotations

import csv
import hashlib
from collections import Counter
from fractions import Fraction
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ROUTE_B = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
SRC = ROUTE_B / "routeB_dense_Mq"
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest().upper()}


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def q(text: str) -> Fraction:
    return Fraction(text.replace("//", "/"))


def before_summary(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if "#SUMMARY" not in lines:
        raise ValueError("port partition has no summary boundary")
    rows = list(csv.DictReader(lines[:lines.index("#SUMMARY")]))
    if len(rows) != 5120 or {row.get("status") for row in rows} != {"RESOLVED"}:
        raise ValueError("port partition is not 5120 resolved cells")
    return rows


def main() -> int:
    partition = SRC / "routeB_compact_port_bi_partition_probe_left_frobenius_output.csv"
    cover = SRC / "routeB_compact_qbox_cover_depth3.csv"
    ledger = SRC / "routeB_compact_port_frobenius_ledger.csv"
    report = SRC / "P5_COMPACT_PORT_FROBENIUS_LEDGER.md"
    generator = SRC / "routeB_compact_port_frobenius_ledger.py"
    for path in (partition, cover, ledger, report, generator):
        if not path.is_file():
            raise FileNotFoundError(path)

    rows = before_summary(partition)
    footer = partition.read_text(encoding="utf-8").split("#SUMMARY", 1)[1]
    source_match = re.search(r"^source_sha256,([0-9a-f]{64})$", footer, re.MULTILINE)
    cover_match = re.search(r"^cover_sha256,([0-9a-f]{64})$", footer, re.MULTILINE)
    if source_match is None or cover_match is None:
        raise ValueError("partition provenance footer is malformed")
    if hashlib.sha256(cover.read_bytes()).hexdigest() != cover_match.group(1):
        raise ValueError("declared cover hash does not match coverage artifact")
    cover_rows = list(csv.DictReader(cover.open(newline="", encoding="utf-8")))
    cover_counts = Counter((row.get("eta"), row.get("status")) for row in cover_rows)
    if cover_counts != Counter({("2.7", "INTERSECTS"): 2560,
                                ("5.6", "INTERSECTS"): 2560,
                                ("2.7", "OUTSIDE"): 1536,
                                ("5.6", "OUTSIDE"): 1536}):
        raise ValueError("q-box cover has unexpected eta/status accounting")
    by_eta = {eta: [row for row in rows if row["eta"] == eta]
              for eta in {row["eta"] for row in rows}}
    if set(by_eta) != {"2.7", "5.6"} or any(len(cell_rows) != 2560
                                              for cell_rows in by_eta.values()):
        raise ValueError("unexpected eta/cell partition")

    ledger_rows = list(csv.DictReader(ledger.open(newline="", encoding="utf-8")))
    expected = {
        "2.7": ("4227/500000", "15773/100000", "True", "True"),
        "5.6": ("34547/1000000", "5453/200000", "True", "True"),
    }
    metrics: dict[str, dict[str, str]] = {}
    for eta, (rho, margin, admissible, spd) in expected.items():
        matches = [row for row in ledger_rows
                   if row.get("eta") == eta and row.get("theta") == "1/4"]
        if len(matches) != 1:
            raise ValueError(f"missing unique ledger row for eta={eta}")
        row = matches[0]
        if (row.get("rho2_frobenius") != rho or row.get("margin") != margin or
                row.get("admissible") != admissible or row.get("implicit_HG_spd") != spd or
                q(row["margin"]) <= 0):
            raise ValueError(f"ledger budget mismatch for eta={eta}")
        metrics[eta] = {key: row[key] for key in
                        ("resolved_boxes", "rho2_frobenius", "rho2_induced",
                         "theta", "lambda", "charge", "margin",
                         "admissible", "implicit_HG_spd")}

    store = StateStore(ROOT / "artifacts/routeb_6dof/state.json")
    state = store.load()
    parent = find(state, "P4.residual_schur_pmi")
    name = "P4.residual_port_frobenius_bound"
    source_artifacts = [ref(path) for path in (partition, cover, ledger, report, generator)]
    metadata = {
        "verification_domain": "external-research",
        "research_stage": "P4",
        "statement_status": "resolved_cells_conditional_port_budget_candidate",
        "claim_status": "port_bound_candidate_open",
        "evidence_level": "rigorous-numerical-cellwise-candidate",
        "registry_eligible": False,
        "comparator_accepted": False,
        "formal_certificate_allowed": False,
        "physical_certificate_allowed": False,
        "source_artifacts": source_artifacts,
        "partition_contract": {
            "cell_count": 5120,
            "eta_values": ["2.7", "5.6"],
            "cells_per_eta": 2560,
            "status": "RESOLVED",
            "weighted_metric_scaling": "left_output",
            "declared_source_sha256": source_match.group(1),
            "declared_cover_sha256": cover_match.group(1),
        },
        "exact_budget_rows": metrics,
        "unresolved": [
            "independent_interval_source_replay",
            "true_dh_and_float64_semantic_binding",
            "coefficient_level_residual_absorption",
            "full_domain_and_flowpipe_coverage",
            "strict_gram_and_lean_statement_comparator",
        ],
    }
    existing = next((node for node in state.nodes.values() if node.name == name), None)
    if existing is None:
        node_id = state.add_node(
            name,
            "On the declared resolved-cell partition, the normalized port map "
            "has the recorded Frobenius squared bound and positive Young margin "
            "for eta 2.7 and 5.6.",
            parent_id=parent.id,
            proof_sketch=(
                "Replay the 5120-cell outward interval contract, reduce the "
                "Frobenius square bound to exact rational Young charges, and "
                "keep source semantics, residual PMI, coverage, and flowpipe "
                "as independent premises."),
            metadata=metadata,
        )
        state.event("routeb_port_frobenius_bound_recorded", node_id=node_id,
                    parent_id=parent.id, source_artifacts=source_artifacts,
                    exact_budget_rows=metrics, registry_promoted=False,
                    formal_certificate_allowed=False)
        store.save(state)
        print({"status": "recorded", "node_id": node_id,
               "state_revision": state.revision})
        return 0

    changed = False
    for key, value in metadata.items():
        if existing.metadata.get(key) != value:
            existing.metadata[key] = value
            changed = True
    if existing.parent_id != parent.id:
        existing.parent_id = parent.id
        changed = True
    if changed:
        state.event("routeb_port_frobenius_bound_refresh", node_id=existing.id,
                    parent_id=parent.id, source_artifacts=source_artifacts,
                    exact_budget_rows=metrics, registry_promoted=False,
                    formal_certificate_allowed=False)
        store.save(state)
        print({"status": "refreshed", "node_id": existing.id,
               "state_revision": state.revision})
    else:
        print({"status": "already_recorded", "node_id": existing.id,
               "state_revision": state.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
