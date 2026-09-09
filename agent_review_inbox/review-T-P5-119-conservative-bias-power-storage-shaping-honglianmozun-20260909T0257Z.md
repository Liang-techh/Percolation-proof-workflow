---
kind: review_result
review_id: review-T-P5-119-conservative-bias-power-storage-shaping-honglianmozun-20260909T0257Z
task_id: T-P5-119-CONSERVATIVE-BIAS-POWER-STORAGE-SHAPING
reviewer: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-09T02:57:00Z
claim_commit: 06f0298aa9a2c69a22c3c25f6dc684cfd6e36049
inspected_commit: 20810eea625a4895f7fe5677f4420b52d74c5c38
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-118-CENTER-BIAS-MIXED-SMALL-GAIN-guyuefangyuan-20260909T0224Z.md
    commit: d74f645aefcd7e485cd3b6df03d20b39e4e03826
  - path: agent_review_inbox/review-T-P5-117-ANCHOR-STORAGE-CENTER-COMPATIBILITY-liuguanyi-20260909T0204Z.md
    commit: 65b15e1baea910c0d913d9090209f00806ad7dfb
  - path: agent_review_inbox/review-T-P5-089-mechanical-skew-energy-honglianmozun-20260908T1104.md
    commit: 8faea4cff4f6f5157d2c11ed98f9473da8fd90cc
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact chain-rule, quadratic-form, and finite-dimensional differential-form derivation only
exit_code: n/a
---

# T-P5-119 — conservative bias power can be moved into the storage before paying an additive floor

## 0. Bottleneck selected

T-P5-117 proves that a nonzero anchor/storage-center offset cannot satisfy the homogeneous displacement comparator used by T-P5-116 at the zero-storage state. T-P5-118 therefore gives the correct generic fallback: retain the state-dependent second-jet factor but pay a mixed relative/additive Lyapunov charge.

T-P5-118 also leaves one explicit escape hatch: **a source-proved signed cancellation may remove the bias-generated floor**.

This child identifies the most important such structural branch for mechanical/Newton--Euler energy ledgers. A force or residual channel need not be treated as a disturbance merely because its norm or graph remainder is nonzero. If its power is an exact configuration derivative, then it belongs in the storage functional. If a velocity-dependent part is pointwise skew, its power is identically zero. Only the genuinely nonconservative remainder should reach the T-P5-118 additive/mixed budget.

The result is source-independent mathematics. It does not claim that the deployed anchor defect, gravity residual, FD residual, controller residual, or any particular Route-B channel is conservative.

---

## 1. Exact storage-shaping identity

Let `q(t)` be a configuration curve and `v=qdot`. Suppose an existing energy ledger has the form

**(1.1)**

`Edot <= -D + p_other + v^T r(t,q,v)`

with `D>=0`.

Assume the actual signed force/residual channel admits the decomposition

**(1.2)**

`r(t,q,v) = grad_q Psi(t,q) + J(t,q,v) v + n(t,q,v)`,

where `J^T=-J` pointwise. Then

`v^T J v = 0`

and the chain rule gives

`d/dt Psi(t,q(t)) = Psi_t + v^T grad_q Psi`.

Therefore

**(1.3)**

`v^T r = d/dt Psi - Psi_t + v^T n`.

Define the reshaped storage

**(1.4)** `V := E - Psi + C`,

where `C` is any time-independent normalization constant. Subtracting the exact derivative in (1.3) from (1.1) yields

**(1.5) EXACT SHAPED ENERGY LEDGER**

`Vdot <= -D + p_other + v^T n - Psi_t`.

Hence, in the autonomous conservative/gyroscopic case

`Psi_t=0`, `n=0`,

one gets

**(1.6)**

`Vdot <= -D + p_other`.

There is **no additive disturbance floor from this channel at all**. The force amplitude may be large; what matters is its signed power structure.

This is the correct energy-first ordering:

1. form the signed power `v^T r`;
2. remove exact derivative and skew-zero pieces;
3. only then norm-bound / Young-bound the remaining `v^T n`.

Charging the full `r` into T-P5-118 before this decomposition can double-count a conservative contribution that should have been part of the Lyapunov functional.

---

## 2. Constant bias is the simplest nontrivial example

Take a constant force bias

`r(q)=b`.

It is conservative with

`Psi(q)=b^T q`.

Thus

`v^T b = d/dt (b^T q)`

