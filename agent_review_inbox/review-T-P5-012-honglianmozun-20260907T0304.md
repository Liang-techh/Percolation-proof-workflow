---
kind: review_result
review_id: review-T-P5-012-honglianmozun-20260907T0304
task_id: T-P5-012
source_agent: 红莲魔尊
claimed_at: 2026-09-07T02:50:00-06:00
created_at: 2026-09-07T03:04:00-06:00
inspected_commit: cee6a020d6c5f5b425428b1027a97d4ab41d6e52
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_parameter_dependent_storage_shift_and_affine_ramp_work_then_source_classify_controller_mismatch
---

# T-P5-012 — parameter-dependent conservative-force extraction, the exact ramp-work remainder, and the nonconservative bias boundary

## Scope

`T-P5-008` reduced the P5 force-error ledger by moving the constant mass
regularizer and the frozen-potential gravity FD discrepancy into storage.
`T-P5-011` then showed that the remaining exact-real C-FD cubic power can be
self-absorbed on a Lyapunov energy sublevel.  The latest execution split
`T-P4-007` keeps `delta_ctrl` and the solve defect explicit, while `T-P8-008`
shows that the mathematically correct mechanical trajectory uses the ramp

```text
w(t) = c*t,    w'(t) = c.
```

The next energy question is therefore not merely whether a controller/runtime
force remainder is numerically small.  Before charging it as an additive bias,
one should ask whether it is a gradient in the mechanical coordinate `q` and
can be moved into storage.  When that gradient depends on the ramp parameter
`w`, however, a new exact term appears from `w'`.

This review proves that bridge, gives the complete affine decomposition, and
identifies a sharp obstruction: **being conservative for each frozen value of
`w` is not enough to be removable at zero cost along a nonzero P8 ramp.**

Inputs inspected:

- `review-T-P5-008-honglianmozun-20260906T2348.md`;
- `review-T-P5-011-honglianmozun-20260907T0155.md` and the compiled formal
  follow-up `review-T-P5-011-sumengchen-20260907T0221.md`;
- `review-T-P4-007-liuguanyi-20260907T0212.md` for the execution-lift residual
  split with `delta_ctrl` and solve defect;
- `review-T-P8-008-guyuefangyuan-20260907T0231.md` for the exact first-12
  mechanical ramp elimination `w=c*t`;
- `review-T-P4-014-kuangmanmozun-20260907T0247.md` for the independent P4
  additive/transverse Schur boundary.  That result is not reproved here.

No source coefficient identification, IEEE bound, ODE coverage, admission,
provenance, or final P5/M4 closure is claimed.

## 1. General parameter-dependent storage shift

Let `q(t) in R^n`, `v(t)=q'(t)`, and let the scalar ramp state satisfy

```text
w'(t) = c.                                                   (1)
```

Suppose the current P5 ledger contains a force-power term

```text
<F(q,w), v>,                                                 (2)
```

and suppose there is a differentiable scalar potential `Phi(q,w)` satisfying

```text
F(q,w) = grad_q Phi(q,w).                                    (3)
```

The chain rule gives

```text
d/dt Phi(q(t),w(t))
 = <grad_q Phi, v> + partial_w Phi * c
 = <F(q,w),v> + c * partial_w Phi(q,w).                      (4)
```

Therefore, if

```text
V_dot <= L + <F(q,w),v> + P_rem,                             (5)
```

then the shifted storage

```text
V_hat := V - Phi(q,w)                                        (6)
```

satisfies the exact ledger

```text
V_hat_dot
 <= L + P_rem - c * partial_w Phi(q,w).                      (7)
```

This is the central bridge.  It separates two very different facts:

- the `q`-gradient part of `F` is still removable exactly;
- the parameter dependence of that potential creates the **ramp-work term**
  `-c partial_w Phi`.

When `c=0`, (7) reduces to the ordinary conservative-force storage shift used
implicitly in `T-P5-008`.  For nonzero P8 ramp, the last term cannot be dropped.

## 2. Affine controller/runtime force: exact symmetric/skew split

A particularly useful source-facing form is

```text
F(q,w) = H q + ell*w + b + r(q,v,w),                         (8)
```

where `H` is an `n x n` real matrix, `ell,b in R^n`, and `r` is the part not yet
classified as conservative.

Split

```text
S := (H + H^T)/2,
K := (H - H^T)/2,                                            (9)
```

so `S^T=S` and `K^T=-K`.  Then

```text
Hq = Sq + Kq.                                                (10)
```

The affine force

```text
F_cons(q,w) := S q + ell*w + b                              (11)
```

is exactly the `q`-gradient of

```text
Phi(q,w)
 := 1/2 q^T S q + w * ell^T q + b^T q.                      (12)
```

