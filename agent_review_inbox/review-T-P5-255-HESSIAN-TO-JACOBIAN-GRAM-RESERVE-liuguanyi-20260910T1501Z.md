---
kind: review_result
review_id: review-T-P5-255-hessian-to-jacobian-gram-reserve-liuguanyi-20260910T1501Z
task_id: T-P5-255-HESSIAN-TO-JACOBIAN-GRAM-RESERVE
reviewer: 柳冠一
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T15:01:00Z
claim_commit: 23eaa6e1dc7e550cdbc811b8585e1e3f4841b64b
inspected_commit: 90b760d4dd193c1cb2d752956fabd0e65cd55090
upstream_commits:
  - 598db594c600e1999d4ddf12cb0fb23df4ffbd70  # T-P5-254 shared-quotient Jacobian leakage certificate
  - ced7eda6a74e19487f9d5f7be60bc4610cb28c97  # T-P5-253 nonlinear source transversality reserve
  - a25de2d6e01b16133af9dc40d46efcfef6731ef8  # T-P5-247 affine GL(n) chart covariance
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_raywise_mixed_hessian_gram_lemma; add_radial_second_order_leakage_lemma; add_singular_D_kernel_dispatch; add_fraction_free_hessian_packet
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact finite-dimensional calculus/PSD algebra; rational sharp examples; no provenance/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-255 — Hessian-to-Jacobian Gram reserve

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-254 reduced producer-side nonlinear leakage to the pointwise Jacobian Gram
obligation

`J_b(theta)^T E^T E J_b(theta) <= delta D^T D`.

Its remaining seam was to derive such a packet from the more common source data

`b(0)=0`, `J_b(0)=0`, plus a second-derivative bound on a source ellipsoid,

without whitening away the anisotropy of `D^T D`.

This child closes that implication.  The main result is stronger than a generic
ambient Hessian norm estimate: a **raywise mixed Hessian Gram bound** with
constant `kappa` gives

**`J_b(theta)^T E^T E J_b(theta)
   <= kappa (theta^T M theta) D^T D`,**

hence on `theta^T M theta <= R`,

**`delta_J(R)=kappa R`.**

Moreover, integrating the second-order Taylor remainder directly yields the
strictly sharper endpoint leakage packet

**`||E b(theta)||^2
   <= (kappa/4)(theta^T M theta)||D theta||^2`,**

so the T-P5-253 relative-leakage constant can be taken as

**`delta_b(R)=kappa R/4`.**

The constants `1` and `1/4` are sharp already in one dimension.

A second theorem shows that the direct endpoint packet needs only a weaker
**radial Hessian** inequality.  This matters when `D` is singular: the mixed
Jacobian route forces every `ker(D)` direction to be killed by the transverse
Jacobian, while the endpoint relative-leakage inequality can remain true even
when that stronger kernel condition fails.  Thus failure of the mixed Hessian
packet is only a failure of this producer route, not automatically a physical
obstruction.

No actual P5 Hessian, source ellipsoid, same-key chart, cell/tube/trajectory
coverage, Float64/interval semantics, Lean receipt, independent verification,
admission, registry mutation, or parent closure is claimed.

---

# Part I — setup

## 1. Data

Let `Omega_R subset R^m` be star-shaped with respect to `0` and satisfy

`theta^T M theta <= R`

for all `theta in Omega_R`, where `M=M^T>=0` and `R>=0`.

Let

`b : Omega_R -> R^p`

be `C^2` on every radial segment used below.  Let

`E : R^p -> R^r`,

`D : R^m -> R^q`,

and define the quotient Gram matrix

**`G := D^T D >=0`.**

Only `E b` is physically charged as transverse leakage.  It is therefore enough
to assume

`E b(0)=0`, `E J_b(0)=0`.

The stronger source normalization `b(0)=0`, `J_b(0)=0` used by T-P5-254 is of
course sufficient.

Write the Hessian as the symmetric bilinear map

`H_b(x)[u,v] := D^2 b(x)[u,v]`.

---

# Part II — mixed Hessian to Jacobian Gram

## 2. Theorem 1 — raywise mixed Hessian domination

