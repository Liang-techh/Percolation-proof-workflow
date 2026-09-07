"""Read-only Lean source-bundle verifier; no .olean, cache, receipt or registry writes.

This checks actual declarations together, not independently built module imports.
The explicit map avoids the two different P5FeasibleConeSPN.lean files colliding.
Only standard library; run with python -B. All evidence is printed to stdout.
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

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
DEPENDENCIES = {
    "NEW_CONE_INDEX_Core": (
        HERE / "NEW_CONE_INDEX_Core.lean",
        "b0e154716a2ba71058b7996b8d85f982a12326ce117f8127cf9895286bd80602",
    ),
    "P5FeasibleConeSPN": (
        ROOT / "examples/routeb_p5_feasible_cone_spn_lean/P5FeasibleConeSPN.lean",
        "8a2206d22747bc7c24be65e2d87b31fc23f94e769525a62aabad97326e5385e7",
    ),
    "P5PiecewiseTransport": (
        ROOT / "examples/routeb_p5_piecewise_transport_lean/P5PiecewiseTransport.lean",
        "c445e4110584c5c536f023ad08b2a8c5eccef21fc9b97aa363f24e0a9ae95208",
    ),
}
AUDITED = [
    "row_mono", "envelope_mono", "component_le_iff_rows", "ComponentBinding.zero_at_origin",
    "ComponentBinding.weaken", "transportedGain",
    "PathBinding.toComponentBinding", "liftSPN", "direct_envelope",
    "componentwise_spn_power", "pointwise_ledger", "cone_gap_antitone",
]
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def bundle() -> tuple[str, dict[str, str]]:
    imports: list[str] = []
    bodies: list[str] = []
    hashes: dict[str, str] = {}
    for name, (path, expected) in DEPENDENCIES.items():
        data = path.read_bytes()
        if digest(data) != expected:
            raise ValueError(f"frozen dependency changed: {path.relative_to(ROOT)}")
        hashes[str(path.relative_to(ROOT))] = digest(data)
        lines = []
        for line in data.decode("utf-8-sig").splitlines():
            if line.startswith("import "):
                if not line.startswith("import Mathlib."):
                    raise ValueError(f"unexpected dependency import: {line}")
                if line not in imports:
                    imports.append(line)
            else:
                lines.append(line)
        bodies.append(f"-- BEGIN frozen {name}\n" + "\n".join(lines))
    core = HERE / "NEW_KPATH_INTERFACE_Core.lean"
    data = core.read_bytes()
    hashes[str(core.relative_to(ROOT))] = digest(data)
    lines = data.decode("utf-8-sig").splitlines()
    core_imports = [line[7:] for line in lines if line.startswith("import ")]
    if core_imports != list(DEPENDENCIES):
        raise ValueError("unexpected Core import map/order")
    bodies.append("-- BEGIN new interface\n" + "\n".join(
        line for line in lines if not line.startswith("import ")
    ))
    return "\n".join(imports) + "\n\n" + "\n\n".join(bodies) + "\n", hashes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, default=(
        Path.home() / ".elan/toolchains/leanprover--lean4---v4.32.0/bin/lean.exe"
    ))
    parser.add_argument("--emit-source", action="store_true",
                        help="print the exact assembled source without running Lean")
    args = parser.parse_args()
    source, hashes = bundle()
    if args.emit_source:
        print(source)
        return 0
    packages = ROOT / "examples/local_fkg/.lake/packages"
    paths = sorted(p / ".lake/build/lib/lean" for p in packages.iterdir()
                   if (p / ".lake/build/lib/lean").is_dir())
    if not paths or not args.lean.is_file():
        raise ValueError("Lean executable or existing Mathlib cache unavailable")
    env = os.environ.copy()
    env["LEAN_PATH"] = os.pathsep.join(map(str, paths))
    version = subprocess.run([str(args.lean), "--version"], capture_output=True,
                             text=True, encoding="utf-8", check=True).stdout.strip()
    if "version 4.32.0" not in version:
        raise ValueError(f"unexpected toolchain: {version}")
    result = subprocess.run([str(args.lean), "--stdin"], input=source,
                            capture_output=True, text=True, encoding="utf-8",
                            env=env, cwd=ROOT, timeout=180)
    output = result.stdout + result.stderr
    print(output, end="" if output.endswith("\n") else "\n")
    if result.returncode or "sorryAx" in output or re.search(r"\b(error|warning):", output):
        raise ValueError(f"Lean source-bundle check failed (exit {result.returncode})")
    audits = {}
    for name in AUDITED:
        full_name = "RouteBP5KPathInterface." + name
        match = re.search(re.escape("'" + full_name + "' depends on axioms:")
                          + r"\s*\[([^\]]*)\]", output)
        if match is None:
            raise ValueError(f"missing axiom audit: {full_name}")
        axioms = {item.strip() for item in match.group(1).split(",") if item.strip()}
        if not axioms <= ALLOWED_AXIOMS:
            raise ValueError(f"unexpected axioms: {full_name}: {axioms}")
        audits[name] = sorted(axioms)
    # Detect concurrent input edits; no stale-input success report.
    current_source, current_hashes = bundle()
    if current_source != source or current_hashes != hashes:
        raise ValueError("inputs changed during verification")
    print(json.dumps({
        "status": "conditional_interface_source_bundle_checked",
        "toolchain": version,
        "lean_exit_code": result.returncode,
        "source_bundle_sha256": digest(source.encode("utf-8")),
        "inputs_sha256": hashes,
        "axioms": audits,
        "module_import_build_verified": False,
        "concrete_K_path_bound": False,
        "concrete_H_gap_instantiated": False,
        "concrete_spn_certificates_supplied": False,
        "source_coverage_verified": False,
        "registry_eligible": False,
        "P5_P8_M4_closed": False,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "rejected_or_uncheckable", "reason": str(exc),
                          "registry_eligible": False}, ensure_ascii=False))
        sys.exit(1)
