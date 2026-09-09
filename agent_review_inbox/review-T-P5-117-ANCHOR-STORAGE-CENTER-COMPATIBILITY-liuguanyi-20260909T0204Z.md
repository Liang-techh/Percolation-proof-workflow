---
kind: review_result
review_id: review-T-P5-117-anchor-storage-center-compatibility-liuguanyi-20260909T0204Z
task_id: T-P5-117-ANCHOR-STORAGE-CENTER-COMPATIBILITY
reviewer: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T02:04:00Z
claim_commit: 1ddc23e313ac234a54de3ace26e94fa5059aa9bd
inspected_commit: 75e7cb34f7ec2cdb5803cf7a535163756af7eb5d
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-112-SAME-CELL-GRAPH-ANCHOR-BUDGET-guyuefangyuan-20260909T0030Z.md
    commit: 3072f9b62a333f96448defd626a67039adb50168
  - path: agent_review_inbox/review-T-P5-116-homogeneous-anchor-small-gain-honglianmozun-20260909T0158Z.md
    commit: 75e7cb34f7ec2cdb5803cf7a535163756af7eb5d
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional quadratic/integral derivation only
exit_code: n/a
---

# T-P5-117 — anchor displacement / Lyapunov storage center compatibility

## 0. Bottleneck closed by this child

T-P5-116 turns the homogeneous second-jet packet into a no-additive-floor Lyapunov small-gain theorem, but it requires the same storage to control the anchor displacement:

`m Q_Z(delta) <= V`, with `m>0`.

That premise is not bookkeeping.  It links three independently typed objects:

1. the state/error coordinates used by the Lyapunov storage;
2. the source coordinates in which the affine anchor displacement `delta` is measured;
3. the actual anchor center/reference identity.

This review proves the smallest inverse-free bridge for that premise, gives an exact semidefinite kernel criterion, and shows that a center mismatch destroys homogeneous absorption at the zero-storage state.  It also gives a nonlinear centered-anchor transport lemma for state-dependent anchor maps.

No source equality, actual coefficient packet, whole-domain coverage, Lean receipt, admission, or registry promotion is claimed.

---

## 1. Exact affine displacement-to-storage theorem

Let `E` be the Lyapunov error space and `Zs` the anchor-displacement space.  Let

`V(e) = (1/2) e^T P e`,

`Q_Z(y) = y^T Z y`,

with symmetric PSD matrices `P,Z`.  Suppose the source/normalization layer proves that the anchor displacement is **centered affine-linear** in the Lyapunov error:

`delta(e) = L e`.

Let `m>=0`.  If the exact quadratic-form certificate

**(1.1)** `P - 2 m L^T Z L >= 0`

holds, then for every `e`

**(1.2)** `m Q_Z(delta(e)) <= V(e)`.

Proof: evaluate (1.1) on `e`:

`0 <= e^T(P-2mL^TZL)e = 2V(e)-2mQ_Z(Le)`.

This is exactly the T-P5-116 comparator.  The trusted checker needs only matrix multiplication, transpose, rational scalar multiplication and a PSD witness; it does not need `P^{-1}`, `Z^{1/2}`, a generalized eigenvalue, a singular value, or a square root.

### Source-friendly rational form

If `P,Z,L,m` are rational, a producer may propose any rational `m>0` and certify (1.1) by exact LDL/principal-minor/other accepted PSD machinery.  The theorem does not require the checker to compute an optimal `m`.

For a fixed cell anchor equal to the Lyapunov center, `L` is often just a coordinate extraction/change-of-variables map.  For a centered affine anchor map

`A(e)=Pi e`,

with displacement `delta=e-A(e)`, use

`L=I-Pi`.

Thus projection/restriction anchors need no new analytic argument: only the exact typed map `L` and the congruence matrix in (1.1).

---

## 2. Semidefinite storage: exact kernel criterion

T-P5-116 correctly notes that a semidefinite storage may fail to control anchor displacement.  For a linear displacement map this has a sharp finite-dimensional criterion.

Set

`S = L^T Z L >= 0`.

Then the following are equivalent:

1. there exists a real `m>0` such that `2m S <= P`;
2. `ker(P) subset ker(S)`;
3. every zero-storage direction is invisible to the displacement metric:
   `e^T P e = 0 -> Q_Z(L e)=0`.

### Necessity

If `2mS<=P` and `e in ker(P)`, then

`0 <= 2m e^T S e <= e^T P e = 0`.

Hence `e^TSe=0`; because `S` is PSD, this implies `Se=0`.

### Sufficiency