Assume there is `kappa>=0` such that for every `theta in Omega_R`, every
`s in [0,1]`, and every `v in R^m`,

**(Hmix)**

`||E H_b(s theta)[theta,v]||^2
 <= kappa (theta^T M theta) (v^T G v)`.

Then for every `theta in Omega_R`,

**(2.1)**

`J_b(theta)^T E^T E J_b(theta)
 <= kappa (theta^T M theta) G`

in PSD order.  Consequently,

**(2.2)**

`J_b(theta)^T E^T E J_b(theta)
 <= kappa R G`.

Thus T-P5-254 may consume

**`delta_J(R)=kappa R`.**

### Proof

Since `E J_b(0)=0`, the fundamental theorem of calculus along the radial
segment gives, for every `v`,

`E J_b(theta)v
 = integral_0^1 E H_b(s theta)[theta,v] ds`.

By Jensen/Cauchy-Schwarz on the unit interval,

`||E J_b(theta)v||^2
 <= integral_0^1 ||E H_b(s theta)[theta,v]||^2 ds`.

Apply (Hmix):

`||E J_b(theta)v||^2
 <= kappa (theta^T M theta)(v^T G v)`.

This is exactly the quadratic-form statement (2.1).  Bounding
`theta^T M theta` by `R` yields (2.2). QED.

## 3. Exact square-root-free producer form

For fixed `(s,theta)`, define the matrix `B(s,theta)` by

`B(s,theta)v := E H_b(s theta)[theta,v]`.

Then (Hmix) is **exactly equivalent** to the PSD condition

**(3.1)**

`kappa (theta^T M theta) G - B(s,theta)^T B(s,theta) >=0`.

No inverse, square root, singular vector, pseudoinverse, or whitening map appears.
For rational polynomial source data and rational `kappa,M,D,E,R`, (3.1) is a
rational matrix-polynomial nonnegativity obligation on the compact semialgebraic
set

`0<=s<=1`, `theta^T M theta<=R`.

How that source-domain nonnegativity is established (exact factorization, SOS,
rational interval subdivision, etc.) is independent of this mathematical child.
The important point is that the consumer contract itself is already
fraction-free.

---

# Part III — direct second-order endpoint reserve

## 4. Theorem 2 — sharper endpoint leakage from the same mixed packet

Under the assumptions of Theorem 1,

**(4.1)**

`||E b(theta)||^2
 <= (kappa/4)(theta^T M theta)(theta^T G theta)`.

Since `theta^T G theta=||D theta||^2`, on `Omega_R` this gives

**(4.2)**

`||E b(theta)||^2
 <= (kappa R/4)||D theta||^2`.

Hence the T-P5-253 leakage constant can be chosen as

**`delta_b(R)=kappa R/4`.**

### Proof

The second-order integral remainder is

`E b(theta)
 = integral_0^1 (1-s) E H_b(s theta)[theta,theta] ds`.

By (Hmix) with `v=theta`,

`||E H_b(s theta)[theta,theta]||
 <= sqrt(kappa)
    sqrt(theta^T M theta)
    sqrt(theta^T G theta)`.

Taking norms before integration and using

`integral_0^1 (1-s) ds = 1/2`

gives

`||E b(theta)||
 <= (sqrt(kappa)/2)
    sqrt(theta^T M theta)
    sqrt(theta^T G theta)`.

Squaring yields (4.1), then (4.2). QED.

### Immediate reserve gate

T-P5-253 uses the information-level gate

`L delta < gamma`.

The direct Hessian packet therefore gives the division-free sufficient gate

**(4.3)**

`L kappa R < 4 gamma`.

If one insists on routing through the uniform Jacobian packet first, the weaker
gate is `L kappa R < gamma`.  Thus the direct second-order route preserves a
factor four of reserve.

---

# Part IV — a weaker radial theorem

## 5. Theorem 3 — radial Hessian condition is enough for endpoint leakage

To prove only the T-P5-253 endpoint ratio, the full mixed condition is stronger
than necessary.  It suffices to assume, for every `theta in Omega_R` and
`s in [0,1]`,