and the shaped storage is simply

**(2.1)** `V=E-b^T q+C`.

So a nonzero constant force bias does **not** intrinsically imply an ultimate-ball floor. It implies such a floor only if one insists on the old storage or lacks a positive/coercive reshaping.

This does not contradict T-P5-118. Its hard obstruction is valid under the fixed-storage squared-envelope premises. T-P5-119 changes the candidate Lyapunov functional before the disturbance budget is formed.

---

## 3. Inverse-free quadratic recentering theorem

The previous observation becomes especially concrete when the old storage already contains a quadratic potential.

Let `x=q-q0` and suppose

**(3.1)**

`E(x,v) = T(v) + (1/2) x^T K x`,

where `K=K^T`, `T(v)>=0`.

Let the conservative residual be affine:

**(3.2)** `r(x)=b+A x`, with `A=A^T`.

Take

`Psi(x)=b^T x + (1/2) x^T A x`.

Then `grad Psi=r`. Define the shaped stiffness

**(3.3)** `H := K-A`.

Assume a source/certificate layer supplies a vector `a` satisfying the **linear witness equation**

**(3.4)** `H a = b`.

No matrix inverse is required. Choose the normalization

**(3.5)** `C=(1/2) a^T H a`.

Then exact expansion gives

**(3.6) RECENTERING IDENTITY**

`E-Psi+C`
` = T(v) + (1/2) x^T H x - b^T x + (1/2) a^T H a`
` = T(v) + (1/2) (x-a)^T H (x-a)`.

Therefore, if

**(3.7)** `H >= 0`

as a quadratic form, the reshaped storage is nonnegative. If `H` is positive definite on the relevant configuration subspace and `T` is coercive in velocity, it is a genuine centered Lyapunov energy around `x=a`.

The trusted consumer needs only:

- exact symmetric `K,A`;
- exact vector equality `Ha=b`;
- an accepted PSD/coercivity witness for `H`;
- the scalar normalization (3.5).

It does not need `H^{-1}`, an eigen-decomposition, a square root, or an optimizer-computed equilibrium.

### Constant-bias specialization

Set `A=0`, hence `H=K`. If a rational witness `a` satisfies

`K a=b`,

then

`(1/2)x^TKx-b^Tx+(1/2)a^TKa = (1/2)(x-a)^T K(x-a)`.

Thus a constant bias can be absorbed exactly by recentering to the force-balanced equilibrium, provided the shaped stiffness remains admissible.

---

## 4. Exact obstruction 1: derivative cancellation alone does not make a Lyapunov function

Perfect power cancellation is insufficient if the reshaped storage loses positivity.

Take one dimension:

`K=1`, `A=2`, `b=0`, `T(v)=v^2/2`.

The residual `r(x)=2x` is perfectly conservative with `Psi=x^2`, so its power can be removed from `Edot` exactly. But

`H=K-A=-1`,

and the shaped storage is

`V=v^2/2-x^2/2`,

which is indefinite and unbounded below in configuration.

Therefore the source contract must keep two gates separate:

1. **power identity / exact derivative gate**;
2. **reshaped-storage positivity/coercivity gate**.

A successful gradient identity cannot substitute for the second gate.

---

## 5. Exact obstruction 2: semidefinite shaped stiffness needs a range/center witness

Suppose `H>=0` but singular. A constant bias is harmless only if it is compatible with the range of `H`.

If an `a` satisfying `Ha=b` exists, (3.6) still gives a nonnegative centered configuration energy.

If no such `a` exists, then because `H` is symmetric PSD, there is a vector `z in ker(H)` with `b^T z != 0`. Along `x=t z`,

`(1/2)x^THx-b^Tx = -t b^T z`,

which is unbounded below in one time direction. No additive normalization constant can repair this.

A concrete example is

`H=diag(1,0)`, `b=(0,1)`.

Then the shaped potential is

`x1^2/2 - x2`,

unbounded below. So for semidefinite storage the exact solve witness `Ha=b` is not cosmetic: it is the finite-dimensional compatibility condition that prevents a bias along an uncontrolled zero-energy direction.

---

## 6. General configuration-force fingerprint: symmetric Jacobian means locally conservative

The affine theorem suggests a reusable structural test for a nonlinear residual field `r(q)`.

Assume `r` is `C^1` on a star-shaped configuration domain `Omega` with center `q0`. If there is a `C^2` scalar potential `Psi` with

