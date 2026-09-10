---
kind: review_result
review_id: review-T-P5-252-source-slice-partial-metric-coercivity-guyuefangyuan-20260910T1418Z
task_id: T-P5-252-SOURCE-SLICE-PARTIAL-METRIC-COERCIVITY
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T14:19:30Z
claim_commit: 0ac3db37b50bf7c261d39d31228eff48d247723a
inspected_commit: af5077437194e07f0418e86211c48cf87fe8d969
upstream_commits:
  - ef68d2faa4e23bdad40c700937eccfa6e9b78306  # T-P5-251 semidefinite normal metric/range bridge
  - 3e31954f21aa78b31754e314e8ded0b27922cc38  # T-P5-250 thick affine tube equality multiplier
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_source_slice_transversality_gate; add_partial_to_euclidean_tube_bridge; add_zero_radius_source_slice_dispatch
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional PSD algebra; residual-image quotient coercivity; exact rational counterexamples; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-252 — Source-slice coercivity for a singular residual metric

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-251 proved that a singular normal metric `W >= 0` defines a genuine
partial tube, and that at zero radius one may conclude only

`W C xi = 0`,

not ambiently `C xi = 0`.

This child closes the missing mathematical distinction between **ambient
singularity** and **singularity actually seen by the source slice**.

If the source residual directions occupy a linear image `range(D)` and

**`range(D) ∩ ker(W) = {0}`,**

then `W` is automatically coercive on exactly those residual directions even
when `W` is singular on the ambient residual space. Equivalently there exists a
strict scalar gap `gamma>0` such that

**`D^T W D >= gamma D^T D`.**

This gives a division-free radius conversion

**`gamma ||C xi||^2 <= (C xi)^T W (C xi) <= eta^2`**

on an affine source slice through an exact residual-zero reference. In
particular, at `eta=0`, the partial equality upgrades to the exact equality
`C xi=0` **on that source slice**.

The result is exact finite-dimensional algebra. It does not identify an actual
P5 `C,W,N,xi0`, does not prove tube/trajectory coverage, and does not replace
the independent T-P5-251 multiplier range gate `range(Y) subset range(W)`.

---

# Part I — residual-image transversality

## 1. Setup

Let

- `W=W^T >= 0` be an `r x r` residual metric;
- `D : R^m -> R^r` be the linear residual-direction map;
- `R := range(D)`;
- `B := D^T W D`;
- `G := D^T D`.

`W` may be singular, and `D` need not be injective.

The source-relevant condition is

`R ∩ ker(W) = {0}`.

This is strictly weaker than `W>0` on the full residual space.

## 2. Lemma 1 — zero quadratic value for a PSD form

For every symmetric `W>=0`,

**`x^T W x = 0  <->  W x = 0`.**

One inverse-free proof is to use positivity of

`(x+t y)^T W (x+t y)`

for all real `t`. If `x^TWx=0`, a nonzero linear coefficient
`2 x^T W y` would make this quadratic negative for one sufficiently small sign
of `t`; hence `x^TWy=0` for every `y`, so `Wx=0`.

Therefore

`z^T B z = 0`

iff

`W D z = 0`.

Since `B>=0`, this also yields

**`ker(B) = ker(WD)`.**

Likewise `G>=0` and

**`ker(G)=ker(D)`.**

## 3. Theorem 1 — exact qualitative equivalences

The following are equivalent:

1. **residual-image transversality**

   `range(D) ∩ ker(W) = {0}`;

2. **kernel equality**

   `ker(D^T W D) = ker(D)`;

3. **composed-map kernel equality**

   `ker(WD)=ker(D)`;

4. **rank preservation**

   `rank(WD)=rank(D)`.

### Proof

`ker(D)` is always contained in `ker(WD)`.

If `range(D) ∩ ker(W)={0}` and `WDz=0`, then `Dz` lies both in
`range(D)` and in `ker(W)`, so `Dz=0`; hence the two kernels are equal.
Conversely, if the two kernels are equal and `r=Dz` belongs to `ker(W)`, then
`WDz=0`, whence `Dz=0` and therefore `r=0`.

