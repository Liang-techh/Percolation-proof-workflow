---
kind: review_result
review_id: review-GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT-guyuefangyuan-20260908T2230Z
task_id: GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT
source_agent: 古月方源
created_at: 2026-09-08T22:30:00Z
claim_commit: b121ba94052242ac03e5453d634069f8fef9bef9
inspected_commit: 2c6b41192b1b1800e96c963321e8b102a8e02884
status: BLOCKED_WITH_EXACT_SOURCE_DIMENSION_OBSTRUCTION
integration_status: pending
admission_label: pending
proof_status: SAME_CONFIGURATION_PACKET_NOT_FOUND
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
registry_mutation: false
state_mutation: false
---

# GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT — same-configuration source join

## 1. Result

The requested same-configuration actual packet is **not currently bindable from the inspected repository artifacts**.
The obstruction is sharper than “some source file is missing”:

1. the signed-affine Schur consumer is a **three-dimensional** defect chart for
   `C=(4,5,6)`, with `d in R^3` and the dense metric `H=M0_CC^-1`;
2. the closest actual/preconditioned source-row packet currently exposes only
   rows 4 and 5, and its weighted reconstruction is explicitly the
   **two-dimensional** principal block `B=(4,5)`;
3. those two observed/reconstructed directions cannot, even in principle, imply
   a finite cap on the three-dimensional positive-definite quadratic defect
   `D=d^T H d` unless a third independent source constraint is supplied.

Therefore the present source material cannot be spliced into

```text
y = X z_A,
d = A y + b,
H = M0_CC^-1,
u = <ell,d>_H,
s = <ell+r0,d>_H,
D = d^T H d
```

under one actual source/configuration key.  This is a fail-closed source obstruction,
not a claim that no future actual packet can exist.

No receipt/provenance/admission audit was performed.  The newly landed generic Schur
Lean sidecar is source-independent and does not change this result.

## 2. The two interfaces do not have the same physical dimension

The signed-affine chart review fixes the intended Route-B candidate to
`C=(4,5,6)` and requires a fixed rational `A : R^6 -> R^3`, offset `b in R^3`,
SPD `H in R^(3x3)`, and

```text
d=A y+b,
u=ell^T H d,
s=(ell+r0)^T H d,
D=d^T H d.
```

Its helper is deliberately `3 x 6` and computes `u`, `s`, and `D` separately.
It also states that actual `J_d/b`, signed `y=X z_A`, and the same-source metric
binding are missing.

By contrast, the closest source-row recovery review derives its weighted packet for

```text
B=(4,5), E=(1,2,3),
(e_A)_B = D2 (b_meas + m_B) + c + delta_e,
```

where `D2=diag(beta,kappa)` is 2 x 2.  The same review explicitly records that the
inspected preconditioned payloads output only rows 4 and 5, not a complete six-row
actual packet.  Its principal residual equation is consequently two-dimensional:

```text
S u = f0 + delta_e,     S in R^(2x2), u=ahat_B in R^2.
```

This object is useful for the principal `(4,5)` lane, but it is not the `d in R^3`
required by the block456 signed-affine chart.  In particular, physical joint 6 and
preconditioned row 6 are not interchangeable objects.

## 3. Exact mathematical obstruction: two signed observations cannot cap a 3D SPD energy

The following lemma is the key source-dimension obstruction.

### Lemma — no SPD quadratic cap from a rank-deficient observation

Let `H` be positive definite on `R^3`.  Let `L : R^3 -> R^m` be linear with
`rank(L)<3`.  Then for every finite `C>=0` there exists `d in R^3` such that

```text
L d = 0,
d^T H d > C.
```

**Proof.** Since `rank(L)<3`, choose nonzero `v in ker L`.  Positive definiteness gives
`q=v^T H v>0`.  Put `d=t v`.  Then `L d=0` for every real `t`, while
`d^T H d=t^2 q`.  Choosing `t^2 q>C` proves the claim.  QED.

Two important specializations are immediate.

- If the available actual source information determines only the first two defect
  coordinates, take `L(d)=(d_4,d_5)`.  The unobserved block456 direction supplies a
  nonzero kernel vector.
- If one tries to use only the two Schur projections
  `u=ell^T H d` and `s=(ell+r0)^T H d`, their joint observation map has rank at most 2.
  Hence those two scalars can never imply a finite `D=d^T H d` cap for an arbitrary
  three-dimensional defect.  This proves, structurally, why `D` must remain a
  separately supplied output.