Let `K=ker(P)`.  The kernel assumption implies `S` also vanishes on `K`; for PSD `S`, all cross terms with `K` vanish as well.  Restrict both forms to any finite-dimensional complement of `K`.  There `P` is positive definite, so the continuous ratio

`e^T S e / e^T P e`

on the `P`-unit sphere has a finite maximum `C`.  Therefore `S<=C P` on the complement and hence on all of `E`.  Any `0<m<=1/(2C)` gives `2mS<=P` (if `S=0`, any positive `m` works).

For rational source data, once one positive real margin exists, a smaller positive rational `m` may be chosen; the trusted side still checks the direct PSD inequality (1.1), not the compactness argument.

### Minimal obstruction

Take

`P=diag(1,0)`, `Z=I`, `L=I`.

Then `V(x,y)=x^2/2`, while `Q_Z(delta)=x^2+y^2`.  Along `(0,1)`, storage is zero but displacement energy is one.  No `m>0` can satisfy the T-P5-116 premise.  This is not repaired by positivity of an unrelated metric or by shrinking a numerical cell unless the offending kernel direction is actually removed from the admissible state space.

---

## 3. Center compatibility is mathematically necessary

Now allow an affine bias between the storage center and the anchor center:

**(3.1)** `delta(e)=L e + b`.

Suppose a homogeneous comparator

**(3.2)** `m Q_Z(delta(e)) <= V(e)`

with `m>0` is claimed on any set containing the zero-storage state `e=0`.

Evaluating at `e=0` gives

`m Q_Z(b) <= 0`.

Since `Q_Z>=0`, necessarily

**(3.3)** `Q_Z(b)=0`.

If `Z` is positive definite, this forces

**(3.4)** `b=0`.

Therefore a nonzero anchor/reference offset cannot be hidden inside the homogeneous T-P5-116 lane.  The source interface must either prove that the anchor fixes the storage center, or explicitly route the center bias through an additive/mixed defect budget.

### Fixed-anchor specialization

Let the physical/source coordinate be `z`, Lyapunov center `z_ref`, and cell/graph anchor `z_a`.  Write `e=z-z_ref`.  Then

`delta=z-z_a = e + (z_ref-z_a)`.

Thus `L=I` and `b=z_ref-z_a`.  If `Q_Z` is SPD, a homogeneous comparator valid at `z=z_ref` is possible only if

**`z_a = z_ref`.**

This is a concrete cross-layer key constraint: a `cellAnchorKey` and a `storageCenterKey` may not be silently treated as interchangeable.

### Centered affine anchor-map specialization

For an affine anchor map

`A(e)=Pi e + a0`,

with displacement `delta=e-A(e)`, one has

`L=I-Pi`, `b=-a0`.

The homogeneous lane therefore requires `Q_Z(a0)=0`; with SPD `Z`, it requires `a0=0`.  Once this center identity is established, (1.1) controls the remaining linear displacement exactly.

---

## 4. Nonlinear centered-anchor transport lemma

The affine theorem is enough for many fixed-cell/reference consumers, but a state-dependent anchor map can still be handled without inverse metrics.

Let `delta : E -> Zs` be `C^1` on every straight segment from the storage center `0` to the admissible state `e`, and assume

**(4.1)** `delta(0)=0`.

Suppose there is `kappa>=0` such that on each such segment, for every tangent vector `v`,

**(4.2)** `Q_Z(D delta(x) v) <= kappa * v^T P v`.

Then the fundamental theorem of calculus gives

`delta(e) = integral_0^1 D delta(s e) e ds`.

Quadratic Jensen on the unit interval yields

`Q_Z(delta(e)) <= integral_0^1 Q_Z(Ddelta(se)e) ds`
`                <= kappa * e^T P e`
`                = 2 kappa V(e)`.

Hence any proposed `m>=0` satisfying the root-free scalar gate

**(4.3)** `2 m kappa <= 1`

obeys

**(4.4)** `m Q_Z(delta(e)) <= V(e)`.

This gives a clean nonlinear source-to-math adapter:

- prove exact center fixing `delta(0)=0`;
- prove same-segment domain coverage;
- certify a directional Jacobian metric bound (4.2);
- check only `2m kappa<=1` downstream.

A matrix producer may establish (4.2) pointwise by

`kappa P - Ddelta(x)^T Z Ddelta(x) >= 0`.

Again, no inverse, square root or eigenvalue is required by the theorem consumer.

### Why segment coverage is essential

The integral identity traverses `s e`, `0<=s<=1`.  A derivative bound only at the endpoint or only at the anchor does not imply (4.4).  This is the same physical-segment discipline already exposed by T-P5-112 for the second implicit jet.

