"""Record the conditional O0 baseline construction with exact arithmetic checks."""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "agent_review_inbox/receipt-T-P4-033-O0-exact-tuple-baseline-construction-obstruction-20260907.json"
STATE = ROOT / "artifacts/routeb_6dof/state.json"
sys.path.insert(0, str(ROOT / "src"))
from percolation_workflow.store import StateStore  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def q(value: str, field: str) -> Fraction:
    try:
        return Fraction(value)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{field} is not exact rational") from exc


def find(state, name: str):
    for node in state.nodes.values():
        if node.name == name:
            return node
    raise ValueError(f"missing node: {name}")


def main() -> int:
    if not RECEIPT.is_file() or not STATE.is_file():
        raise FileNotFoundError(RECEIPT if not RECEIPT.is_file() else STATE)
    doc = json.loads(RECEIPT.read_text(encoding="utf-8"))
    if doc.get("status") != "CONDITIONAL_RHO_AND_THETA_CONSTRUCTED_MR_BLOCKED":
        raise ValueError("unexpected O0 conditional construction status")
    if doc.get("schur_margin_consumed") is not False or doc.get("registry_promoted") is not False:
        raise ValueError("conditional construction cannot consume or promote")
    key = doc.get("canonical_key", {})
    if key.get("source_key") != "routeb-exact-fourier-mass:a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8|mu=1/1000000|contract=exp(i*nu*q)":
        raise ValueError("O0 source key drift")
    tuple_inputs = doc.get("tuple_inputs", {})
    Br, K, Cf = (q(tuple_inputs[name], name) for name in ("Br", "K", "Cf"))
    U = q(doc["constructed_baseline"]["unweighted_U_r"], "unweighted_U_r")
    rho = q(doc["constructed_baseline"]["weighted_rho_r"], "weighted_rho_r")
    if U != Br * K * Cf or rho != 10 * U:
        raise ValueError("O0 conditional exact arithmetic mismatch")
    if doc["constructed_theta"]["theta"] != "1" or doc["constructed_theta"]["lambda"] != "2":
        raise ValueError("O0 theta construction drift")
    m_r = q(doc["conditional_unit_margin_branch"]["m_r_unit"], "m_r_unit")
    m_f = q(doc["conditional_unit_margin_branch"]["strict_post_charge_leftover"], "strict_post_charge_leftover")
    if m_r <= 0 or m_f <= 0 or doc["conditional_unit_margin_branch"]["strict_post_charge_positive"] is not True:
        raise ValueError("O0 conditional margin is not strictly positive")
    text = RECEIPT.read_text(encoding="utf-8", errors="replace")
    if "NOT_CONSUMABLE_WITHOUT_ADDITIONAL_PREMISE" not in text or "L_base=1" not in text:
        raise ValueError("O0 conditional boundary missing")
    entry = {
        "status": doc["status"],
        "receipt_sha256": sha(RECEIPT),
        "source_key": key["source_key"],
        "state_key": key.get("state_key"),
        "unweighted_U_r": str(U),
        "weighted_rho_r": str(rho),
        "theta": "1",
        "lambda": "2",
        "conditional_baseline_premise": "normalized baseline budget L_base=1 with no other uncharged baseline term",
        "conditional_m_r": str(m_r),
        "conditional_m_f": str(m_f),
        "typed_map_and_exact_real_K_required": True,
        "physical_R_port_identity_required": True,
        "schur_margin_consumed": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    store = StateStore(STATE)
    state = store.load()
    node = find(state, "P4.true_dh_regularizer_semantics_bridge")
    prior = list(node.metadata.get("o0_conditional_baseline_constructions", []))
    changed = entry not in prior
    if changed:
        prior.append(entry)
        node.metadata["o0_conditional_baseline_constructions"] = prior
    desired = {
        "status": entry["status"],
        "receipt_sha256": entry["receipt_sha256"],
        "conditional_baseline_premise": entry["conditional_baseline_premise"],
        "conditional_m_r": entry["conditional_m_r"],
        "conditional_m_f": entry["conditional_m_f"],
        "schur_margin_consumed": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    if node.metadata.get("o0_conditional_baseline_construction") != desired:
        node.metadata["o0_conditional_baseline_construction"] = desired
        changed = True
    if changed:
        state.event(
            "routeb_o0_conditional_baseline_construction_recorded",
            node_id=node.id,
            status=entry["status"],
            strict_post_charge_positive=True,
            schur_margin_consumed=False,
            formal_certificate_allowed=False,
            registry_promoted=False,
        )
        state.validate()
        store.save(state)
    print({"status": "recorded" if changed else "already_recorded", "state_revision": store.load().revision, "conditional_m_f_positive": True, "schur_margin_consumed": False, "registry_promoted": False})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