Lemma 1 gives `ker(D^TWD)=ker(WD)`, proving the equivalence with item 2.
Finally, because `ker(D) subset ker(WD)`, equality of ranks is equivalent to
equality of nullities, hence to equality of the two kernels. QED.

### Why the rank statement is useful

For exact rational packets the condition can be checked by exact minors or a
rank certificate without ever constructing a floating nullspace. However the
rank statement is qualitative only; the next theorem gives the quantitative
packet that downstream tube consumers actually want.

---

# Part II — exact coercivity on the residual image

## 4. Theorem 2 — transversality iff a strict Gram gap exists

The following are equivalent:

(A) `range(D) ∩ ker(W) = {0}`;

(B) there exists `gamma>0` such that

**`D^T W D - gamma D^T D >= 0`.**

Equivalently, for every `z`,

**`gamma ||Dz||^2 <= (Dz)^T W (Dz)`.**

### Proof: (B) -> (A)

Let `r=Dz` lie in `ker(W)`. Then

`0 = r^TWr >= gamma ||r||^2`.

Since `gamma>0`, `r=0`.

### Proof: (A) -> (B)

If `range(D)={0}`, both Gram matrices vanish and any positive `gamma` works.

Otherwise consider the Euclidean unit sphere in the finite-dimensional space
`R=range(D)`. It is compact. The continuous function

`f(r)=r^TWr`

is strictly positive on that sphere by (A) and Lemma 1, so it has a positive
minimum `gamma_* > 0`. Therefore for every `r in R`,

`r^TWr >= gamma_* ||r||^2`.

Substitute `r=Dz` to obtain the Gram inequality. QED.

## 5. Rational certificate corollary

Assume `W,D` have rational entries and condition (A) holds. Then there exists a
**rational** `gamma>0` satisfying

`D^T W D - gamma D^T D >=0`.

Indeed choose any rational `0<gamma<gamma_*` from the proof above. Therefore a
producer does not need to serialize the exact smallest generalized eigenvalue.
It may simply provide:

- rational `D,W,gamma`;
- `gamma>0`;
- an exact PSD witness for
  `D^T W D - gamma D^T D` (LDL, matrix-SOS, principal-minor packet, or another
  accepted exact checker representation).

This packet is stronger operationally than a floating rank decision: it proves
both transversality and a usable radius-conversion constant.

## 6. Exact negative certificate when transversality fails

Failure also has a small exact witness. It is enough to exhibit `z` such that

`r:=Dz != 0`,

`W r = 0`.

Then `r` is a genuine source residual direction invisible to the partial
metric, and no `gamma>0` Gram gap can exist.

This is a mathematical obstruction to the **source-slice exact-equality
upgrade**, not automatically to direct tube safety for some separate target.

---

# Part III — affine source slices

## 7. Source-slice model

Let an affine source slice be parameterized by

**`xi = xi0 + N z`.**

Assume the reference is an actual exact-image point:

**`C xi0 = 0`.**

Define

**`D := C N`.**

Then every residual on the slice is exactly

`C xi = D z`.

No injectivity of `N` or `D` is required.

## 8. Theorem 3 — partial tube to Euclidean tube

Suppose a rational/real gap `gamma>0` satisfies

`D^T W D - gamma D^T D >=0`.

Then for every point on the affine source slice,

**`gamma ||C xi||^2 <= (C xi)^T W (C xi)`.**

Hence membership in the partial tube

`(C xi)^T W(C xi) <= eta^2`

implies the division-free Euclidean residual bound

**`gamma ||C xi||^2 <= eta^2`.**

If one wants a conventional radius and division is allowed, this is

`||C xi||^2 <= eta^2/gamma`.

### Proof

Write `xi=xi0+Nz`. Since `Cxi0=0`, `Cxi=Dz`. The claimed inequality is exactly

`z^T(D^TWD-gamma D^TD)z >=0`. QED.

## 9. Corollary — zero-radius partial equality becomes exact equality

Under the same source-slice hypotheses,

**`W C xi = 0  ->  C xi = 0`.**

Equivalently, on this source slice,

`(Cxi)^T W(Cxi)=0`

iff

`Cxi=0`.

Thus the T-P5-251 zero-radius dispatcher can safely route the singular metric
branch to exact `Cxi=0` **only after this source-slice coercivity packet is
present**.