Indeed,

```text
grad_q Phi = S q + ell*w + b,
partial_w Phi = ell^T q.                                    (13)
```

Thus the power identity is

```text
<F(q,w),v>
 = d/dt Phi(q,w)
   - c * ell^T q
   + <Kq + r(q,v,w), v>.                                    (14)
```

After subtracting `Phi` from storage, the exact remainder is therefore

```text
-c * ell^T q + <Kq+r,v>.                                    (15)
```

Three consequences are immediate.

### 2.1 A constant force offset is not automatically a dissipative bias

The vector `b` is the gradient of `b^T q`.  If it enters the energy ledger only
through `b^T v`, it can be removed **exactly** by the storage shift
`V -> V-b^T q`.  Its magnitude is irrelevant to that derivative identity.

What changes is the lower-bound/coercivity problem for storage; see Section 5.
Thus a source theorem should not classify a constant controller force mismatch
as a genuine P5 additive *power* bias before checking whether this conservative
extraction is admissible on the covered `q` domain.

### 2.2 The symmetric configuration-linear part is also exact storage

`Sq` is the gradient of `q^T S q/2`.  Only the skew part `Kq` survives as a
nonconservative affine force.  Note that `q^T K q=0` does **not** imply
`v^T Kq=0`; the latter is generally nonzero.

### 2.3 The `w`-linear part is conservative only at frozen parameter

For fixed `w`, `ell*w` is a constant force in `q`, hence conservative.  Along
`w'=c`, however, moving it into storage necessarily produces the ramp-work term

```text
-c * ell^T q.                                               (16)
```

That term is configuration power injection, not velocity-quadratic damping.

## 3. Exact obstruction: frozen-parameter conservativity is insufficient under ramp

The obstruction can be stated without the affine ansatz.

Suppose `c != 0` and one seeks a state function `Psi(q,w)` whose derivative
along **every** mechanical tangent `q'=v`, `w'=c` exactly reproduces
`F(q,w)^T v` with no extra term:

```text
<grad_q Psi(q,w),v> + c * partial_w Psi(q,w)
 = <F(q,w),v>                                               (17)
```

for every `v`.

Set `v=0`.  Since `c!=0`, (17) forces

```text
partial_w Psi(q,w)=0.                                       (18)
```

Then comparison of the coefficients of arbitrary `v` forces

```text
grad_q Psi(q,w)=F(q,w).                                     (19)
```

A universal state-storage removal with zero ramp remainder therefore requires
the potential to be independent of `w`; under the usual connected/smooth
setting this in turn requires the removable force itself to be independent of
`w`.

For the affine family `(8)`, this forces

```text
ell = 0.                                                     (20)
```

### Scalar counterexample

Take one coordinate and

```text
F(q,w)=w,
Phi(q,w)=w*q,
w'=c.
```

Then

```text
F v = w v,
d/dt(wq) = w v + c q,
```

hence

```text
w v = d/dt(wq) - c q.                                       (21)
```

For `q(t)=t`, `w(t)=c t`, `v=1`, the omitted ramp term is exactly `c t`.
Therefore the route “prove `F` is a gradient for each fixed `w`, subtract its
potential, and declare zero residual” is mathematically false whenever the
potential depends on the nonzero ramp.

## 4. Closed-one-form viewpoint and the skew obstruction

Equation (7) has a useful structural interpretation.  The mechanical work
one-form is

```text
omega = sum_i F_i(q,w) dq_i.                                (22)
```

To be the differential of a storage function on the **extended** `(q,w)` state
without a `dw` work term, it must not only be curl-free in `q`; its `w`
dependence must also be compatible with the missing `dw` component.  In the
present ramp contract that compatibility is exactly what fails when
`partial_w F != 0`.

For the affine `Hq+ell*w+b`, there are two independent obstructions:

```text
skew(H) != 0        -> nonzero circulation in q,
ell != 0, c != 0    -> unavoidable ramp-work injection.      (23)
```

A concrete skew counterexample uses

```text
K = [[0,-k],[k,0]].
```

On the unit circle, `Kq` is tangent and its line integral around one loop is
nonzero for `k!=0`; hence no scalar configuration potential can remove this
term globally.  This rules out treating an arbitrary linear controller
mismatch as conservative merely because it vanishes at `q=0`.

## 5. The storage lower bound survives conservative extraction on a bounded P8 domain

`T-P5-011` uses a lower bound on the non-kinetic storage to obtain

```text
A(v) <= 2600000 * Z.                                        (24)
```

Subtracting `Phi` does not destroy this architecture if `Phi` has an upper
bound on the same covered state domain.

Write the pre-shift modified storage as

