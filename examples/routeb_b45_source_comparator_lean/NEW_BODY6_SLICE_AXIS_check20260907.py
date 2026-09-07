"""Read-only symbolic DH-axis check. No CSV, state, registry, Lean or Lake access.

Checks the mathematical formulas using exact polynomial algebra, separately
from the uncompiled Lean tactics. Only sine/cosine unit-circle identities are
used to reduce dot products; all 18 coordinate bindings are polynomial equalities.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PINS = {
    "examples/routeb_real_dh_step_lean/RealDHStep.lean":
        "9c04da5b9627ee749c53009733006934f95b2d33265e46ca59d0725aa453786a",
    "examples/routeb_b45_fourier_normal_form/FourierNormalForm.lean":
        "56ec2f2d29a22942bcb83a3ba98197ae1ce4d607340072b81c013b8d358d3218",
    "examples/routeb_frame_slot_accessor_lean/FrameSlotAccessor.lean":
        "f497bd1f45fae4dd385f4d0f46df79252c92e5cd027b29d5dc55011f91525c31",
    "examples/routeb_source_contract_adapter_lean/SourceContractAdapter.lean":
        "58c0b15b6fceb1064f773acdb9f684dc55a021ac69a030c13e1c8b46f7b9a8dc",
    "examples/routeb_concrete_step_homogeneous_lean/ConcreteStepHomogeneous.lean":
        "5da25ba14626338bb82e63b13f2abd4caa4f5bf84d1f5b23ec38731682307499",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def definition(text, name):
    block = text.split("def " + name, 1)[1]
    return re.split(r"\n(?:def|theorem|#print) ", block, maxsplit=1)[0]


def cases(text, name):
    return {int(k): v.strip() for k, v in
            re.findall(r"\|\s*(\d+)\s*=>\s*([^\r\n]+)", definition(text, name))}


def main():
    source = {}
    for path, digest in PINS.items():
        data = (ROOT / path).read_bytes()
        require(hashlib.sha256(data).hexdigest() == digest, "source drift: " + path)
        source[path] = data.decode("utf-8")
    dh = source["examples/routeb_real_dh_step_lean/RealDHStep.lean"]
    constants = source["examples/routeb_b45_fourier_normal_form/FourierNormalForm.lean"]
    # Confirm the parsed actual upper-left DH block before constructing matrices.
    block = {(int(i), int(j)): re.sub(r"\s+", "", v) for i, j, v in
             re.findall(r"\|\s*(\d+),\s*(\d+)\s*=>\s*([^\r\n]+)", definition(dh, "realDHStep"))}
    expected_block = [["ct", "-st*ca", "st*sa"], ["st", "ct*ca", "-ct*sa"], ["0", "sa", "ca"]]
    require(all(block[i, j] == expected_block[i][j] for i in range(3) for j in range(3)),
            "DH rotation block mismatch")
    cos_case, sin_case = cases(dh, "routeBRealCos"), cases(dh, "routeBRealSin")
    ca_case, sa_case = cases(constants, "routeBCosAlpha"), cases(constants, "routeBSinAlpha")
    s = sp.symbols("s0:6")
    c = sp.symbols("c0:6")
    prefix = sp.eye(3)
    axes = []
    for k in range(6):
        # The axis is captured BEFORE the current step. Includes slot 0 identity.
        axes.append(prefix[:, 2])
        allowed = {"Real.cos q": c[k], "Real.sin q": s[k],
                   "-Real.cos q": -c[k], "-Real.sin q": -s[k]}
        ct, st = allowed[cos_case[k]], allowed[sin_case[k]]
        ca, sa = int(ca_case[k]), int(sa_case[k])
        step = sp.Matrix([[ct, -st*ca, st*sa], [st, ct*ca, -ct*sa], [0, sa, ca]])
        prefix = (prefix * step).applyfunc(sp.expand)
    cp, ss = c[1]*c[2]-s[1]*s[2], s[1]*c[2]+c[1]*s[2]
    yaw = sp.Matrix([[c[0], -s[0], 0], [s[0], c[0], 0], [0, 0, 1]])
    pitch = sp.Matrix([[cp, 0, ss], [0, 1, 0], [-ss, 0, cp]])
    local = [sp.Matrix([0, 0, 1]), pitch*sp.Matrix([0, 1, 0]), pitch*sp.Matrix([0, 1, 0]),
             pitch*sp.Matrix([0, 0, 1]), pitch*sp.Matrix([-s[3], c[3], 0]),
             pitch*sp.Matrix([c[3]*s[4], s[3]*s[4], c[4]])]
    coordinate_residuals = [sp.expand((axes[i]-yaw*local[i])[a])
                            for i in range(6) for a in range(3)]
    require(all(x == 0 for x in coordinate_residuals), "parent-axis coordinate mismatch")
    values = [cp*c[4]-ss*c[3]*s[4], s[3]*s[4], s[3]*s[4], c[4], sp.Integer(0), sp.Integer(1)]
    # q6 is absent: axes[5] was captured before its step. Only q0..q4 identities needed.
    variables = (*s[:5], *c[:5])
    circle = sp.groebner([s[k]**2+c[k]**2-1 for k in range(5)], *variables, domain=sp.QQ)
    dot_residuals = [circle.reduce(sp.expand(axes[i].dot(axes[5])-values[i]))[1] for i in range(6)]
    require(all(x == 0 for x in dot_residuals), "source-axis dot mismatch")
    require(all(not (s[5] in x.free_symbols or c[5] in x.free_symbols)
                for a in axes for x in a), "used post-step axis")
    lean_files = sorted(HERE.glob("NEW_BODY6_SLICE_AXIS_*.lean"))
    require(len(lean_files) == 3, "new Lean file inventory")
    for path in lean_files:
        text = path.read_text(encoding="utf-8")
        require(not re.search(r"^\s*(axiom|opaque)\s|\bsorry\b|\badmit\b", text, re.M), "placeholder")
    geometry = (HERE / "NEW_BODY6_SLICE_AXIS_Geometry20260907.lean").read_text(encoding="utf-8")
    require(re.findall(r"^import (.+)$", geometry, re.M) ==
            ["NEW_BODY6_SLICE_AXIS_Core20260907", "FrameSlotHomogeneousPrefixV2", "SourceContractAdapter"],
            "geometry import boundary")
    consumer = (HERE / "NEW_BODY6_SLICE_AXIS_Consumer20260907.lean").read_text(encoding="utf-8")
    require("(hall : AllEntriesGramFourierTarget) (hzero : EmptyFourierTarget)" in consumer,
            "full-matrix boundary")
    print(json.dumps({
        "status": "EXACT_DH_AXIS_POLYNOMIAL_CHECK_PASSED_LEAN_NOT_RUN",
        "sympy_version": sp.__version__,
        "checks": {"parent_axis_coordinate_residuals": [str(x) for x in coordinate_residuals],
                   "six_dot_residuals_mod_unit_circles": [str(x) for x in dot_residuals],
                   "phase_offsets_read_from_source": True, "q6_absent": True,
                   "fourier_csv_read": False, "geometry_import_boundary": True},
        "input_sha256": PINS,
        "new_lean_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in lean_files},
        "lean_lake_run": False, "source_axis_dot_proven": False,
        "source_binding_proven": False, "source_coverage_proven": False,
        "registry_eligible": False, "registry_status": "pending", "formal_certificate_allowed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