The familiar concrete control is `H=I`, `ell=e1`, `r0=e2`, `d=t e3`:
`u=s=0` for every `t` but `D=t^2` is unbounded.  This is not a robot-state
counterexample; it is an exact impossibility theorem for the proposed information
flow.

## 4. The block456 metric candidate exists only on the symbolic/source-reification lane

The block456 source-reification review reconstructs the exact nominal C-block

```text
KQ =
[[350003/3000000, 0,               1/60],
 [0,               200739/4000000, 0],
 [1/60,            0,               50003/3000000]]
```

and proposes the exact rational inverse

```text
HQ =
[[ 50003000000/5000400003, 0,                    -50000000000/5000400003],
 [ 0,                         4000000/200739,       0],
 [-50000000000/5000400003,   0,                    350003000000/5000400003]].
```

That review is careful that `H=M0_CC^-1` is a proposed exact inverse of the
symbolically reconstructed nominal block, not an already deployed Julia/runtime
`inv` witness.  Thus the current repository contains useful exact `H` mathematics,
but not a same-key actual `y/A/b/H` packet.

This also blocks a tempting splice: the two-row source reconstruction cannot simply
borrow this 3 x 3 `HQ`.  The quadratic form would then charge a third defect direction
for which the actual source packet supplies no independent bound.

## 5. Why the existing `y=X z_A` material is still insufficient

The source-rows weighted review defines the correct analytic residual semantics

```text
z_A = M_A^mu * ahat - F_A,
y_A = X z_A,
```

but finds that the inspected preconditioned builder exports only rows 4 and 5 and
omits twenty nonzero q/dq controller coefficients across those two rows.  Its exact
correction is a signed omission term `m_i`; therefore the payload row cannot be
silently identified with the corresponding component of `y_A`.

Even if that two-row omission were corrected, the present task needs a six-dimensional
`y` box or an equivalent source-complete image sufficient for the 3 x 6 map `A`.
No inspected artifact supplies both:

```text
actual signed y=X z_A enclosure on every A-active direction,
d=J_d z_A+b (equivalently d=A y+b),
```

under the same configuration/reference/runtime semantics.

A full six-row actual packet would solve this source-information problem directly.
An alternative is a direct three-dimensional actual `d` packet together with a proof
that it equals the intended block456 defect and a separate same-domain quadratic cap.
A two-row principal packet does not.

## 6. Minimum packet that would close this child

One immutable record should freeze a single `source_key/configuration_key/domain_key`
and provide, without cross-payload substitution:

```text
z_A identity and actual/refinement semantics,
X and y=X z_A,
a six-dimensional y enclosure on every A-active coordinate,
J_d and b with d=J_d z_A+b,
A with A X = J_d (or A=J_d X^-1 plus the inverse witness),
C=(4,5,6) coordinate/order/unit witness,
M0_CC and H with exact left/right inverse witness,
ell and r0 in the same H-coordinate convention,
independent u interval,
independent s interval,
independent D cap,
and the common box/domain key consumed by all three outputs.
```

The last three should be regenerated from the same packet.  In particular, `D` may
be computed by the exact affine-box quadratic vertex theorem once the actual rational
`A,b,H` and legal `y` box are available, but it may not be reconstructed from `u,s`.

If the intended physical route instead switches to `B=(4,5)`, it needs a separately
stated 2D theorem and a matching 2 x 2 metric/source chart.  That would be a statement
change, not a completion of the present block456 packet.

## 7. Suggested Lean leaf

The smallest new theorem worth formalizing is source-independent and directly guards
against an invalid future adapter:

```lean
-- schematic statement
 theorem no_uniform_pd_energy_cap_of_nontrivial_kernel
   {n m : Nat}
   (H : Matrix (Fin n) (Fin n) Real)
   (L : Matrix (Fin m) (Fin n) Real)
   (hpd : PositiveDefinite H)
   (v : Fin n -> Real)
   (hv : v != 0)
   (hker : L *ᵥ v = 0) :
   forall C : Real, exists d : Fin n -> Real,
     L *ᵥ d = 0 /\ C < dot d (H *ᵥ d)
```

The proof is just `d=t v` plus positive definiteness.  A specialized `n=3,m=2`
corollary can be used as a typed gate: a rank-deficient actual observation packet may
never be admitted as an independent 3D `D` producer.

## 8. Status

`GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT` is resolved for this round as
`BLOCKED_WITH_EXACT_SOURCE_DIMENSION_OBSTRUCTION`.

The mathematical helper remains valid; the obstruction is the missing same-key
actual source information.  No source/coverage/admission/registry claim is made, and
no result of the synthetic Fraction self-test is used as runtime evidence.
