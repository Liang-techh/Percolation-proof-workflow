"""Read-only Lean stdin verification; no olean, cache, receipt or registry writes.

Imports of local sidecars are replaced by their complete, pinned source bodies
in dependency order. This is NOT a standalone import/Lake-build verification.
The old P5 proof attempt and Python geometry program are hashed, not executed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
NEW = "NEW_CONE_INDEX_OrbitFiber20260914.lean"
PINS = {
    "P5FeasibleConeSPN.lean": "fa9d990cfb2adb6fce049b4c6feb9ab2dfed3c2bcd14b059a0a8332138e1e824",
    "NEW_exact_geometry_spn.py": "263fac727c1c3068043c02a63dade5995a22e1e7e9a879682ac3e69bafd54f42",
    "NEW_CONE_INDEX_Core.lean": "b0e154716a2ba71058b7996b8d85f982a12326ce117f8127cf9895286bd80602",
    "NEW_CONE_INDEX_InverseCover20260908.lean": "2e4a6dfaca0d564e3fbf3407c6c68b31776c1fced30687d4c8e81e6b90d740c0",
    "NEW_CONE_INDEX_SignedCoverConsumer.lean": "ea9a87281e096caf2e3b082a31dd0fbb00efc85016376dbd8ad735b39d41f4b8",
    "NEW_CONE_INDEX_ConcreteConsumer20260908.lean": "5f50f2c68713a18d4b490573923315cb2f0a24cfafda3e281f7c1154c1d36205",
}
DEPENDENCIES = (
    "NEW_CONE_INDEX_Core", "NEW_CONE_INDEX_InverseCover20260908",
    "NEW_CONE_INDEX_SignedCoverConsumer", "NEW_CONE_INDEX_ConcreteConsumer20260908",
)
AUDITS = (
    "coordinates_neg", "opposite_member_iff_zero", "representative_injective_on_members",
    "orbit_member_iff", "unique_orientation", "coveringRepresentatives_nonempty",
    "multiplicity_eq_support_card", "origin_support_card", "exact_multiplicity_formula",
    "origin_orientation_erasure_loses_multiplicity",
)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--mathlib-packages", type=Path, required=True)
    args = parser.parse_args()
    names = (*PINS, NEW, Path(__file__).name)
    raw = {name: (ROOT / name).read_bytes() for name in names}
    before = {name: digest(value) for name, value in raw.items()}
    need(all(before[name] == pin for name, pin in PINS.items()), "input drift: re-audit required")
    imports, bodies, loaded = [], [], set()
    for name in (*(d + ".lean" for d in DEPENDENCIES), NEW):
        body = []
        for line in raw[name].decode("utf-8").splitlines():
            if line.startswith("import "):
                module = line.removeprefix("import ")
                if module in DEPENDENCIES:
                    need(module in loaded, "local dependency order mismatch")
                else:
                    need(module.startswith("Mathlib."), "unexpected import")
                    if line not in imports:
                        imports.append(line)
            else:
                body.append(line)
        bodies.append("\n".join(body))
        loaded.add(Path(name).stem)
    bundle = "\n".join(imports) + "\n\n" + "\n\n".join(bodies) + "\n"
    paths = sorted(p / ".lake/build/lib/lean" for p in args.mathlib_packages.resolve().iterdir()
                   if (p / ".lake/build/lib/lean").is_dir())
    need(any((p / "Mathlib.olean").is_file() for p in paths), "no cached Mathlib")
    result = subprocess.run([str(args.lean.resolve()), "--stdin"], input=bundle,
                            encoding="utf-8", capture_output=True, timeout=180,
                            env=dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, paths))))
    output = result.stdout + result.stderr
    print(output)
    need(result.returncode == 0, "Lean failed")
    need("sorryAx" not in output and "warning:" not in output, "sorry/warning audit failed")
    reports = re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", output)
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    for name, axioms in reports:
        need({a.strip() for a in axioms.split(",") if a.strip()} <= allowed,
             "unexpected axiom: " + name)
    reported = {name for name, _ in reports}
    need(all("RouteBP5ConeIndexOrbitFiber." + name in reported for name in AUDITS),
         "missing new declaration audit")
    need(before == {name: digest((ROOT / name).read_bytes()) for name in names},
         "input changed during verification")
    print(json.dumps(dict(result="pass", lean_exit_code=result.returncode,
                         verification="Lean stdin source bundle", new_axiom_reports=len(AUDITS),
                         total_axiom_reports=len(reports), input_sha256=before,
                         source_bundle_sha256=digest(bundle.encode("utf-8")),
                         standalone_module_imports_verified=False,
                         cached_mathlib_authenticated=False, concrete_K_path_bound=False,
                         P5_closed=False, registry_eligible=False), indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps(dict(result="rejected_or_uncheckable", reason=str(exc))))
        sys.exit(1)