This does not make `W` positive definite ambiently. It says only that the
source residual image avoids the invisible normal directions.

---

# Part IV — equality-constrained source coordinates

## 10. Source directions given by an equality matrix

Often the actual source slice is presented as

`A (xi-xi0)=0`

rather than directly by `N`.

If a producer provides a complete basis/parameterization `N` with

**`range(N)=ker(A)`,**

then the relevant residual-direction map is still simply

`D=C N`.

The exact certificate is therefore

**`(CN)^T W (CN) - gamma (CN)^T(CN) >=0`, `gamma>0`.**

The completeness statement `range(N)=ker(A)` is a separate typed dependency;
checking the Gram gap for an incomplete subset of source directions is not a
coverage proof.

A basis-free rank slogan is

`rank(W C|_{ker A}) = rank(C|_{ker A})`,

but for a checker the explicit `N` plus Gram-gap packet is preferable because
it simultaneously carries the quantitative reserve.

---

# Part V — counterexamples fixing the boundaries

## 11. Regression A — ambiently singular but source-safe

Take

`W = [[1,0],[0,0]]`,

`D = [[1],[1]]`.

Then `W` is singular, but

`D^T W D = [1]`,

`D^T D = [2]`.

Therefore `gamma=1/2` gives equality

`D^TWD - gamma D^TD = 0`.

The source residual line `span((1,1))` intersects `ker(W)=span((0,1))` only at
zero. Hence a globally singular metric is a perfectly valid exact normal metric
on this source residual image.

Any dispatcher requiring ambient `W>0` would reject this valid case.

## 12. Regression B — a real invisible source direction

Take the same

`W = [[1,0],[0,0]]`,

but

`D = [[0],[1]]`.

Then `Dz=(0,z)` lies in `ker(W)` for every `z`, and

`D^TWD=0`, `D^TD=1`.

No positive `gamma` is possible. At zero partial-tube radius the metric accepts
all residuals `(0,z)`, so `WCxi=0` cannot imply `Cxi=0`.

## 13. Regression C — the residual-zero reference is essential

Direction transversality alone does not control an **affine offset**.

Let

`W = [[1,0],[0,0]]`,

`D=0`,

and let the affine residual be the constant

`r0=(0,1)`.

The directional condition `range(D)∩ker(W)={0}` holds vacuously, and the Gram
gap also holds vacuously for any `gamma>0`; nevertheless

`W r0=0` while `r0 !=0`.

Therefore Theorem 3 genuinely needs an exact residual-zero reference
`Cxi0=0` (or a more general separate affine-offset exclusion certificate).
One may not infer exact equality from tangent transversality alone.

## 14. Regression D — do not conflate two different range gates

The condition proved here is

`range(CN) ∩ ker(W) = {0}`.

T-P5-251's equality-multiplier reserve reuse instead requires

`range(Y) subset range(W)`.

Neither condition implies the other in general. The first says the **physical
source residual directions** do not disappear under `W`; the second says a
chosen **dual/equality multiplier block** can be absorbed by the semidefinite
metric reserve. They must remain separate typed fields.

---

# Part VI — source-facing exact packet

## 15. Minimal producer packet

To upgrade a singular zero-radius normal metric to exact equality on an affine
source slice, a producer should provide:

1. `same_source_key / same_cell_key / same_tube_key`;
2. exact `C,W,N,xi0`;
3. `W=W^T >=0`;
4. exact-center identity `C xi0=0`;
5. the source-direction coverage identity/contract for
   `xi=xi0+Nz` (or `range(N)=ker(A)` when equality constrained);
6. `D=CN`;
7. rational `gamma>0`;
8. exact PSD witness
   `D^TWD - gamma D^TD >=0`.

Then a checker can consume only matrix multiplication, scalar positivity and a
PSD witness. No pseudoinverse, square root, numerical eigenvector, or floating
rank tolerance is mathematically necessary.

For `eta>0`, the same packet yields the quantitative residual radius

`gamma ||Cxi||^2 <= eta^2`.

For `eta=0`, it yields exact `Cxi=0`.

## 16. Failure packet

If coercivity fails, an exact obstruction packet may instead contain

