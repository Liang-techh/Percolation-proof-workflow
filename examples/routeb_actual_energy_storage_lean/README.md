# Concrete actual-energy storage family

Owned scope: only `examples/routeb_actual_energy_storage_lean/`. No registry or
state writes, full regression, LP solve, dependency build, or download.

Compiler status is recorded in the immutable `output/run-*/terminal.log` files
and summarized in `ATTEMPT_HISTORY.md`. Failed attempts are preserved and are
not verification receipts.

FINAL SUCCESS: `output/run-ZWEIdfZ8/terminal.log`, verifier exit 0 at
2026-09-05T21:11:05Z. ActualStorage compiled with only propext, Classical.choice,
Quot.sound in every printed theorem dependency. Its imported ReferenceMass
compiled with exit 0 in run-EQMuJx15 and was reused only after checking exact
source equality. Both current source files match these compiled snapshots.
See `FINAL_RECEIPT.md` for hashes. All six attempts are preserved.

## Concrete finite-vector results

All vectors are `Fin 6 -> Real`; quadratic forms and squared norms are actual
finite sums. Physical q4 is Lean `q 3`. `ReferenceMass.lean` contains the literal
36 rational entries of both M0 and H0 from coupled reference
`run-20260905T192654Z-3dbe159f/reference.json`.

`M0_dsos_identity` writes `sum vi^2 - v'M0v` as six nonnegative diagonal
slack terms and nine positive rational multiples of `(vi +/- vj)^2`.
`rowAbs_lt_one` checks all six absolute row sums by rational arithmetic.
`M0_le_identity` and `kinetic_M0_upper` follow from that exact identity;
neither assumes the kinetic upper bound.

The narrow Python Fraction audit independently checks the Lean literals against
the reference JSON, reconstructs M0 from all 610 mass CSV rows with the explicit
1/1000000 diagonal regularizer, reconstructs H0 from the 17 potential rows,
and reports the row sums. This is a source-literal audit, not a Lean proof that
the external CSV or Julia/Float64 evaluator denotes the intended physical model.

`actualSignedGap` specializes the compiled signedGap definition from
`routeb_signed_gap_lean/output/run-iH9FGdAL`. Define

```
W0 = (1/2)v'M0v - Sgap + (7/75)q4^2
   = (1/2)v'Mv + (U-Uzero-(1/2)q'Hq) + (7/75)q4^2.
```

The H0 finite quadratic form is expanded and matched to the remainder identity
from compiled `routeb_gravity_twist_floor/output/run-LIFMhESI`. Under the explicit
bindings H=H0, U=referencePotential(q), Uzero=3108789/400000, this proves
`W0=(1/2)v'Mv+R+(7/75)q4^2`.
`W0_nonneg` reuses the compiled global `R >= -q4^4/40` and assumes only those
source bindings, quadratic-form PSD of M, and `q4^2 <= 56/15`.
`W0_from_source_nominal` additionally exposes the equality needed to identify
an external nominal matrix with this literal M0.

For the original twelve-coordinate initial ball,

```
sum qi^2 + sum vi^2 <= 9/400,
Sgap >= -3/10000                         [explicit audit premise],
```

`W0_initial_upper` proves `W0 <= 231/20000`. This uses the full finite-vector
M0 theorem. It does not assume a scalar upper bound or restrict the ball to
the two local axes.

For `V=f W0 + sum pi qi^2 + h c^2`, `storageV_initial_upper` proves

```
V <= (9/400) beta + 3f/10000 + 3h
```

under f,h>=0, the ball and gap premises above, c^2<=3, beta>=f/2 and
`beta>=pi+(7f/75)*indicator(i=4)` for each of six axes.
The upper theorem does not need pi>=0; the positivity theorem does.

## Synthesis interface

`decayPolynomial a t = sum(j=1,...,d) a_j (1-t)^j`.
The finite index is stored as `j.val+1`. All coefficients are nonnegative.
A j=0 term would have to have zero coefficient to enforce the terminal equality.
F, each of the six P rows, and C supply the coefficients of f, pi and h.
`synthesisV` evaluates the concrete storage above.

`synthesisV_nonneg_on_P` proves nonnegativity throughout
`PDomain = {0<=t<=1, q4^2<=56/15}` under the explicit source bindings and M PSD
at the evaluated state. Other coordinates, velocities and c are unrestricted
for this positivity result. Any more restrictive physical P-domain is covered
when it implies these conditions.
`synthesisV_terminal` proves V(1)=0 for every state, without physical premises.
`synthesisV_initial_upper` exposes linear inequalities in coefficient sums:
f(0)=sum F, pi(0)=sum P_i, h(0)=sum C.
Coefficient selection and any LP candidate remain with the main agent Pauli.

## Explicit remaining premises and work

1. The external DH/Fourier/implemented source must be identified with the real
   mass and potential, H0, M0 and Uzero used here. Literal coefficient matching
   is audited; physical source correctness is not proved.
2. Establish `forall z, 0<=z'M(q)z` on the physical domain. This leaf proves
   M0<=I, not global PSD of the actual state-dependent mass.
3. Establish q4^2<=56/15 wherever positivity is invoked, and the initial
   full12 ball and ramp condition c^2<=3 where the initial bound is invoked.
4. `Sgap>=-3/10000` on the entire initial ball is an explicit rational audit
   premise. It is not proved here and does not follow from the gravity floor.
5. Derivative composition is assigned to the separate agent owning
   `examples/routeb_actual_storage_derivative/` for the revision47 checkpoint.
   No derivative file is added here. The expected identity is
   `W0dot=-v'(K+H0)q-v'Dv+v'G w+(14/75)q4v4+v'eta`, with no delta term.
   It requires the compiled signed-gap source derivative, same-state nominal
   acceleration and drive, kinematics, source derivatives, symmetry and actual
   force balance. For c'=0 the family derivative adds f'W0,
   sum(pi' qi^2+2pi qi vi), and h'c^2 to f W0dot. This formula and the exact g=0
   composition have not been compiled in this leaf.
6. Eta includes the chosen physical/source/controller/parameter, FD, Float64
   and solve defects with the signed-gap convention. No eta bound, vanishing
   eta, defect identification, or defect-work estimate is proved here.
7. No coefficient feasibility, dissipation inequality, integration/regularity,
   existence/continuation, or physical J<=1 is established by these storage
   shape and initial-bound results.

## Reproduce

From the workspace root: `wsl -d Ubuntu -- bash examples/routeb_actual_energy_storage_lean/verify.sh`.
Only ReferenceMass and ActualStorage are compiled, with `warningAsError=true`.
Pinned executable: Lean 4.33.1. Cached Mathlib revision:
`0df444a360eaa60ab8c11dca51a86af692955474`.
The verifier snapshots all new sources, its script, source audit and available
reports, reference inputs and imported local oleans before compilation. Every
attempt has its own pre-run SHA256 manifest, commands, terminal log, exit codes,
and successful output hashes. Cached local dependencies are copied from the two
specified final runs. No Lake command or download is used.

For the final storage-only replay, append `ActualStorage` to the verifier
command. That mode reuses the successful local ReferenceMass olean from
run-EQMuJx15 after a byte-for-byte source comparison and records its compile log
as an input. The default command still compiles both new modules.
