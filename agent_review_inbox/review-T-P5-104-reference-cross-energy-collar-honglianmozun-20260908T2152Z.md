---
kind: review_result
review_id: review-T-P5-104-reference-cross-energy-collar-honglianmozun-20260908T2152Z
task_id: T-P5-104-REFERENCE-CROSS-ENERGY-COLLAR
source_agent: 红莲魔尊
created_at: 2026-09-08T21:52:00Z
claim_commit: 6efe1c05e810729e80325e0f9b35ad1dc4f77516
inspected_commit: 879cbcacbc502da3651074ca200a31505a1a3186
upstream_reference_review_commit: 0d00d383cd8a82772bab4036e83f76d29388107e
upstream_tasks:
  - P5-103-ACTUAL-REFERENCE-CONTEXT-BINDING
  - T-P5-100-BASE-STORAGE-COLLAR-MATH
status: CONDITIONAL_PASS
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize the exact cross-energy derivative/power-square absorption/collar theorem, then bind it to one actual RefSpec without exporting an entire trajectory as a primitive
commands: none_math_derivation_only
lean_compile_status: not_run
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
---

# T-P5-104 — nominal-reference cross-energy collar

## 0. Question and result

P5-103 has reduced the nominal-reference identity problem to a small source object: a constant-coefficient reference generator plus an initial identity can determine the reference, rather than requiring the whole trajectory as primitive data. What is still missing on the mathematics side is a **general-time reference-state bound** that can be generated from that RefSpec without sampling/exporting every `qbar(t),vbar(t)`.

For the nominal block equation

`M q'' + D q' + K q = f(t)`,  `v=q'`,

this review gives a cross-term Lyapunov storage

`Veps = 1/2 q^T K q + 1/2 v^T M v + eps q^T M v`

whose derivative is an exact algebraic identity. A single rational block-PSD rate certificate plus one squared input-power certificate yields

`Veps' <= -nu Veps + beta`,

and therefore the exact Route-B collar form already consumed by T-P5-100/T-P5-096:

`nu Veps' <= -nu^2 Veps + nu beta`.

The construction is inverse-free, square-root-free and exponential-free at the trusted gate. It also exposes a precise obstruction: the raw mechanical energy cannot satisfy a strict pointwise decay inequality on all nonzero states, even for an unforced strictly damped oscillator, because at a turning state `v=0,q!=0` its derivative is exactly zero. Thus a cross term (or a finite-step/path-energy argument) is mathematically necessary if the desired interface is a strict instantaneous collar inequality.

This review is source-independent exact-real mathematics. It does not establish an actual `referenceKey`, deployed source equality, Float64/controller semantics, P8 flowpipe/coverage, Lean compilation or registry admission.

---

## 1. Exact cross-energy identity

Assume throughout this section that `M,D,K` are constant real symmetric matrices and the reference obeys

`q' = v`,

`M v' + D v + K q = f(t)`.

No matrix inverse is needed in the derivation.

Define

`E = 1/2 v^T M v + 1/2 q^T K q`,

`C = q^T M v`,

`Veps = E + eps C`.

The raw energy satisfies

`E' = v^T(Mv') + q^T K v`
`   = v^T(f-Dv-Kq) + q^T K v`
`   = -v^T D v + v^T f`.

The cross term satisfies

`C' = v^T M v + q^T M v'`
`   = v^T M v + q^T(f-Dv-Kq)`
`   = v^T M v - q^T D v - q^T K q + q^T f`.

Therefore the exact identity is

**(1.1)**

`Veps' = -Qeps(q,v) + (v+eps q)^T f`,

where

**(1.2)**

`Qeps(q,v)`
` = eps q^T K q + eps q^T D v + v^T(D-eps M)v`.

Introduce `x=(q,v)` and the symmetric block matrices

**(1.3)**

`Peps = [[K, eps M], [eps M, M]]`,

`Qmat_eps = [[eps K, (eps/2)D], [(eps/2)D, D-eps M]]`.

Then

`Veps = 1/2 x^T Peps x`,

`Qeps = x^T Qmat_eps x`.

This is the useful checker shape: storage positivity is a statement about `Peps`, while strict homogeneous decay is a different statement about `Qmat_eps`. They must not be conflated.

### Candidate theorem

`reference_cross_energy_derivative`

Inputs: the two reference equations and symmetry of `M,D,K`.

Output: equation (1.1) exactly.

The proof needs only bilinearity, transpose symmetry and ring normalization.

---

## 2. Division-free rate certificate

Assume a source-independent matrix certificate provides

**(2.1)** `Peps >= 0`

and, for some exact rational/real `lambda>0`,

**(2.2)** `2 Qmat_eps - lambda Peps >= 0`