`z`, `r=Dz`, `r!=0`, `Wr=0`.

That obstruction should be recorded as

`SOURCE_SLICE_PARTIAL_METRIC_NOT_COERCIVE`

or equivalent. It should **not** be renamed as a proof that the original P5
Lyapunov target is false: T-P5-251's direct one-tube S-lemma may still exploit
other target curvature.

---

# Part VII — suggested Lean decomposition

## 17. Small algebraic leaves

Suggested first leaves:

1. `psd_quadratic_eq_zero_iff_mulVec_eq_zero`

   For real symmetric PSD `W`,
   `x^T W x = 0 <-> W*x=0`.

2. `residualImage_transverse_iff_gramKernel_eq`

   `range(D) ∩ ker(W)={0}` iff
   `ker(D^T W D)=ker(D)`.

3. `residualImage_transverse_iff_rank_preserved`

   `range(D) ∩ ker(W)={0}` iff `rank(WD)=rank(D)`.

4. `residualImage_coercive_of_gramGap`

   From `gamma>0` and
   `D^TWD-gamma D^TD>=0`, conclude
   `gamma*||Dz||^2 <= (Dz)^TW(Dz)`.

5. `partialTube_onAffineSlice_to_euclideanTube`

   From `Cxi0=0`, `xi=xi0+Nz`, `D=CN`, the Gram gap and partial-tube
   membership, conclude `gamma||Cxi||^2<=eta^2`.

6. `partialEquality_onAffineSlice_imp_exactEquality`

   Same hypotheses plus `WCxi=0`, conclude `Cxi=0`.

The compactness direction

`transversality -> exists gamma>0`

can be formalized later. The first source adapter does not need it if the
producer directly supplies rational `gamma` and the exact PSD witness.

## 18. Why the producer-supplied gap is the better first interface

A theorem that merely proves existence of some real minimum is less useful to
the exact checker. A concrete rational `gamma`:

- avoids choosing an eigenvalue representation;
- gives a radius conversion immediately;
- survives denominator clearing;
- can be independently checked by the existing rational PSD machinery;
- naturally exposes a strict reserve for later perturbation arguments.

---

# Part VIII — interaction with T-P5-251 and the next seam

## 19. What this closes mathematically

T-P5-251's statement

`eta=0, W>=0 => WCxi=0`

can now be refined to:

- if no source-image coercivity is known, retain the partial equality;
- if the exact affine source slice carries the Gram gap above, upgrade to
  `Cxi=0` on that slice.

Thus **ambient singularity is not itself the blocker**. The blocker is whether
actual residual directions enter `ker(W)`.

## 20. What remains independent

This child does not close:

- the T-P5-251 dual multiplier range gate `range(Y) subset range(W)`;
- actual P5 identification of `C,W,N,xi0`;
- proof that the source is truly affine over the whole consumed tube;
- nonlinear chart remainder/curvature;
- trajectory, stencil, segment, flowpipe or continuation coverage;
- Float64/interval rank semantics;
- Lean/kernel verification;
- independent validation by `封不觉`;
- admission, registry, P5/P8/M4 parent closure.

## 21. Next distinct mathematical seam

The natural continuation is **stability of source-image transversality under a
nonlinear residual chart**.

Suppose the true source residual is

`r(z)=Dz+n(z)`

rather than exactly `Dz`. The current Gram gap gives a strict reserve on
`range(D)`, but a nonlinear remainder may rotate residuals toward `ker(W)`.
The next useful child should derive a quantitative radius-dependent condition
from:

- `D^TWD >= gamma D^TD`;
- an upper metric bound such as `W <= L I` on the relevant residual span;
- a relative or second-order remainder estimate for `n(z)`.

The goal should be an explicit degraded gap

`r(z)^T W r(z) >= gamma_eff ||r(z)||^2`

on a certified radius, preferably with a rational Young/PSD packet and no
square roots. This is the correct bridge from the affine source-slice result
here to the nonlinear-chart defect machinery of T-P5-248.

---

## 22. Non-claims

This review does not establish actual P5 source identity, source/tube coverage,
Float64 semantics, a Lean/kernel receipt, independent verification, admission
or registry eligibility. Status remains

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**