`grad Psi = r`,

then necessarily

**(6.1)** `Dr(q)=Dr(q)^T`

throughout `Omega`, because `Dr` is the Hessian of `Psi`.

Conversely, on a star-shaped domain, (6.1) is sufficient. Put `x=q-q0` and define the line-integral potential

**(6.2)**

`Psi(q) := integral_0^1 r(q0+s x)^T x ds`.

For any direction `h`, differentiation gives

`D Psi(q)[h]`
` = integral_0^1 [s Dr(q0+s x)[h]^T x + r(q0+s x)^T h] ds`.

Using symmetry of `Dr`,

`Dr[h]^T x = h^T Dr[x]`

and `Dr[x] = d/ds r(q0+s x)`. Hence

`D Psi(q)[h]`
` = h^T integral_0^1 [s d/ds r(q0+s x) + r(q0+s x)] ds`
` = h^T [s r(q0+s x)]_0^1`
` = h^T r(q)`.

Therefore `grad Psi=r`.

This gives a precise structural fingerprint for a configuration-only residual:

> **curl-free / symmetric Jacobian on the same star-shaped cell -> exact storage-shaping candidate.**

A source producer may either export the potential identity directly or prove the Jacobian symmetry and use a constructive polynomial/integral potential. The latter is especially natural for exact polynomial/rational residual models.

---

## 7. Affine nonsymmetric residual: absorb only the symmetric part

For an affine field

`r(x)=b+A x`,

decompose

`S=(A+A^T)/2`, `N=(A-A^T)/2`.

Then `S^T=S`, `N^T=-N`, and

**(7.1)**

`Psi(x)=b^T x + (1/2)x^T S x`

satisfies

`grad Psi=b+Sx`.

Thus

**(7.2)**

`v^T r = d/dt Psi + v^T N x`.

Only the antisymmetric configuration-Jacobian part remains as a genuine nonconservative power channel.

This point matters because `N` being skew does **not** make `v^T N x` vanish. Skew cancellation applies to `v^T J v`, not to a mixed `v^T N x` term.

For example, in two dimensions let

`N=[[0,-1],[1,0]]`, `x=(1,0)`, `v=(0,1)`.

Then

`N x=(0,1)` and `v^T N x=1`.

So a nonsymmetric stiffness/residual Jacobian cannot be silently treated as a gyroscopic term.

This is the exact affine obstruction: a configuration-only affine force admits a quadratic scalar potential iff its linear coefficient is symmetric.

---

## 8. Gyroscopic residual fingerprint

A genuinely velocity-linear skew term behaves differently. If

`r_g(q,v)=J(q,v) v`,

with

`J(q,v)^T=-J(q,v)`

pointwise, then

**(8.1)** `v^T r_g = v^T J v = 0`.

No smallness, norm cap, or domain radius is needed for this cancellation. This is the residual-channel analogue of the mechanical skew-energy identity already isolated in T-P5-089.

Therefore a good source decomposition is not merely

`residual = small + bias`.

It is structurally finer:

**(8.2)**

`residual = conservative configuration part`
`         + gyroscopic/skew velocity part`
`         + genuinely nonconservative remainder`.

Only the last line should consume the generic P5 residual-power reserve.

---

## 9. Time-dependent potential / moving reference boundary

If `Psi=Psi(t,q)` is time-dependent, the conservative configuration power still cancels, but (1.5) leaves the exact schedule term

**(9.1)** `-Psi_t`.

This is important for ramp/reference problems: one should charge the **time variation of the potential**, not its full force amplitude.

For example, let

`r(t,q)=b(t)` and `Psi(t,q)=b(t)^T q`.

Then

`v^T b(t) = d/dt(b(t)^T q) - bdot(t)^T q`,

so after shaping the remaining power is

**(9.2)** `-bdot(t)^T q`.

A constant plateau (`bdot=0`) has zero continuous-flow cost even if `|b|` is large. A ramp pays only the slew term. This is the same structural lesson as the recentered reference-energy lane, now stated directly at the force-power level.

If the storage is renormalized by a time-dependent scalar `C(t)`, its derivative `Cdot(t)` must also be included; additive normalization is derivative-free only when the constant is actually constant.

---

## 10. Interaction with T-P5-118: when the additive floor is and is not unavoidable

T-P5-118 remains the correct fallback when one has only a nonzero bias packet and a squared power envelope. T-P5-119 adds a strict preprocessing rule:

