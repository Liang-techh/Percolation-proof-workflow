"""Read-only exact DH check for the small velocity-Gram leaves, not Fourier data.

Reuses only the previous checker's text parsers and pinned source identities;
does not call its main(), run Lean/Lake, or write artifacts/state/registry.
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
    spec = importlib.util.spec_from_file_location("vgram_source_parser", HERE / "NEW_BODY6_SLICE_AXIS_check20260907.py")
    require(spec is not None and spec.loader is not None, "parser loader")
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    source = {}
    for name, digest in helper.PINS.items():
        data = (ROOT / name).read_bytes()
        require(hashlib.sha256(data).hexdigest() == digest, "pinned source drift: " + name)
        source[name] = data.decode("utf-8")
    dh = source["examples/routeb_real_dh_step_lean/RealDHStep.lean"]
    constants = source["examples/routeb_b45_fourier_normal_form/FourierNormalForm.lean"]
    ct_cases, st_cases = helper.cases(dh, "routeBRealCos"), helper.cases(dh, "routeBRealSin")
    ca_cases, sa_cases = helper.cases(constants, "routeBCosAlpha"), helper.cases(constants, "routeBSinAlpha")
    a_cases, d_cases = helper.cases(constants, "routeBA"), helper.cases(constants, "routeBD")

    def rational(text):
        parts = text.split("/")
        return sp.Rational(int(parts[0]), int(parts[1])) if len(parts) == 2 else sp.Rational(int(parts[0]))

    s, c = sp.symbols("s0:6"), sp.symbols("c0:6")
    circle = sp.groebner([s[k]**2+c[k]**2-1 for k in range(6)], *s, *c, domain=sp.QQ)

    def reduce(poly):
        return circle.reduce(sp.expand(poly))[1]

    T = sp.eye(4)
    origins, axes = [T[:3, 3]], []
    for k in range(6):
        axes.append(T[:3, 2])
        trig = {"Real.cos q": c[k], "Real.sin q": s[k],
                "-Real.cos q": -c[k], "-Real.sin q": -s[k]}
        ct, st = trig[ct_cases[k]], trig[st_cases[k]]
        ca, sa = int(ca_cases[k]), int(sa_cases[k])
        a, d = rational(a_cases[k]), rational(d_cases[k])
        step = sp.Matrix([[ct, -st*ca, st*sa, ct*a], [st, ct*ca, -ct*sa, st*a],
                          [0, sa, ca, d], [0, 0, 0, 1]])
        T = (T*step).applyfunc(sp.expand)
        origins.append(T[:3, 3])
    h, mass, inertia = sp.Rational(7, 200), sp.Rational(3, 20), sp.Rational(1, 60)
    center = (origins[5]+origins[6])/2
    v = [axes[i].cross(center-origins[i]) for i in range(6)]
    center_residuals = [sp.expand(x) for x in center-origins[5]-h*axes[5]]
    require(all(x == 0 for x in center_residuals), "center offset")
    require(all(sp.expand(x) == 0 for x in origins[5]-origins[4]), "o5=o4")
    require(all(sp.expand(x) == 0 for x in origins[5]-origins[3]-sp.Rational(19, 100)*axes[3]), "o5-o3")
    residuals = []
    for i in range(6):
        split = axes[i].cross(origins[5]-origins[i])+h*axes[i].cross(axes[5])
        residuals.extend(sp.expand(x) for x in v[i]-split)
    require(all(x == 0 for x in residuals), "general velocity decomposition")
    for i in (3, 4):
        require(all(sp.expand(x) == 0 for x in v[i]-h*axes[i].cross(axes[5])), "tail velocity")
    require(all(sp.expand(x) == 0 for x in v[5]), "last geometric zero")
    # Only the small tail leaves are checked; no 5x5/36-entry Fourier comparison.
    v3, v4 = v[3].applyfunc(reduce), v[4].applyfunc(reduce)
    checks = {
        "velocity33": reduce(v3.dot(v3)-h**2*s[4]**2),
        "velocity44": reduce(v4.dot(v4)-h**2),
        "velocity34": reduce(v3.dot(v4)),
        "angular34": reduce(axes[3].dot(axes[4])),
        "mass33": reduce(mass*v3.dot(v3)+inertia*axes[3].dot(axes[3])
                         -(sp.Rational(1, 60)+sp.Rational(147, 800000)*s[4]**2)),
        "mass44": reduce(mass*v4.dot(v4)+inertia*axes[4].dot(axes[4])-sp.Rational(40441, 2400000)),
        "mass34": reduce(mass*v3.dot(v4)+inertia*axes[3].dot(axes[4])),
    }
    require(all(x == 0 for x in checks.values()), "tail Gram polynomial mismatch")
    files = sorted(HERE.glob("NEW_BODY6_SLICE_VGRAM_*.lean"))
    require(len(files) == 4, "Lean file inventory")
    for path in files:
        text = path.read_text(encoding="utf-8")
        require(not re.search(r"^\s*(axiom|opaque)\s|\bsorry\b|\badmit\b", text, re.M), "placeholder")
    text = (HERE / "NEW_BODY6_SLICE_VGRAM_Source20260907.lean").read_text(encoding="utf-8")
    require("def frontJoint (i : Fin 5) : Fin 6" in text and "(prevOrigin i)" in text,
            "front/parent index boundary")
    require("def FirstThreeLeverTarget" in text and "no_inactive_body6_joint_attempt" in text,
            "lever/active boundary")
    print(json.dumps({
        "status": "SMALL_DH_VELOCITY_GRAM_CHECK_PASSED_LEAN_NOT_RUN",
        "scope": "general cross decomposition and front-block indices 3,4 only; not full Fourier coverage",
        "checks": {"center_and_tail_origins_exact": True, "all_18_decomposition_residuals_zero": True,
                   "tail_residuals": {k: str(x) for k, x in checks.items()},
                   "velocity4_squared_norm": str(h**2), "first_three_zero_assumed": False,
                   "all_six_joints_active": True, "fourier_csv_read": False},
        "source_inputs_sha256": helper.PINS,
        "parser_sha256": hashlib.sha256((HERE / "NEW_BODY6_SLICE_AXIS_check20260907.py").read_bytes()).hexdigest(),
        "new_lean_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        "lean_lake_run": False, "source_gram_proven": False, "full_source_binding_proven": False,
        "source_coverage_proven": False, "registry_eligible": False,
        "registry_status": "pending", "formal_certificate_allowed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
