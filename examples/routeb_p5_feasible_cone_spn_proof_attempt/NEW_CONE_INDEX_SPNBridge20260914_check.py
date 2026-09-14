"""Read-only typed source-bundle check, not a Lean admission receipt.

Uses the full generic P5 sidecar at the explicit sibling path, never the
homonymous proof-attempt module. No .olean, cache, log or receipt is written.
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
NEW = "NEW_CONE_INDEX_SPNBridge20260914"
GENERIC = "examples.routeb_p5_feasible_cone_spn_lean.P5FeasibleConeSPN"
MODULES = {
    "NEW_CONE_INDEX_Core": ("NEW_CONE_INDEX_Core.lean", "b0e154716a2ba71058b7996b8d85f982a12326ce117f8127cf9895286bd80602"),
    "NEW_CONE_INDEX_InverseCover20260908": ("NEW_CONE_INDEX_InverseCover20260908.lean", "2e4a6dfaca0d564e3fbf3407c6c68b31776c1fced30687d4c8e81e6b90d740c0"),
    "NEW_CONE_INDEX_SignedCoverConsumer": ("NEW_CONE_INDEX_SignedCoverConsumer.lean", "ea9a87281e096caf2e3b082a31dd0fbb00efc85016376dbd8ad735b39d41f4b8"),
    "NEW_CONE_INDEX_ConcreteConsumer20260908": ("NEW_CONE_INDEX_ConcreteConsumer20260908.lean", "5f50f2c68713a18d4b490573923315cb2f0a24cfafda3e281f7c1154c1d36205"),
    "NEW_CONE_INDEX_OrbitFiber20260914": ("NEW_CONE_INDEX_OrbitFiber20260914.lean", "4df14d1e6174b702dc9ed0d6d45c5021b9f786d0eb577b41347b404eec80ace9"),
    GENERIC: ("../routeb_p5_feasible_cone_spn_lean/P5FeasibleConeSPN.lean", "8a2206d22747bc7c24be65e2d87b31fc23f94e769525a62aabad97326e5385e7"),
    NEW: (NEW + ".lean", None),
}
AUDITS = ("p5_gap_even", "signed_gap_of_even", "eighteen_spn_envelope", "signed_gap_origin",
          "weighted_gap_factor", "weighted_gap_nonneg_iff", "envelope_iff_weighted_nonneg",
          "residual_power_of_envelope")


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
    raw = {path: (ROOT / path).read_bytes() for path, _ in MODULES.values()}
    raw[Path(__file__).name] = Path(__file__).read_bytes()
    before = {name: digest(value) for name, value in raw.items()}
    for path, pin in MODULES.values():
        need(pin is None or before[path] == pin, "source drift: " + path)
    imports, bodies, loaded = [], [], set()
    for module, (path, _) in MODULES.items():
        body = []
        for line in raw[path].decode("utf-8").splitlines():
            if line.startswith("import "):
                dependency = line.removeprefix("import ")
                if dependency in MODULES:
                    need(dependency in loaded, "dependency order mismatch")
                else:
                    need(dependency.startswith("Mathlib."), "unmapped import: " + dependency)
                    if line not in imports:
                        imports.append(line)
            else:
                body.append(line)
        bodies.append("\n".join(body))
        loaded.add(module)
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
    for name, axioms in reports:
        need({a.strip() for a in axioms.split(",") if a.strip()} <=
             {"propext", "Classical.choice", "Quot.sound"}, "unexpected axiom: " + name)
    reported = {name for name, _ in reports}
    need(all("RouteBP5ConeIndexSPNBridge." + name in reported for name in AUDITS),
         "missing child theorem audit")
    need(before == {name: digest((ROOT / name).read_bytes()) for name in raw}, "input changed")
    print(json.dumps(dict(result="pass", lean_exit_code=0, new_axiom_reports=len(AUDITS),
                         total_axiom_reports=len(reports), input_sha256=before,
                         source_bundle_sha256=digest(bundle.encode("utf-8")),
                         verification="Lean stdin source bundle",
                         standalone_module_imports_verified=False, admission_verified=False,
                         cached_mathlib_authenticated=False, concrete_K_path_bound=False,
                         source_coverage_verified=False, P5_closed=False, registry_eligible=False), indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps(dict(result="rejected_or_uncheckable", reason=str(exc))))
        sys.exit(1)