in the quadratic-form sense.

Then for every state `x`,

`2 Qeps >= lambda x^T Peps x = 2 lambda Veps`,

hence

**(2.3)** `Qeps >= lambda Veps >= 0`.

No generalized eigenvalue, inverse, or square root needs to appear in the theorem statement. For a fixed rational reference model, (2.1) and (2.2) may be discharged by principal minors, LDL/SOS, or any existing exact PSD adapter.

If the storage sublevel itself is later used as a physical domain, one additionally needs a positive coercivity packet such as `Peps >= m I` with `m>0`, or an explicit sublevel-to-source-tube inclusion. Mere semidefiniteness is not a coverage theorem.

---

## 3. Sharp squared-power absorption

Let

`p := (v+eps q)^T f`.

Suppose for constants

`0 <= theta < 1`, `0 <= beta`

one can prove

**(3.1)** `p^2 <= 4 theta beta Qeps`.

Then

`(theta Qeps + beta)^2 - p^2`
` >= (theta Qeps + beta)^2 - 4 theta beta Qeps`
` = (theta Qeps-beta)^2 >= 0`.

Because `theta Qeps+beta>=0`, this implies

**(3.2)** `p <= theta Qeps + beta`.

Combining (1.1), (2.3) and (3.2),

`Veps' <= -(1-theta)Qeps + beta`
`      <= -(1-theta)lambda Veps + beta`.

Define

**(3.3)** `nu := (1-theta) lambda > 0`.

Then

**(3.4)** `Veps' <= -nu Veps + beta`,

and multiplying by positive `nu` gives

**(3.5)** `nu Veps' <= -nu^2 Veps + nu beta`.

This is exactly the T-P5-100/T-P5-096 Route-B collar syntax, with

`E_collar = nu beta`.

For inner/outer levels `Rin<Rout`, the non-strict inward gate is simply

**(3.6)** `beta <= nu Rin`.

A strict first-exit barrier uses `beta < nu Rin`.

The coefficient `4` in (3.1) is sharp at the scalar-information level. Given only `p^2 <= C Qeps`, the smallest uniform additive charge compatible with a fixed dissipation fraction `theta>0` is `C/(4 theta)`; equality occurs at the completed-square boundary. Therefore improving this constant requires additional sign/correlation information, not a different Young parameterization.

### Candidate theorem

`reference_cross_energy_collar_of_power_square`

Inputs:

- exact identity (1.1),
- `Peps >= 0`,
- `2 Qmat_eps-lambda Peps >= 0`, `lambda>0`,
- `0<=theta<1`, `0<=beta`,
- `p^2 <= 4 theta beta Qeps`.

Output: (3.4) and (3.5), with first-exit gate (3.6).

---

## 4. Scalar input law: a RefSpec can produce the whole power packet

P5-103 writes the canonical constant-coefficient reference forcing as `f(t)=g w(t)`. In this important scalar-input case, the source burden can be reduced further without exporting the reference trajectory.

Let

**(4.1)** `c_g := (eps g, g)`

in the stacked `(q,v)` coordinates. Then

`p = w(t) c_g^T x`.

Suppose the same RefSpec provides an input amplitude certificate

**(4.2)** `w(t)^2 <= Wbar`

on the time interval of interest, and an exact quadratic domination

**(4.3)** `(c_g^T x)^2 <= chi Qeps(x)`

for all states, with `chi>=0`.

The latter can itself be certified without inverse/square root by the single PSD matrix

**(4.4)** `chi Qmat_eps - c_g c_g^T >= 0`.

Then

`p^2 <= Wbar chi Qeps`.

Consequently it suffices to verify the scalar division-free gate

**(4.5)** `Wbar chi <= 4 theta beta`.

Thus an actual canonical reference packet need not contain a sampled `qbar/vbar` trajectory merely to obtain a general-time energy collar. A mathematically sufficient source handoff is:

`referenceKey / RefSpec`
`+ exact M,D,K,g`
`+ initial state`
`+ uniqueness/existence semantics`
`+ input amplitude Wbar`
`+ rational eps,lambda,chi,theta,beta`
`+ PSD witnesses (Peps, 2Q-lambda P, chi Q-c_gc_g^T)`.

The separate physical-domain/flowpipe layer must still prove that this reference collar is the one used by the hybrid anchor and that any derivative/FD/reference halos are covered.

---

## 5. Exact rational sanity witness

The packet is non-vacuous even in a fully rational toy oscillator.

Take the scalar model

`M=D=K=g=1`, `eps=1/4`.

Then

`Peps = [[1,1/4],[1/4,1]]`,

whose determinant is `15/16>0`.

Also

`Qmat_eps = [[1/4,1/8],[1/8,3/4]]`,

