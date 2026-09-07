"""Admit a same-key exact-Fourier O0 tuple as a conditional one-cell child."""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "agent_review_inbox/receipt-T-P4-033-O0-constructive-exact-fourier-cell-K-Br-Cf-20260907.json"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
ROUTE = ROOT.parent / "6dof_sos_optimized" / "6dof_sos_optimized"
SOURCE_PATHS = {
    "mass_fourier_csv": ROUTE / "routeB_dense_Mq/routeB_fourier_mass_full_rational.csv",
    "source_numbers_receipt": ROOT / "artifacts/routeb_agent_schur_fullq_next_20260906T091446Z/NUMBERS.json",
    "source_audit": ROOT / "artifacts/routeb_agent_schur_fullq_next_20260906T091446Z/AUDIT.md",
}
EXPECTED_HASHES = {
    "mass_fourier_csv": "A986A208B62F585C6CA1B9C81B958710D2043E5BF786DDC930A6FA29F7A232B8",
    "source_numbers_receipt": "59C7E9BECA460DAB46B675F056BB3BAC147001A3FF1888EBC2CE0110611F7F3E",
    "source_audit": "D24452D179CCF0275C096246A906CC8300159A4285CF8D7E825769C3CBEEF281",
}
sys.path.insert(0, str(ROOT / "src"))

from percolation_workflow.store import StateStore  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def ref(path: Path) -> dict[str, str]:
    return {"path": str(path.resolve()), "sha256": sha(path)}


def frac(value: str) -> Fraction:
    return Fraction(value)


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    for path in (RECEIPT, STATE, *SOURCE_PATHS.values()):
        if not path.is_file():
            raise FileNotFoundError(path)
    payload = json.loads(RECEIPT.read_text(encoding="utf-8"))
    for key, expected in {
        "schema": "routeb-o0-constructive-exact-fourier-cell-tuple-v1",
        "task": "T-P4-033",
        "status": "CONDITIONAL_EXACT_RATIONAL_TUPLE_CONSTRUCTED",
    }.items():
        if payload.get(key) != expected:
            raise ValueError(f"O0 constructive receipt field {key!r} mismatch")
    admission = payload.get("admission", {})
    if admission.get("exact_fourier_cell_child_consumable") is not True:
        raise ValueError("receipt does not admit its declared one-cell child")
    for key in ("formal_certificate_allowed", "registry_eligible", "ledger_consumed", "schur_margin_consumed"):
        if admission.get(key) is not False:
            raise ValueError(f"receipt is not fail-closed at {key}")
    orientation = payload.get("orientation_and_norm", {})
    if orientation.get("norm") != "induced_infinity":
        raise ValueError("unexpected O0 norm")
    if orientation.get("B_one_based") != [4, 5] or orientation.get("D_one_based") != [1, 2, 3, 6]:
        raise ValueError("unexpected O0 block orientation")
    source_key = payload.get("source_key")
    state_key = payload.get("state_key")
    if not source_key or not state_key or "norm=induced_infinity" not in state_key:
        raise ValueError("missing same-key O0 source/state contract")
    exact = payload["exact_tuple"]
    K = frac(exact["K"]["value"])
    Br = frac(exact["Br"]["value"])
    Cf = frac(exact["Cf"]["value"])
    X = frac(exact["K"]["construction"]["X_norm"])
    rho = frac(exact["K"]["construction"]["neumann_rho"])
    if not (K > 0 and Br > 0 and Cf > 0 and rho < 1 and K == X / (1 - rho)):
        raise ValueError("O0 K/Br/Cf tuple or Neumann construction failed exact arithmetic")
    br_construction = exact["Br"]["construction"]
    if Br != frac(br_construction["MBD_q0_norm"]) + frac(br_construction["DeltaMBD_norm"]):
        raise ValueError("O0 Br construction failed exact arithmetic")
    perturb = payload["regularizer_perturbation_check"]
    delta = frac(perturb["delta"])
    epsilon = Br * Cf * delta * K * K / (1 - delta * K)
    if not (delta * K < 1 and epsilon == frac(perturb["epsilon_R_unweighted"])):
        raise ValueError("O0 epsilon_R construction failed exact arithmetic")
    hashes = {name: sha(path) for name, path in SOURCE_PATHS.items()}
    if hashes != EXPECTED_HASHES:
        raise ValueError("O0 exact tuple source hash drifted")

    entry = {
        "schema_version": 1,
        "task_id": payload["task"],
        "source_agent": "codex-inbox",
        "review_status": payload["status"],
        "receipt_artifact": ref(RECEIPT),
        "source_key": source_key,
        "state_key": state_key,
        "norm": orientation["norm"],
        "block_orientation": {"B": [4, 5], "D": [1, 2, 3, 6]},
        "K": str(K),
        "Br": str(Br),
        "Cf": str(Cf),
        "delta": str(delta),
        "epsilon_R": str(epsilon),
        "source_artifacts": {name: ref(path) for name, path in SOURCE_PATHS.items()},
        "cell_scope": payload["consumer_scope"],
        "deployed_float64_q_nonzero_binding": False,
        "global_cell_coverage": False,
        "weighted_metric_conversion": False,
        "schur_margin_consumed": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
        "admission_status": "conditional_exact_fourier_cell_child",
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_regularizer_semantics_bridge")
    prior = list(node.metadata.get("o0_exact_fourier_cell_tuples", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["o0_exact_fourier_cell_tuples"] = prior
    desired = {
        "status": payload["status"],
        "source_key": source_key,
        "state_key": state_key,
        "norm": orientation["norm"],
        "K": str(K),
        "Br": str(Br),
        "Cf": str(Cf),
        "epsilon_R": str(epsilon),
        "cell_scope": payload["consumer_scope"],
        "global_coverage": False,
        "weighted_metric_conversion": False,
        "schur_margin_consumed": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o0_constructive_exact_tuple") != desired:
        node.metadata["o0_constructive_exact_tuple"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o0_constructive_exact_fourier_tuple_recorded",
            node_id=node.id,
            source_key=source_key,
            state_key=state_key,
            child_scope=payload["consumer_scope"],
            exact_rational_K=True,
            exact_rational_Br=True,
            exact_rational_Cf=True,
            global_coverage=False,
            registry_promoted=False,
            formal_certificate_allowed=False,
        )
        state.validate()
        store.save(state)
    print({
        "status": "recorded" if changed else "already_recorded",
        "review_status": payload["status"],
        "state_revision": store.load().revision,
        "K": str(K),
        "Br": str(Br),
        "Cf": str(Cf),
        "epsilon_R": str(epsilon),
        "registry_promoted": False,
        "formal_certificate_allowed": False,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
