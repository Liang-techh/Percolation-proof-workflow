"""Exact 36-entry Route-B DH-to-Fourier coefficient bridge.

The source is read only as provenance.  Its finite decimal literals are
interpreted as rationals and each +/- pi/2 offset as an exact quarter turn.
The DH mass formula is then evaluated in the Laurent ring
Q(i)[z_1^+/-1,...,z_6^+/-1].  The result is compared entrywise with the frozen
610-row rational Fourier table, adding the source's exact 1e-6 diagonal
regularizer.  No floating-point operation is used by this checker.

This is an executable exact coefficient leaf.  It is intentionally separate
from the Lean contract in ExactCoefficientBridge.lean: the latter proves the
generic evaluator consequence, while this checker supplies the source/table
coefficient evidence and keeps the external source hash explicit.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKFLOW = HERE.parents[1]
EXTERNAL_ROOT = Path(
    r"C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized"
)
SOURCE = Path(os.environ.get("ROUTEB_DH_SOURCE", str(EXTERNAL_ROOT / "routeB_dense_Mq" / "dhport_lib.jl")))
REFERENCE = WORKFLOW / "examples" / "routeb_source_binding_audit" / "snapshots" / "current_exact" / "routeB_fourier_mass_full_rational.csv"
RESULT = HERE / "CHECK_RESULT.json"
RECEIPT = HERE / "CHECKER_OUTPUT.txt"

EXPECTED_SOURCE_SHA256 = "aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936"
EXPECTED_REFERENCE_SHA256 = "a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8"
N = 6
ZERO = (0,) * N
Gauss = tuple[F, F]
Poly = dict[tuple[int, ...], Gauss]


def gadd(a: Gauss, b: Gauss) -> Gauss:
    return a[0] + b[0], a[1] + b[1]


def gmul(a: Gauss, b: Gauss) -> Gauss:
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def trim(p: dict[tuple[int, ...], Gauss]) -> Poly:
    return {k: v for k, v in p.items() if v != (F(0), F(0))}


def pconst(x: F | int) -> Poly:
    x = F(x)
    return {} if x == 0 else {ZERO: (x, F(0))}


def padd(*terms: Poly) -> Poly:
    out: dict[tuple[int, ...], Gauss] = defaultdict(lambda: (F(0), F(0)))
    for term in terms:
        for key, value in term.items():
            out[key] = gadd(out[key], value)
    return trim(out)


def pscale(p: Poly, x: F | int | Gauss) -> Poly:
    scalar = x if isinstance(x, tuple) else (F(x), F(0))
    return trim({key: gmul(value, scalar) for key, value in p.items()})


def pmul(a: Poly, b: Poly) -> Poly:
    out: dict[tuple[int, ...], Gauss] = defaultdict(lambda: (F(0), F(0)))
    for ka, va in a.items():
        for kb, vb in b.items():
            key = tuple(x + y for x, y in zip(ka, kb))
            out[key] = gadd(out[key], gmul(va, vb))
    return trim(out)


def pneg(p: Poly) -> Poly:
    return pscale(p, -1)


def dot(a: list[Poly], b: list[Poly]) -> Poly:
    return padd(*(pmul(x, y) for x, y in zip(a, b)))


def cross(a: list[Poly], b: list[Poly]) -> list[Poly]:
    return [
        padd(pmul(a[1], b[2]), pneg(pmul(a[2], b[1]))),
        padd(pmul(a[2], b[0]), pneg(pmul(a[0], b[2]))),
        padd(pmul(a[0], b[1]), pneg(pmul(a[1], b[0]))),
    ]


def matmul(a: list[list[Poly]], b: list[list[Poly]]) -> list[list[Poly]]:
    return [[padd(*(pmul(a[i][k], b[k][j]) for k in range(4)))
             for j in range(4)] for i in range(4)]


def eye4() -> list[list[Poly]]:
    return [[pconst(int(i == j)) for j in range(4)] for i in range(4)]


def parse_phase(token: str) -> int:
    token = token.strip()
    if token in {"0", "0.0"}:
        return 0
    if token == "pi/2":
        return 1
    if token == "-pi/2":
        return -1
    raise AssertionError(f"DH angle is not an exact quarter turn: {token!r}")


def exact_quarter_turn(phase: int) -> Gauss:
    return {
        0: (F(1), F(0)), 1: (F(0), F(1)),
        2: (F(-1), F(0)), 3: (F(0), F(-1)),
    }[phase % 4]


def trig_laurent(joint: int, phase: int) -> tuple[Poly, Poly]:
    ep = exact_quarter_turn(phase)
    em = (ep[0], -ep[1])
    plus = tuple(int(k == joint) for k in range(N))
    minus = tuple(-x for x in plus)
    cosine = {plus: gmul(ep, (F(1, 2), F(0))),
              minus: gmul(em, (F(1, 2), F(0)))}
    sine = {plus: gmul(ep, (F(0), F(-1, 2))),
            minus: gmul(em, (F(0), F(1, 2)))}
    return trim(cosine), trim(sine)


def parse_array(source: str, name: str) -> list[F]:
    match = re.search(rf"\b{name}\s*=\s*\[([^\]]*)\]", source, re.S)
    if not match:
        raise AssertionError(f"missing source array {name}")
    return [F(x.strip()) for x in match.group(1).split(",")]


def parse_source() -> tuple[list[int], list[F], list[F], list[int], list[F], list[F], F, str]:
    raw = SOURCE.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SOURCE_SHA256:
        raise AssertionError(f"canonical source hash drift: {digest}")
    text = raw.decode("utf-8")
    required = [
        "z[:, ii] = Tc[end][1:3, 3]",
        "th = q[ii] + DH[ii, 1]",
        "pcom = 0.5 .* (o[:, ii] + o[:, ii+1])",
        "Ii = (I_val[ii] / 3) .* Matrix{Float64}(I, 3, 3)",
        "Jv[:, jj] = cross(z[:, jj], pcom - o[:, jj])",
        "Jw[:, jj] = z[:, jj]",
        "M += m[ii] .* (Jv' * Jv) + Jw' * (Ri * Ii * Ri') * Jw",
        "return M + Float64(regularization) .* Matrix{Float64}(I, 6, 6)",
    ]
    missing = [fragment for fragment in required if fragment not in text]
    if missing:
        raise AssertionError(f"canonical mass formula drift; missing {missing}")
    match = re.search(r"\bDH\s*=\s*\[(.*?)\]", text, re.S)
    if not match:
        raise AssertionError("missing DH source matrix")
    rows = []
    for line in match.group(1).splitlines():
        fields = line.strip().rstrip(";").split()
        if fields:
            if len(fields) != 4:
                raise AssertionError(f"unexpected DH row: {line!r}")
            rows.append(fields)
    if len(rows) != N:
        raise AssertionError(f"expected {N} DH rows, got {len(rows)}")
    theta = [parse_phase(row[0]) for row in rows]
    d = [F(row[1]) for row in rows]
    a = [F(row[2]) for row in rows]
    alpha = [parse_phase(row[3]) for row in rows]
    masses = parse_array(text, "m")
    inertias = parse_array(text, "I_val")
    if len(masses) != N or len(inertias) != N:
        raise AssertionError("source mass/inertia tables must each have six entries")
    reg_match = re.search(r"const\s+MASS_REGULARIZER\s*=\s*([^\s]+)", text)
    if not reg_match:
        raise AssertionError("missing MASS_REGULARIZER")
    return theta, d, a, alpha, masses, inertias, F(reg_match.group(1)), digest


def source_exact_mass() -> tuple[list[list[Poly]], F, str]:
    theta, d, a, alpha, masses, inertias, regularizer, digest = parse_source()
    transforms = [eye4()]
    origins = [[pconst(0) for _ in range(3)] for _ in range(N + 1)]
    axes = [[pconst(0) for _ in range(3)] for _ in range(N)]
    for i in range(N):
        ct, st = trig_laurent(i, theta[i])
        ca0, sa0 = exact_quarter_turn(alpha[i])
        ca, sa = pconst(ca0), pconst(sa0)
        step = [
            [ct, pneg(pmul(st, ca)), pmul(st, sa), pscale(ct, a[i])],
            [st, pmul(ct, ca), pneg(pmul(ct, sa)), pscale(st, a[i])],
            [pconst(0), sa, ca, pconst(d[i])],
            [pconst(0), pconst(0), pconst(0), pconst(1)],
        ]
        # The source takes the parent-frame axis before applying this step.
        axes[i] = [transforms[-1][k][2] for k in range(3)]
        current = matmul(transforms[-1], step)
        transforms.append(current)
        origins[i + 1] = [current[k][3] for k in range(3)]

    mass = [[{} for _ in range(N)] for _ in range(N)]
    for link in range(N):
        pcom = [pscale(padd(origins[link][k], origins[link + 1][k]), F(1, 2))
                for k in range(3)]
        jv = [[pconst(0) for _ in range(N)] for _ in range(3)]
        jw = [[pconst(0) for _ in range(N)] for _ in range(3)]
        for joint in range(link + 1):
            offset = [padd(pcom[k], pneg(origins[joint][k])) for k in range(3)]
            col = cross(axes[joint], offset)
            for k in range(3):
                jv[k][joint] = col[k]
                jw[k][joint] = axes[joint][k]
        rotation = [[transforms[link + 1][r][c] for c in range(3)] for r in range(3)]
        rotated_axes = []
        for joint in range(N):
            if joint > link:
                rotated_axes.append([pconst(0) for _ in range(3)])
                continue
            rotated_axes.append([
                padd(*(pmul(rotation[r][c], jw[r][joint]) for r in range(3)))
                for c in range(3)
            ])
        for r in range(N):
            for c in range(N):
                tv = dot([jv[k][r] for k in range(3)], [jv[k][c] for k in range(3)])
                # z_r^T R (I_val/3) R^T z_c = (I_val/3)(R^T z_r)^T(R^T z_c).
                rw = dot(rotated_axes[r], rotated_axes[c])
                mass[r][c] = padd(mass[r][c], pscale(tv, masses[link]),
                                   pscale(rw, inertias[link] / 3))
    for i in range(N):
        for j in range(N):
            if i == j:
                mass[i][j] = padd(mass[i][j], pconst(regularizer))
    return mass, regularizer, digest


def load_reference(regularizer: F) -> tuple[list[list[Poly]], int]:
    digest = hashlib.sha256(REFERENCE.read_bytes()).hexdigest()
    if digest != EXPECTED_REFERENCE_SHA256:
        raise AssertionError(f"frozen Fourier CSV hash drift: {digest}")
    out = [[{} for _ in range(N)] for _ in range(N)]
    rows = 0
    with REFERENCE.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            rows += 1
            i, j = int(row["row"]) - 1, int(row["col"]) - 1
            if not (0 <= i < N and 0 <= j < N):
                raise AssertionError(f"matrix index out of range: {(i + 1, j + 1)}")
            key = tuple(int(row[f"nu{k}"]) for k in range(1, N + 1))
            coeff = (F(int(row["real_num"]), int(row["real_den"])),
                     F(int(row["imag_num"]), int(row["imag_den"])))
            old = out[i][j].get(key, (F(0), F(0)))
            out[i][j][key] = gadd(old, coeff)
    if rows != 610:
        raise AssertionError(f"expected 610 CSV rows, got {rows}")
    for i in range(N):
        out[i][i][ZERO] = gadd(out[i][i].get(ZERO, (F(0), F(0))),
                                (regularizer, F(0)))
        out[i][i] = trim(out[i][i])
    return out, rows


def conjugate_symmetric(poly: Poly) -> bool:
    return all(poly.get(tuple(-x for x in key)) == (real, -imag)
               for key, (real, imag) in poly.items())


def main() -> None:
    source, regularizer, digest = source_exact_mass()
    reference, row_count = load_reference(regularizer)
    mismatches = []
    supports = []
    active = set()
    for i in range(N):
        for j in range(N):
            if source[i][j] != reference[i][j]:
                support_delta = sorted(set(source[i][j]) ^ set(reference[i][j]))
                coefficient_delta = sorted(
                    key for key in set(source[i][j]) & set(reference[i][j])
                    if source[i][j][key] != reference[i][j][key]
                )
                mismatches.append({"entry": [i + 1, j + 1],
                                   "support_delta": support_delta,
                                   "coefficient_delta": coefficient_delta})
            supports.append(len(source[i][j]))
            active.update(key_index for key in source[i][j] for key_index, power in enumerate(key) if power)
            if not conjugate_symmetric(source[i][j]):
                raise AssertionError(f"non-conjugate coefficient map at M{i + 1}{j + 1}")
    if mismatches:
        raise AssertionError(json.dumps({"mismatches": mismatches}, default=list))
    payload = {
        "status": "EXACT_36_ENTRY_SOURCE_TO_FOURIER_COEFFICIENT_EQUALITY_CHECKED",
        "entries_checked": 36,
        "csv_rows_checked": row_count,
        "canonical_source": str(SOURCE).replace("\\", "/"),
        "canonical_source_sha256": digest,
        "reference_csv_sha256": hashlib.sha256(REFERENCE.read_bytes()).hexdigest(),
        "exact_semantics": {
            "decimal_literals": "rational",
            "pi_over_2": "exact quarter turn",
            "coefficient_domain": "Gaussian rationals",
            "default_mass_regularizer": str(regularizer),
            "all_36_coefficient_maps_equal": True,
            "all_real_q_extensional_equality": True,
            "entry_support_min": min(supports),
            "entry_support_max": max(supports),
            "active_joint_angles": sorted(index + 1 for index in active),
        },
        "float64_semantics": {
            "used": False,
            "source_runtime_bridge_proved": False,
        },
        "lean_bridge": {
            "generic_coefficient_evaluator_compiled": "see COMPILE_RECEIPT.md",
            "source_coefficients_instantiated_in_lean": False,
        },
        "formal_certificate_allowed": False,
        "physical_certificate_allowed": False,
        "minimal_open_gap": "Lean/source instantiation and Julia Float64 execution semantics remain separate obligations",
    }
    RESULT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    receipt = (
        "EXACT_36_ENTRY_SOURCE_TO_FOURIER_COEFFICIENT_EQUALITY_CHECKED\n"
        f"source_sha256={digest}\n"
        f"reference_csv_sha256={payload['reference_csv_sha256']}\n"
        "entries_checked=36\n"
        f"csv_rows_checked={row_count}\n"
        f"support_range={min(supports)}..{max(supports)}\n"
        "float64_used=false\n"
        "formal_certificate_allowed=false\n"
    )
    RECEIPT.write_text(receipt, encoding="utf-8")
    print(receipt, end="")


if __name__ == "__main__":
    main()