```text
V = T_eps + W,
W >= W_min.                                                  (25)
```

Assume on the same domain

```text
Phi(q,w) <= Phi_max.                                         (26)
```

Then

```text
V_hat = T_eps + (W-Phi),
W-Phi >= W_min-Phi_max.                                     (27)
```

Define

```text
Z_hat := V_hat - (W_min-Phi_max).                           (28)
```

The exact same kinetic coercivity remains:

```text
Z_hat >= T_eps >= eps/2 * ||v||^2,
A(v) <= 2600000 * Z_hat                                     (29)
```

for the current `eps=10^-6` and `d_max=13/10`.

Thus conservative extraction can be inserted *before* the `T-P5-011` cubic
self-bootstrap with no change in the constant `K=2600000`; only the lower-bound
reference changes.

For the affine potential `(12)`, a coordinate box

```text
|q_i| <= Q_i,   |w| <= Wbar                                (30)
```

gives the explicit safe bound

```text
Phi(q,w)
 <= 1/2 sum_ij |S_ij| Q_i Q_j
    + Wbar * sum_i |ell_i| Q_i
    + sum_i |b_i| Q_i.                                      (31)
```

Under the P8 ramp on `[0,1]`, `w=c t`, one may take `Wbar=|c|`.
So a source/P8 box can supply `Phi_max` directly if this affine split is found.

## 6. Composition with the cubic energy barrier

After applying the storage shift, suppose the remaining ledger has the form

```text
Z_hat_dot
 <= -A + P_C + P_rel
    + <r_nc,v>
    - c * partial_w Phi,                                    (32)
```

where `r_nc` includes only terms not already extracted as conservative.  This
is the proper place for the solve defect, skew controller remainder, or other
execution remainder unless a stronger structure theorem is proved for them.

Let

```text
P_rel <= kappa_R A,
|P_C| <= kappa_C A,
kappa_R + kappa_C < 1,
g := 1-kappa_R-kappa_C > 0.                                 (33)
```

The `|P_C|` bound can come from the square-only `T-P5-011` energy barrier.  Then

```text
Z_hat_dot
 <= -g A + <r_nc,v> - c * partial_w Phi.                    (34)
```

This is a substantially cleaner classification than placing every source
mismatch into a single force envelope.

If the ramp-work term has the good sign

```text
-c * partial_w Phi <= 0,                                    (35)
```

and the nonconservative force is damping-relative, (34) returns directly to the
strict P5 small-gain route.  If either term has a genuine positive component,
it needs its own consumer; it must not be hidden inside `S_F` or the C-FD cubic
constant.

For the affine `w` dependence, a same-domain q-box gives

```text
|-c ell^T q|
 <= |c| * sum_i |ell_i| Q_i.                                (36)
```

This is the natural finite-horizon/P8 injection budget generated by the ramp.

## 7. Sharp energy-level boundary for a nonconservative force remainder

Let `D=diag(d_i)>0` and

```text
A(v)=v^T D v.
```

For a fixed force remainder `r`, define its damping-dual square

```text
R_D^2 := r^T D^{-1} r.                                      (37)
```

Completing the square gives the exact identity, for `g>0`,

```text
-g v^T D v + r^T v
 = -g (v-(1/(2g))D^{-1}r)^T D (v-(1/(2g))D^{-1}r)
   + R_D^2/(4g).                                            (38)
```

Hence

```text
sup_v [-g A(v)+r^T v] = R_D^2/(4g).                         (39)
```

This is sharp.  A nonzero fixed nonconservative force cannot be swallowed by
quadratic damping in an entire neighborhood of `v=0`.

### Scalar failure witness

Take `A=d v^2`, `b>0`, and the exact scalar ledger

```text
Z_dot = -g d v^2 + b v.                                     (40)
```

At

```text
v = b/(2 g d)
```

one gets

```text
Z_dot = b^2/(4 g d) > 0.                                    (41)
```

Therefore a theorem claiming local strict Lyapunov decrease from only a
uniform nonzero force bound is impossible.  One needs at least one of:

1. conservative extraction as above;
2. a vanishing/state-relative theorem for the remainder;
3. an explicit ultimate/finite-horizon injection budget;
4. a stronger cross-term/hypocoercive Lyapunov functional using configuration
   dynamics.

This is the energy analogue of the independent P4 zero-slice/transverse-reserve
obstruction, but it does not take over the P4 Schur work.

A uniform dual bound `R_D^2 <= B^2` does still imply, for every `theta>0`,

```text
r^T v <= theta A + B^2/(4 theta).                            (42)
```

Thus (34) yields

```text
Z_hat_dot
 <= -(g-theta) A + B^2/(4 theta) - c partial_w Phi.          (43)
```

