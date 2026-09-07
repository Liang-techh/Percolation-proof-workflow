"""Check the typed O1 regrouping interface without claiming its theorem."""
from __future__ import annotations

import json
from pathlib import Path
import re
from hashlib import sha256


ROOT = Path(__file__).resolve().parents[1]
INTERFACE = ROOT / "artifacts/task_routeb_o1_keyed_regrouping_20260907/RouteBO1KeyedRegroupingInterface.lean"
OUT = ROOT / "artifacts/task_routeb_o1_keyed_regrouping_20260907/interface_check.json"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    text = INTERFACE.read_text(encoding="utf-8")
    if re.search(r"\b(?:sorry|admit|axiom)\b", text):
        raise AssertionError("interface contains a forbidden proof shortcut")
    required = (
        "abbrev PayloadIndex := Fin 610",
        "abbrev TraceIndex := Fin 727",
        "abbrev BodyIndex := Fin 6",
        "abbrev MatrixIndex := Fin 6",
        "abbrev FrequencyIndex := Fin 6",
        "abbrev CoeffPair := ℚ × ℚ",
        "structure FourierKey where",
        "structure KeyedCoeffRow where",
        "def payloadCoeff",
        "def traceCoeff",
        "def traceCoeffBodySum",
        "def KeyedRegroupingTarget",
        "def FiniteSumOrientationTarget",
        "def PayloadToTraceTarget",
    )
    for token in required:
        if token not in text:
            raise AssertionError(f"keyed interface missing {token}")
    receipt = {
        "schema": "routeb.o1.keyed_regrouping.interface_check.v1",
        "status": "PASS_TYPED_KEYED_REGROUPING_INTERFACE_FAIL_CLOSED",
        "interface_sha256": digest(INTERFACE),
        "cardinalities": {"payload": 610, "trace": 727, "body": 6, "matrix": 6, "frequency": 6},
        "common_key_carrier_present": True,
        "finite_fold_targets_present": True,
        "forbidden_shortcuts_present": False,
        "lean_compiled": False,
        "keyed_regrouping_proven": False,
        "payload_trace_equality_proven": False,
        "formal_certificate_allowed": False,
        "registry_promoted": False,
    }
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(receipt)


if __name__ == "__main__":
    main()