---

## 5. Exact interface into T-P5-116

T-P5-116 needs the field `m` only through

`m Q_Z(delta) <= V`

and then checks, for target retained margins, the square-only small-gain gate

`h R <= 16 gamma d m^2 alpha theta`.

This review shows that the source does not need to export an opaque spectral constant `m`.  A minimal centered affine packet is:

1. `storageKey` selecting the exact quadratic storage `P` and its center;
2. `anchorKey` selecting the exact anchor and displacement coordinates;
3. exact center identity / bias-null statement;
4. exact linear displacement map `L` from storage error to `delta`;
5. rational `m>0`;
6. PSD witness for `P - 2m L^T Z L >=0`.

For a nonlinear anchor, replace items 4 and 6 by the same-segment derivative packet `(Ddelta,kappa)` and the two gates (4.2)-(4.3).

The intended ordering is important:

**first bind centers and coordinates, then prove the comparator, then invoke T-P5-116.**

A numerical norm bound that does not identify which center generated `e` and which anchor generated `delta` is not a valid homogeneous small-gain witness.

---

## 6. Bias fallback boundary

If `Q_Z(b)>0`, Section 3 proves that no positive homogeneous comparator can hold at the zero-storage state.  One can still use the elementary PSD quadratic estimate

`Q_Z(L e+b) <= 2 Q_Z(L e) + 2 Q_Z(b)`.

Thus, if the centered part satisfies `m Q_Z(Le)<=V` and a source packet gives `Q_Z(b)<=B`, then

**(6.1)** `m Q_Z(delta) <= 2V + 2mB`.

This is an **affine/additive** comparator, not T-P5-116's homogeneous premise.  Feeding it into the second-jet estimate necessarily leaves a nonzero term at `V=0` whenever `B>0`; that term belongs in the T-P5-113-style additive disturbance / ultimate-bound lane (or in a separately proved signed cancellation), not in a claimed zero-floor contraction theorem.

So the mathematical fork is exact:

- center-compatible / bias-null -> homogeneous T-P5-116 lane;
- non-null center bias -> additive or mixed lane.

No amount of retuning `alpha,theta,R` turns a genuine nonzero `Q_Z(b)` into a homogeneous storage comparator at `V=0`.

---

## 7. Minimal theorem statements for formalization

Suggested leaves, source-independent first:

```lean
-- Pure finite-dimensional congruence leaf.
theorem anchorDisplacement_le_storage_of_psd
    (hpsd : 0 <= P - 2*m • (L.transpose * Z * L)) :
    m * QZ (L e) <= (1/2) * QP e

-- Structural semidefinite criterion.
theorem exists_anchor_storage_gain_iff_kernel
    : (Exists m > 0, 2*m • S <= P) <-> ker P <= ker S

-- Center obstruction.
theorem homogeneous_anchor_gain_forces_bias_null
    (hgain : forall e in U, m * QZ (L e + b) <= V e)
    (h0 : 0 in U) (hm : 0 < m) :
    QZ b = 0

-- SPD corollary.
theorem homogeneous_anchor_gain_forces_same_center
    (hZpd : PositiveDefinite Z) ... : b = 0

-- Nonlinear centered transport.
theorem nonlinear_anchor_displacement_le_storage
    (hcenter : delta 0 = 0)
    (hJac : forall x onSegment 0 e, QZ (Ddelta x v) <= kappa * QP v)
    (hscalar : 2*m*kappa <= 1) :
    m * QZ (delta e) <= V e
```

For Lean, the direct PSD implication and bias-null theorem are the smallest/highest-value leaves.  The kernel equivalence and integral transport can be layered later without blocking consumption of rational affine packets.

---

## 8. Open boundaries / non-claims

This review is **CONDITIONAL_PASS / pending mathematical-interface child** only.

Still open:

- actual source identity of the P5 `delta` used by the second-jet packet;
- exact `storageKey` / storage center and `anchorKey` binding;
- whether the deployed displacement map is affine, projected, or nonlinear;
- actual rational `P,Z,L,m` and a same-source PSD witness;
- if nonlinear, same-segment coverage and a real derivative metric bound `kappa`;
- T-P5-112 second-jet source data `D2M,D2R`, lower gain and whole-segment coverage;
- Float64/FD/controller/runtime semantics, P8 flowpipe, Lean/kernel, independent verifier `封不觉`, admission and registry.

The mathematical contribution is the exact center-compatibility criterion and inverse-free comparator contract needed to make T-P5-116's homogeneous small-gain premise meaningful rather than an untyped scalar assumption.