**(Hrad)**

`||E H_b(s theta)[theta,theta]||^2
 <= kappa (theta^T M theta)(theta^T G theta)`.

Then the same proof as Theorem 2 gives (4.1)--(4.3).

This condition has the exact scalar polynomial form

**(5.1)**

`kappa (theta^T M theta)(theta^T G theta)
 - ||B(s,theta)theta||^2 >=0`.

It is strictly weaker than the matrix PSD condition (3.1), because it tests only
the physical radial pair `(theta,theta)` instead of every mixed second argument
`v`.

This gives a useful dispatcher:

1. if (Hmix) is available, obtain both the T-P5-254 Jacobian certificate and the
   sharper T-P5-253 endpoint certificate;
2. if only (Hrad) is available, bypass T-P5-254 and feed the endpoint ratio
   `delta=kappa R/4` directly to T-P5-253;
3. failure of (Hmix) does **not** imply failure of (Hrad), nor physical failure.

---

# Part V — singular quotient Gram and the real kernel boundary

## 6. Corollary — mixed packet forces quotient-kernel compatibility

Suppose `G=D^T D` is singular.  Under (Hmix), every `v in ker(D)` satisfies

**(6.1)**

`E H_b(s theta)[theta,v]=0`

for every relevant `(s,theta)`, because the right-hand side of (Hmix) is zero.
Integrating in `s` gives

**(6.2)**

`E J_b(theta)v=0`.

Equivalently,

**`ker(D) subset ker(E J_b(theta))`.**

This is also necessary for any finite Jacobian Gram bound

`J_b(theta)^T E^T E J_b(theta) <= delta D^T D`.

Therefore the Jacobian route has an exact kernel obstruction: nonlinear
transverse motion in a `D`-null source direction cannot be bounded by the
`D^T D` metric at derivative level.

## 7. But this is not an endpoint obstruction

The stronger kernel condition above is **not necessary** for the endpoint
relative-leakage inequality.

Take rational data

`theta=(x,y)`, `M=I`, `D=[1 0]`, `E=1`,

and

**`b(x,y)=x y`.**

Then

`H_b[u,v]=u_1 v_2+u_2 v_1`.

For the diagonal radial direction,

`H_b[theta,theta]=2xy`,

so

`|H_b[theta,theta]|^2=4x^2y^2
 <=4(x^2+y^2)x^2`.

Thus (Hrad) holds sharply with `kappa=4`.  On

`x^2+y^2<=R`,

Theorem 3 gives

`|b(x,y)|^2=x^2y^2 <= R x^2 = R||D theta||^2`,

which is sharp in the supremal sense.

However

`J_b(x,y)=[y,x]`.

For the kernel vector `v=e_2 in ker(D)`,

`J_b(x,y)v=x`,

which is nonzero whenever `x!=0`.  Hence no finite matrix inequality

`J_b^T J_b <= delta D^T D`

can hold on such points.

So a producer must not turn failure of the mixed/Jacobian packet into `FAIL`.
The direct radial second-order branch can still close the actual relative
leakage obligation.

---

# Part VI — sharpness

## 8. Sharp one-dimensional regression

Let

`m=p=q=r=1`, `M=D=E=1`,

and

`b(theta)=(a/2) theta^2`

with rational `a`.

Then `H_b=a`, so the optimal mixed Hessian constant is

`kappa=a^2`.

Also

`J_b(theta)=a theta`,

hence on `theta^2<=R`,

`J_b(theta)^2 <= a^2 R`

and equality occurs at `theta^2=R`.  Therefore the coefficient `1` in
`delta_J(R)=kappa R` is sharp.

Meanwhile

`b(theta)^2/(D theta)^2 = a^2 theta^2/4`,

whose maximum is `a^2 R/4`.  Therefore the factor `1/4` in
`delta_b(R)=kappa R/4` is also sharp.

There is no universal improvement of either constant under the stated
information.

---

# Part VII — coordinate covariance

## 9. Theorem 4 — exact GL(m) covariance

Let `theta=P z` with `P` invertible.  Define

`M_z=P^T M P`,

