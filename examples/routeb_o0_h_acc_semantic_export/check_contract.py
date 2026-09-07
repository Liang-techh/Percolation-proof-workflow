"""Read-only design/provenance check. Never checks or admits an H_acc proof.

Exit 0 means the OPEN design is internally consistent and source/evidence
pins are current. Live state drift is reported separately because state is
an observation, not proof evidence. Exit 2 means malformed design or stale
source/evidence pins.
Future semantic-export receipts need a different, soundness-backed checker.
"""
from __future__ import annotations

import argparse
import copy
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import struct


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = Path(__file__).with_name("OPEN_CONTRACT.json")
SOURCE_SHA = "aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936"
STATUS = "OPEN_H_ACC_SOURCE_REFINEMENT_AND_INTERVAL_SOUNDNESS"
CHILDREN = {
    "C0": [], "C1": [], "C2": ["C0", "C1"], "C3": ["C2"],
    "C4": ["C3"], "C5": ["C4"], "H_acc_expr": ["C0", "C1", "C5"],
    "R0": ["C0"], "R1": ["C1", "R0"], "R2": ["R1"],
    "H_acc_round": ["H_acc_expr", "R2"],
}
ADMISSION_FIELDS = {
    "h_acc_expr_proven", "h_acc_round_proven", "source_binding_proven",
    "consumable_now", "registry_eligible", "registry_promoted",
    "formal_certificate_allowed", "baseline_consumed", "schur_margin_consumed",
    "main_state_modified", "o1_adapter_modified", "lean_lake_run", "julia_run",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def check_design(doc: dict) -> None:
    require(doc["schema"] == "routeb.o0.h_acc.obstruction_contract.v1", "schema")
    require(doc["status"] == STATUS, "OPEN verdict required")
    require(doc["artifact_role"] == "design_and_obstruction_only", "design role")
    require(doc["semantic_export_key"] is None, "no semantic export exists")
    require(set(doc["admission"]) == ADMISSION_FIELDS, "admission field coverage")
    require(all(v is False for v in doc["admission"].values()), "false promotion")
    require(doc["pins"]["deployed_source"]["sha256"] == SOURCE_SHA, "source hash")
    require(doc["pins"]["source_snapshot"]["sha256"] == SOURCE_SHA, "snapshot hash")
    require(doc["regularizer_in_target"] is False, "pre-regularizer boundary")
    require(doc["constant_policy"] == "source_decimal_rational_and_exact_pi", "literal policy")
    require(doc["input_policy"] == "decoded_finite_binary64_in_Q1000", "input quantifier")
    require(doc["domain"] == {"dimension": 6, "lower": "-1/1000", "upper": "1/1000"}, "domain")

    index = doc["index_contract"]
    coords = [[r, c] for c in range(1, 7) for r in range(1, 7)]
    require(index["matrix_coordinates"] == coords, "all 36 coordinates and order")
    require(index["matrix_order"] == "column_outer_row_inner", "matrix order")
    require(index["body_order"] == index["joint_order"] == list(range(1, 7)), "body/joint order")
    require(index["frame_order"] == list(range(7)), "frame order")
    require(index["active_joint_prefixes"] == [list(range(1, b + 1)) for b in range(1, 7)], "prefix columns")
    require([index[k] for k in ("final_root_count", "body_root_count", "accumulator_root_count")] == [36, 216, 216], "root coverage")
    require(index["zero_coordinates_may_be_omitted"] is False, "dense zeros required")
    require(index["runtime_symmetry_fill_allowed"] is False, "runtime triangles required")
    require(index["parent_axis_frame"] == "joint-1", "parent axis")
    require(index["com_frame_pair"] == ["body-1", "body"], "COM slots")
    require(index["observation_point"] == "after_line_58_body_6_before_line_60", "observation point")

    constants = doc["exact_constants"]
    for name in ("offset_pi_multiple", "d", "a", "alpha_pi_multiple", "mass", "I_val"):
        require(len(constants[name]) == 6, f"six constants: {name}")
        for value in constants[name]:
            require(str(Fraction(value)) == value, f"canonical rational: {value}")
    require(constants["inertia_divisor"] == "3" and constants["com_divisor"] == "2", "divisors")
    ex = doc["leaf_separation_example"]
    decoded = Fraction(struct.unpack(">d", bytes.fromhex(ex["binary64_bits"]))[0])
    require(decoded == Fraction(ex["decoded"]), "dyadic decoding")
    require(decoded - Fraction(ex["ideal"]) == Fraction(ex["difference"]) != 0, "literal separation")
    require(ex["julia_runtime_bits_observed"] is False, "no Julia observation")
    require(ex["full_mass_counterexample_claimed"] is False, "leaf-only diagnostic")

    evaluator = doc["evaluator"]
    require(evaluator["implemented"] is False and evaluator["source_refinement_proven"] is False, "no evaluator proof")
    require(evaluator["operations"] == {"input": 0, "rat": 0, "pi": 0, "neg": 1, "add": 2, "mul": 2, "div_nat": 1, "sin": 1, "cos": 1}, "operation arities")
    require(evaluator["unsimplified_rotated_inertia_required"] is True, "rotation factors")
    seen = set()
    for child in doc["children"]:
        name = child["id"]
        require(name in CHILDREN and name not in seen, "child identity")
        require(child["status"] == "OPEN", f"unproved child: {name}")
        require(child["depends_on"] == CHILDREN[name], f"dependencies: {name}")
        require(set(child["depends_on"]) <= seen, f"cycle/forward edge: {name}")
        require(bool(child["target"].strip()), f"empty target: {name}")
        seen.add(name)
    require(seen == set(CHILDREN), "child coverage")
    future = doc["future_receipt_contract"]
    require(future["structural_check_can_admit_theorem"] is False, "structural gate")
    require(future["round_receipt_can_discharge_exact_identity"] is False, "round/exact separation")
    required = {"SOURCE_SNAPSHOT/dhport_lib.jl", "exact_target_definition.json",
                "source_dag_manifest.json", "scalar_dag.json", "roots.json",
                "runtime_environment.json", "interval_receipt.json", "source_refinement_receipt.json"}
    paths = [item["path"] for item in doc["required_future_artifacts"]]
    require(len(paths) == len(required) and set(paths) == required, "future artifact coverage")


def check_pins(doc: dict) -> dict:
    results = {}
    for name, pin in doc["pins"].items():
        if name == "observed_state":
            continue
        path = Path(pin["path"])
        if not path.is_absolute():
            path = ROOT / path
        digest = sha256(path.read_bytes()).hexdigest()
        require(digest == pin["sha256"], f"stale or mismatched pin: {name}: {digest}")
        results[name] = digest
    prior = (ROOT / doc["pins"]["prior_h_acc_review"]["path"]).read_text(encoding="utf-8")
    require(doc["known_prior_source_hash_error"] in prior, "prior typo observation changed")
    state_bytes = (ROOT / doc["pins"]["observed_state"]["path"]).read_bytes()
    state = json.loads(state_bytes)
    obs = doc["state_observation"]
    parent = state["nodes"][obs["parent_id"]]
    metadata_nodes = [n for n in state["nodes"].values()
                      if '"h_acc_status"' in json.dumps(n.get("metadata", {}))]
    return {"evidence_pins_checked": len(results), "state_observation": {
        "recorded_revision": obs["revision"], "current_revision": state["revision"],
        "recorded_sha256": doc["pins"]["observed_state"]["sha256"],
        "current_sha256": sha256(state_bytes).hexdigest(),
        "observation_pin_matches": sha256(state_bytes).hexdigest() == doc["pins"]["observed_state"]["sha256"],
        "current_parent_status": parent["status"],
        "current_h_acc_metadata_nodes": len(metadata_nodes),
        "current_independent_h_acc_node_present": any("h_acc" in n["name"].lower() for n in state["nodes"].values()),
        "state_mutated_by_checker": False,
    }}


def self_test(doc: dict) -> int:
    mutations = [
        lambda d: d["index_contract"]["matrix_coordinates"].pop(),
        lambda d: d["index_contract"]["matrix_coordinates"].__setitem__(1, [1, 1]),
        lambda d: d["index_contract"]["body_order"].reverse(),
        lambda d: d["children"][0]["depends_on"].append("H_acc_expr"),
        lambda d: d["admission"].__setitem__("h_acc_expr_proven", True),
        lambda d: d["pins"]["deployed_source"].__setitem__("sha256", "0" * 64),
        lambda d: d["future_receipt_contract"].__setitem__("round_receipt_can_discharge_exact_identity", True),
    ]
    for mutate in mutations:
        candidate = copy.deepcopy(doc)
        mutate(candidate)
        try:
            check_design(candidate)
        except (ValueError, KeyError, TypeError):
            continue
        raise ValueError("negative fixture was accepted")
    return len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        doc = json.loads(CONTRACT.read_text(encoding="utf-8"))
        check_design(doc)
        pins = check_pins(doc)
        count = self_test(doc) if args.self_test else 0
        print(json.dumps({"design_check": "PASS_OPEN_DESIGN_ONLY", "status": STATUS,
                          **pins, "negative_fixtures_rejected": count,
                          "expected_output_roots": {"final": 36, "body": 216, "accumulator": 216},
                          "semantic_export_present": False, "formal_certificate_allowed": False,
                          "files_written": 0}, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"design_check": "REJECTED_OR_STALE", "status": STATUS,
                          "reason": str(exc), "formal_certificate_allowed": False}, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