### Branch A — exact conservative/skew structure is proved

If the actual signed source channel satisfies (1.2) with `n=0` and autonomous `Psi`, reshape the storage and charge **zero** generic residual budget for that channel.

If `Psi_t` or a nonconservative `n` remains, charge only those terms.

### Branch B — no such structure is proved

Keep the old storage and use T-P5-118's mixed/additive small-gain theorem. Do not infer conservativity from small curl samples, approximate symmetry, or a nearby gravity formula.

### Double-counting guard

Once `grad Psi` has been moved from the force ledger into `V=E-Psi+C`, it must be removed from every downstream `p_A`, residual norm, and additive `beta` packet. Charging it again is mathematically a duplicate debit.

Likewise, if the original physical energy already contains the potential whose gradient produces a force term (for example an exact gravity potential), that term is already in the energy identity and must not be reshaped a second time.

---

## 11. Candidate theorem statements

The highest-value source-independent leaves are small.

```text
exact_power_storage_shaping:
  qdot=v,
  Edot <= -D + p_other + <v,r>,
  r = grad_q Psi + J v + n,
  J^T=-J
  -> d/dt(E-Psi+C) <= -D + p_other + <v,n> - Psi_t.

skew_velocity_power_zero:
  J^T=-J -> <v,Jv>=0.

affine_residual_split:
  r=b+A x,
  S=(A+A^T)/2,
  N=(A-A^T)/2
  -> <v,r> = d/dt[b^T x + 1/2 x^T S x] + <v,Nx>.

quadratic_storage_recenter:
  H=K-A, H^T=H, H>=0, H a=b
  -> 1/2 x^T K x - (b^T x + 1/2 x^T A x) + 1/2 a^T H a
     = 1/2 (x-a)^T H (x-a) >=0.

affine_conservative_iff_symmetric:
  grad Psi(x)=b+A x for a C2 scalar Psi on an open cell
  -> A=A^T;
  conversely A=A^T gives Psi=b^T x+1/2 x^T A x.
```

The first, second, and quadratic recentering leaves are excellent Lean candidates because they use only chain-rule premises / ring algebra / transpose symmetry. The nonlinear star-shaped converse can remain a later calculus leaf.

---

## 12. Minimal source-facing packet

Before paying a nonzero P5 bias into T-P5-118, the source side should, when relevant, attempt to provide:

1. the **actual signed force/residual expression** `r` on the same coordinates used by the power ledger;
2. the kinematic identity `qdot=v` on that lane;
3. either an exact potential `Psi` with `grad Psi=r_cons`, or an exact same-cell Jacobian-symmetry/closed-one-form witness;
4. any pointwise skew matrix `J` with an exact equality `r_gyro=Jv` and `J^T=-J`;
5. the remaining `n=r-r_cons-r_gyro` as the only generic disturbance channel;
6. a shaped-storage positivity/coercivity certificate and a normalization/center identity;
7. if time-dependent, an explicit bound or signed identity for `Psi_t` (and `Cdot` if normalization moves);
8. a no-double-count declaration tying the reshaped force term to the removed residual packet.

For an affine/quadratic exact-rational lane, items 3 and 6 reduce to symmetric matrices, one exact linear equation `Ha=b`, and PSD certificates. No inverse primitive is necessary.

---

## 13. Open boundaries / non-claims

This result is **CONDITIONAL_PASS / pending mathematical child** only.

Still open:

- whether the actual anchor second-jet force/power in T-P5-112/113/118 is configuration-conservative, gyroscopic, or neither;
- whether the deployed gravity/controller/FD/solve residual decomposition preserves a signed field from which a potential can even be defined;
- exact source equality for any proposed `Psi`, `J`, `A`, `b`, `K`, `H`, or center `a`;
- same-cell/star-shaped coverage for a nonlinear closed-one-form argument;
- positivity/coercivity and threshold normalization of the reshaped active storage;
- explicit-time/reference slew budgets;
- Float64/FD/runtime semantics, P8 flowpipe, Lean/kernel, independent verifier 封不觉, admission and registry.

The mathematical advance is a structural alternative to the generic biased-anchor ultimate tube: **a nonzero force bias need not cost an additive Lyapunov floor if its signed power is an exact derivative and the corresponding reshaped storage remains admissible.** The irreducible object is the nonconservative remainder, not the raw residual magnitude.
