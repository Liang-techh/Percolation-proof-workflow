"""Read-only Lean source-bundle check; no .olean, cache, receipt or registry writes.

Checks the actual core, generic consumer and typed adapter together through stdin.
This verifies elaboration/kernel proofs, NOT standalone module import resolution.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
FROZEN = {
    "P5FeasibleConeSPN.lean": "fa9d990cfb2adb6fce049b4c6feb9ab2dfed3c2bcd14b059a0a8332138e1e824",
    "NEW_exact_geometry_spn.py": "263fac727c1c3068043c02a63dade5995a22e1e7e9a879682ac3e69bafd54f42",
    "NEW_CONE_INDEX_Core.lean": "b0e154716a2ba71058b7996b8d85f982a12326ce117f8127cf9895286bd80602",
    "NEW_CONE_INDEX_SignedCoverConsumer.lean": "ea9a87281e096caf2e3b082a31dd0fbb00efc85016376dbd8ad735b39d41f4b8",
}
ADAPTER = "NEW_CONE_INDEX_ConcreteConsumer20260908.lean"
AUDITS = ("oriented_eq_expand", "concrete_signed_cover", "all_iff_signed",
          "all_iff_even_representatives", "orientedCoverWitnessEquiv",
          "member_flip_iff", "multiplicity_neg")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in (*FROZEN, ADAPTER)}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--mathlib-packages", type=Path, required=True)
    args = parser.parse_args()
    before = hashes()
    require(all(before[k] == v for k, v in FROZEN.items()), "input changed; re-audit required")
    dependencies = ("NEW_CONE_INDEX_Core", "NEW_CONE_INDEX_SignedCoverConsumer")
    imports, bodies = [], []
    for name in (*(d + ".lean" for d in dependencies), ADAPTER):
        body = []
        for line in (ROOT / name).read_text(encoding="utf-8").splitlines():
            if line.startswith("import "):
                module = line.removeprefix("import ")
                require(module in dependencies or module.startswith("Mathlib."), "unexpected import")
                if module not in dependencies and line not in imports:
                    imports.append(line)
            else:
                body.append(line)
        bodies.append("\n".join(body))
    bundle = "\n".join(imports) + "\n\n" + "\n\n".join(bodies) + "\n"
    paths = sorted(p / ".lake/build/lib/lean" for p in args.mathlib_packages.iterdir()
                   if (p / ".lake/build/lib/lean").is_dir())
    require(any((p / "Mathlib.olean").is_file() for p in paths), "no cached Mathlib")
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(map(str, paths)))
    result = subprocess.run([str(args.lean.resolve()), "--stdin"], input=bundle,
                            encoding="utf-8", capture_output=True, env=env, timeout=180)
    output = result.stdout + result.stderr
    print(output)
    require(result.returncode == 0, "Lean failed")
    require("sorryAx" not in output and "warning:" not in output, "axiom/warning audit failed")
    for name in AUDITS:
        require("RouteBP5ConeIndexConcreteConsumer." + name + "' depends on axioms:" in output,
                "missing axiom audit: " + name)
    require(before == hashes(), "input changed during verification")
    print(json.dumps(dict(result="pass", verification="Lean stdin source bundle",
                         standalone_module_imports_verified=False,
                         source_bundle_sha256=hashlib.sha256(bundle.encode()).hexdigest(),
                         input_sha256=before, concrete_K_path_bound=False,
                         P5_closed=False, registry_eligible=False), indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps(dict(result="rejected_or_uncheckable", reason=str(exc))))
        sys.exit(1)