`D_z=D P`,

`G_z=D_z^T D_z=P^T G P`,

and `b_z(z)=b(Pz)`.

Then

`H_{b_z}(z)[x,v]=H_b(Pz)[Px,Pv]`.

Therefore (Hmix) with constant `kappa` in `theta` coordinates is equivalent to
(Hmix) with the **same `kappa`** in `z` coordinates; likewise for (Hrad).
The squared-radius scalar `R` is unchanged because

`z^T M_z z=(Pz)^T M(Pz)`.

Hence both

`delta_J(R)=kappa R`

and

`delta_b(R)=kappa R/4`

are chart-invariant quantities when the source metric and `D` are transported
together.  This is the second-derivative analogue of T-P5-247: exact chart
anisotropy should be transported, not charged as coefficient error.

For rational `P`, every transported Gram packet remains rational; no whitening
is required.

---

# Part VIII — minimal typed mathematical contract

## 10. Preferred mixed packet

A producer wishing to invoke T-P5-254 should provide, on one common source key:

- `M=M^T>=0`, `R>=0`, and a star-shaped source-domain witness
  `theta^T M theta<=R`;
- `D,E` and `G=D^TD`;
- `E b(0)=0`, `E J_b(0)=0`;
- rational `kappa>=0`;
- the raywise matrix inequality
  `kappa(theta^TMtheta)G-B(s,theta)^TB(s,theta)>=0`
  for `0<=s<=1` on the source domain.

The consumer may emit both

`delta_J=kappa R`

for T-P5-254 and the sharper

`delta_b=kappa R/4`

for a direct T-P5-253 route.

## 11. Radial-only fallback packet

If the matrix inequality is unavailable, it is enough for the endpoint route to
provide

`kappa(theta^TMtheta)(theta^TGtheta)-||B(s,theta)theta||^2>=0`.

Then emit only

`delta_b=kappa R/4`.

Do **not** manufacture a Jacobian Gram certificate from this weaker packet.

## 12. Singular-D dispatch

If `D` is rank deficient:

- mixed/Jacobian branch: require the implied kernel gate
  `E J_b(theta) ker(D)=0`; a concrete violation blocks this branch;
- radial endpoint branch: do not impose that stronger gate automatically;
- neither branch should use `pinv(D)` or a floating quotient basis.

---

# Part IX — boundaries and next seam

## 13. What this closes

This child closes the pure mathematical implication

`anisotropic second derivative bound`

`=> O(R) Jacobian Gram reserve`

`=> T-P5-254 relative-leakage producer packet`,

while also giving the sharper direct endpoint law

`second derivative => delta_b(R)=kappa R/4`.

It preserves the actual quotient anisotropy `D^TD`, exposes the exact
rank-deficient kernel boundary, and avoids all inverse/square-root machinery.

## 14. What remains independent

This review does not establish:

- an actual P5 formula for `b`, its Hessian, `D`, `E`, `M`, or `R`;
- a same-key source proof of (3.1) or (5.1);
- how source code obtains a rigorous rational/interval `kappa`;
- cell/tube/trajectory/flowpipe/stencil/continuation coverage;
- Float64/interval semantics;
- Lean/kernel compilation;
- independent verification by `封不觉`;
- admission, registry, or P5/P8/M4 parent closure.

## 15. Next distinct mathematical seam

The remaining source-facing question is now narrower: for the actual nonlinear
producer, derive `kappa` from a **structured Hessian tensor enclosure** without
collapsing to an ambient operator norm.

A non-redundant next child would treat a polynomial/affine Hessian family

`B(s,theta)=B_0 + sum_i alpha_i(s,theta) B_i`

with rational box/ellipsoid bounds on the coefficients and produce an exact PSD
majorant for

`B^T B <= kappa(theta^TMtheta)D^TD`,

or, when the mixed kernel gate fails, target the weaker radial polynomial (5.1)
directly.  The important distinction is now explicit: **matrix-Gram closure and
radial endpoint closure are separate mathematical lanes.**

Status remains **CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding**.
No provenance/receipt/admission upgrade or parent closure is asserted.