with determinant `11/64>0`.

Choose `lambda=1/4`. Then

`2Qmat_eps-lambda Peps`
` = [[1/4,3/16],[3/16,5/4]]`,

whose determinant is `71/256>0`.

For `c_g=(1/4,1)` choose `chi=3/2`. Then

`chi Qmat_eps-c_g c_g^T`
` = [[5/16,-1/16],[-1/16,1/8]]`,

whose determinant is `9/256>0`.

If `w^2<=1`, choose `theta=1/2`, `beta=3/4`. Then

`Wbar*chi = 3/2 = 4 theta beta`,

and `nu=(1-theta)lambda=1/8`. Therefore the exact rational theorem gives

`Veps' <= -(1/8)Veps + 3/4`.

A strict first-exit collar follows at any `Rin>6` (plus `Rin<Rout` and the independent source-domain inclusion). This example is only a regression witness for the algebra; it is not a Route-B parameter recommendation.

---

## 6. Structural obstruction: raw mechanical energy is not a strict pointwise Lyapunov rate

Even when `f=0` and `D` is strictly positive definite, the raw energy

`E=1/2 v^T M v+1/2 q^T K q`

satisfies only

`E'=-v^T D v`.

At every turning state with

`v=0`, `q!=0`,

one has

`E'>=0` actually `E'=0`, while `E>0` if `K` is positive definite.

Therefore for **every** `nu>0` the pointwise inequality

`E' <= -nu E`

fails at such a state.

This is not a weakness of a particular Young inequality. It is an exact information/functional obstruction. A strict instantaneous collar rate for the reference oscillator requires at least one of:

1. a cross-term storage such as `Veps` above;
2. a finite-step/path-energy theorem that converts dissipation over time into state contraction;
3. a stronger source restriction excluding turning states, which would itself need a real path/domain proof.

Hence P5-103's general-time reference bound should not be sought by repeatedly tightening the raw `E'=-v^T Dv` estimate.

---

## 7. Two additional fail-closed boundaries

### 7.1 The cross term must be certified as a storage

A derivative identity alone does not make `Veps` positive. In the scalar `M=K=1` case,

`Veps=1/2(q^2+v^2)+eps qv`.

If `|eps|>1`, choosing `v=-sign(eps)q` makes `Veps<0` for nonzero `q`. Therefore a consumer must carry `Peps>=0` (preferably a strict coercivity witness for domain use); it may not infer positivity from the physical energy pieces after adding the cross term.

Likewise, an overly large `eps` can destroy dissipation: with `M=D=K=1`, `eps=2`, the `v-v` entry of `Qmat_eps` is `D-eps M=-1`, so homogeneous `Veps'` can be positive. Storage positivity and rate positivity are separate gates.

### 7.2 Persistent forcing needs additive reserve or recentering

Suppose a nonzero fixed forcing is present and the domain contains states arbitrarily near `x=0`. A homogeneous claim `p<=theta Qeps` cannot generally hold. Along `x=t x0` with `c_g^T x0` having the forcing sign,

`p=O(t)` but `Qeps=O(t^2)`.

For sufficiently small positive `t`, the linear power dominates any fixed multiple of the quadratic dissipation. Therefore a nonzero reference input must be handled by an additive `beta`, a state-dependent input that vanishes at the centered equilibrium, or an explicit recentering to a forced equilibrium. It cannot be silently renamed a relative error.

---

## 8. Minimal next source/Lean handoff

This child closes the missing **mathematical** bridge from a canonical constant-coefficient RefSpec to a general-time base-storage collar. The narrow next handoff is now:

1. bind one actual `referenceKey` to the constant matrices/vectors `M,D,K,g`, the initial state and input law `w(t)`;
2. choose an exact rational `eps` and prove `Peps` positive/coercive and `2Qmat_eps-lambda Peps>=0` with one exact `lambda>0`;
3. prove the scalar input cap `w^2<=Wbar` on the intended time interval;
4. prove `chi Qmat_eps-c_g c_g^T>=0` and the scalar gate `Wbar chi<=4 theta beta`;
5. use `beta<=((1-theta)lambda) Rin` and a separate outer-sublevel/source-tube inclusion to feed the existing Route-B collar theorem.

If item 2 fails for every admissible rational `eps`, that is a genuine stability/storage-design obstruction. If item 3 or the `referenceKey` binding is absent, the result stays source-pending. If only raw mechanical energy is available, the turning-state argument above rules out the desired strict pointwise rate and the project should use the existing finite-step/path-energy route instead of forcing a false differential inequality.

No source identity, runtime evaluator, Float64/controller, physical coverage, P8 path-sheet, Lean/kernel receipt, comparator/admission or registry status is claimed by this review.
