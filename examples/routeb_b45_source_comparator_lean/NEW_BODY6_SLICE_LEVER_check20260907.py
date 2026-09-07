"""Read-only exact check of b0,b1,b2 local origins/axes and offset columns.

No v3/v4 tail check, body Fourier CSV, state/registry write, or Lean/Lake run.
The velocity check consumes c6=o5+(7/200)z5; it does not re-prove that endpoint.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

import sympy as sp

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    spec = importlib.util.spec_from_file_location("lever_dh_parser", HERE / "NEW_BODY6_SLICE_AXIS_check20260907.py")
    require(spec is not None and spec.loader is not None, "source parser")
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    source = {}
    for name, expected in helper.PINS.items():
        data = (ROOT / name).read_bytes()
        require(hashlib.sha256(data).hexdigest() == expected, "input drift: " + name)
        source[name] = data.decode("utf-8")
    dh = source["examples/routeb_real_dh_step_lean/RealDHStep.lean"]
    constants = source["examples/routeb_b45_fourier_normal_form/FourierNormalForm.lean"]
    ctcase, stcase = helper.cases(dh, "routeBRealCos"), helper.cases(dh, "routeBRealSin")
    cacase, sacase = helper.cases(constants, "routeBCosAlpha"), helper.cases(constants, "routeBSinAlpha")
    acase, dcase = helper.cases(constants, "routeBA"), helper.cases(constants, "routeBD")

    def rational(text):
        args = [int(part.strip()) for part in text.split("/")]
        return sp.Rational(*args)

    s, c = sp.symbols("s0:5"), sp.symbols("c0:5")
    circle = sp.groebner([s[k]**2+c[k]**2-1 for k in range(5)], *s, *c, domain=sp.QQ)

    def reduce(x):
        return circle.reduce(sp.expand(x))[1]

    T = sp.eye(4)
    origins, axes = [T[:3, 3]], []
    for k in range(5):
        axes.append(T[:3, 2])
        table = {"Real.cos q": c[k], "Real.sin q": s[k],
                 "-Real.cos q": -c[k], "-Real.sin q": -s[k]}
        ct, st = table[ctcase[k]], table[stcase[k]]
        ca, sa, a, d = int(cacase[k]), int(sacase[k]), rational(acase[k]), rational(dcase[k])
        A = sp.Matrix([[ct, -st*ca, st*sa, ct*a], [st, ct*ca, -ct*sa, st*a],
                       [0, sa, ca, d], [0, 0, 0, 1]])
        T = (T*A).applyfunc(sp.expand)
        origins.append(T[:3, 3])
    axis5 = T[:3, 2]
    cp, ss = c[1]*c[2]-s[1]*s[2], s[1]*c[2]+c[1]*s[2]
    h = sp.Rational(7, 200)
    reach = sp.Rational(21, 100)*s[1]+sp.Rational(19, 100)*ss
    height = sp.Rational(21, 100)*c[1]+sp.Rational(19, 100)*cp
    radial = sp.Rational(2, 25)+reach
    Y = sp.Matrix([[c[0], -s[0], 0], [s[0], c[0], 0], [0, 0, 1]])
    local_origins = [sp.zeros(3, 1), sp.Matrix([sp.Rational(2, 25), 0, sp.Rational(1, 10)]),
                     sp.Matrix([sp.Rational(2, 25)+sp.Rational(21, 100)*s[1], 0,
                                sp.Rational(1, 10)+sp.Rational(21, 100)*c[1]])]
    local_end = sp.Matrix([radial, sp.Rational(1, 20), sp.Rational(1, 10)+height])
    local_axes = [sp.Matrix([0, 0, 1]), sp.Matrix([0, 1, 0]), sp.Matrix([0, 1, 0])]
    local_axis5 = sp.Matrix([cp*c[3]*s[4]+ss*c[4], s[3]*s[4], -ss*c[3]*s[4]+cp*c[4]])
    local_b = [sp.Matrix([-sp.Rational(1, 20), radial, 0]), sp.Matrix([height, 0, -reach]),
               sp.Matrix([sp.Rational(19, 100)*cp, 0, -sp.Rational(19, 100)*ss])]
    origin_residuals = [sp.expand(x) for i in range(3) for x in origins[i]-Y*local_origins[i]]
    origin_residuals += [sp.expand(x) for x in origins[5]-Y*local_end]
    require(all(x == 0 for x in origin_residuals), "local parent/end origin mismatch")
    require(all(sp.expand(x) == 0 for i in range(3) for x in axes[i]-Y*local_axes[i]), "first axes")
    b = [axes[i].cross(origins[5]-origins[i]) for i in range(3)]
    b_residuals = [reduce(x) for i in range(3) for x in b[i]-Y*local_b[i]]
    require(all(x == 0 for x in b_residuals), "first-three lever mismatch")
    velocity_residuals = []
    for i in range(3):
        actual = b[i]+h*axes[i].cross(axis5)
        local = local_b[i]+h*local_axes[i].cross(local_axis5)
        velocity_residuals.extend(reduce(x) for x in actual-Y*local)
    require(all(x == 0 for x in velocity_residuals), "offset velocity interface")
    b0norm = reduce(b[0].dot(b[0])-(sp.Rational(1, 400)+radial**2))
    b2norm = reduce(b[2].dot(b[2])-sp.Rational(361, 10000))
    require(b0norm == b2norm == 0, "nonzero-lever norm check")
    files = sorted(HERE.glob("NEW_BODY6_SLICE_LEVER_*.lean"))
    require(len(files) == 2, "Lean inventory")
    for path in files:
        text = path.read_text(encoding="utf-8")
        require(not re.search(r"^\s*(axiom|opaque)\s|\bsorry\b|\badmit\b", text, re.M), "placeholder")
    source_text = (HERE / "NEW_BODY6_SLICE_LEVER_Source20260907.lean").read_text(encoding="utf-8")
    require("(hc : CenterOffsetTarget)" in source_text and "FirstThreeLeverTarget" in source_text,
            "typed source/center boundaries")
    print(json.dumps({
        "status": "FIRST_THREE_LEVER_SYMBOLIC_CHECK_PASSED_LEAN_NOT_RUN",
        "scope": "b0,b1,b2 and their explicit COM-offset vector interface only",
        "checks": {"parent_and_terminal_origin_residuals": list(map(str, origin_residuals)),
                   "lever_residuals": list(map(str, b_residuals)),
                   "offset_velocity_residuals": list(map(str, velocity_residuals)),
                   "b0_norm_residual": str(b0norm), "b2_norm_residual": str(b2norm),
                   "center_offset_consumed_not_reproved": True, "tail_rechecked": False,
                   "fourier_csv_read": False},
        "new_lean_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        "source_inputs_sha256": helper.PINS,
        "lean_lake_run": False, "source_levers_proven": False, "source_mass_coverage_proven": False,
        "registry_eligible": False, "registry_status": "pending", "formal_certificate_allowed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