This is an ultimate/finite-horizon estimate, not strict local decay.  In
particular, the one-sided coercivity from `T-P5-011`, `A<=K Z_hat`, is the
**wrong direction** for converting (43) into an invariant `Z_hat` ball.  Such a
conversion needs additional configuration/observability structure or a
finite-time P8 budget.

## 8. Exact finite-horizon integration-by-parts form for the ramp term

For the affine `ell*w` force, (14) can also be integrated directly.  On
`[0,T]` with `w'=c`,

```text
integral_0^T (ell*w)^T v dt
 = [w * ell^T q]_0^T - c * integral_0^T ell^T q dt.          (44)
```

Under the P8 initialization `w(0)=0` and `w(T)=cT`, this is

```text
= cT * ell^T q(T) - c * integral_0^T ell^T q(t) dt.          (45)
```

This gives a second legitimate consumer when strict pointwise dissipation is
not available: a verified P8 q-box/flowpipe can bound the total ramp work over
`[0,1]` without pretending it is damping-relative.

## 9. Recommended source classification before any new P5 bias constant

For `delta_ctrl` or another controller-like execution force, the highest-value
source theorem is no longer simply

```text
||delta_ctrl|| <= B.
```

A more informative typed split is

```text
delta_ctrl(q,v,w)
 = S q + ell*w + b       [q-conservative affine part]
   + K q                 [skew/nonconservative linear part]
   + r_rel(q,v,w)        [vanishing/relative part]
   + r_exec(q,v,w),      [remaining execution term]          (46)
```

with `S^T=S`, `K^T=-K`.

Then P5 can:

- move `Sq + ell*w + b` into `Phi`;
- charge exactly `-c ell^T q` as ramp work;
- test `Kq+r_rel+r_exec` with weighted-dual/relative or ultimate-bound tools;
- update `W_min` using a same-domain `Phi_max` instead of discarding the energy
  bootstrap.

The solve defect from `T-P4-007` should remain in `r_exec` unless an independent
structure theorem shows it is a gradient or vanishes suitably.  Likewise, the
centered runtime gravity term `DeltaG(q)-DeltaG(0)` is not automatically
conservative merely because it vanishes at zero; conservativity requires a
potential/curl theorem.

## 10. Lean-friendly theorem package

The first formal child should stay algebraic and avoid a large ODE API.

### A. Storage-shift ledger

Treat the chain-rule result as an input identity:

```lean
theorem parameter_storage_shift_ledger
    (dV dPhi base pCons pRem rampWork : Real)
    (hV : dV <= base + pCons + pRem)
    (hPhi : dPhi = pCons + rampWork) :
    dV - dPhi <= base + pRem - rampWork
```

Then a calculus wrapper may later instantiate

```text
pCons    = <grad_q Phi,v>,
rampWork = c * partial_w Phi.
```

### B. Affine directional identity

For finite vectors/matrices, define `(S q)_i` and dot products by finite sums
and prove, under symmetry of `S`,

```text
D[(1/2 q^T S q + w ell^T q + b^T q)](v,c)
 = (S q + ell*w + b)^T v + c * ell^T q.                     (47)
```

This is the minimal theorem needed to make `(14)` checkable without formalizing
full multivariable gradients first.

### C. Symmetric/skew force decomposition

Prove algebraically

```text
Hq = ((H+H^T)/2)q + ((H-H^T)/2)q
```

and the symmetry/skew properties.  The formalization should **not** add a false
lemma `v^T Kq=0` for skew `K`.

### D. Sharp dual-force power bump

A separate scalar/quadratic theorem can formalize (38)--(39), preferably in a
matrix-free weighted-dot form if an inverse-matrix API is inconvenient.

## 11. What remains open

- Source/checker: determine whether `delta_ctrl` actually has an affine or
  gradient part and freeze its exact coefficients if so.
- P8/source: provide the same-domain `q`/`w` bounds needed for `Phi_max` and for
  the ramp-work budget; `T-P8-008` already supplies the mathematical
  `w=c*t` interface but not the flowpipe coverage.
- Execution lane: bound/classify the solve defect and remaining IEEE terms;
  do not relabel them conservative without a mathematical potential theorem.
- Energy layer: if the ramp-work term is sign-indefinite and cannot be made
  state-relative, choose between a finite-horizon injection budget and a new
  cross-term/hypocoercive Lyapunov functional.  `T-P5-011` alone cannot turn a
  positive injection constant into an invariant energy ball.
- Formalization: implement the small theorem package above, then leave
  independent validation to 封不觉 and integration to 梁智炜.

## Status

`pending` mathematical child only.  This review changes no P5/P8/P4/M4 status
and makes no admission claim.
