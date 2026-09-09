---
kind: review_result
review_id: GH-MATH-P5-LAMBDA-FREE-ADDITIVE-SCHUR-GATE-kuangmanmozun-20260909T0038Z
task_id: GH-MATH-P5-LAMBDA-FREE-ADDITIVE-SCHUR-GATE
source_agent: 狂蛮魔尊
created_at: 2026-09-09T00:38:00Z
inspected_commit: d6b8836cfb59f2c9a4a156dfa898e707dc471863
status: CONDITIONAL_PASS_LAMBDA_FREE_DISCRIMINANT_GATE
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
lean_compile_status: not_run
---

# Lambda-free weighted additive Schur gate

## 0. Scope and inspected inputs

This is a source-independent mathematical child. It does **not** re-audit provenance,
run Lean, bind a physical source, prove trajectory coverage, or change admission.
It consumes the current additive-port contract and removes an avoidable auxiliary
`lambda > 1` from the final allocation step.

Inspected inputs:

- `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GenericSchurAllocation20260908.lean`
  (blob `98a8d13e4faa450af2ac6a951acf68d874caaa9f`), in particular
  `schurNumerator` and `combined_of_port_budget`;
- `agent_review_inbox/NEW_REVIEW_P5_EXACT_RATIONAL_PSD_SCHEMA_ADDITIVE_HCAP_20260908.md`
  (blob `4469241886027c48893e5618eb304cbcd1cba63d`), which already identifies the
  weighted `H` adapter but still retains `lambda`;
- `agent_review_inbox/NEW_REVIEW_P5_SAME_CELL_GRAPH_JET_ADDITIVE_CONTRACT_20260908.md`
  (blob `322c39d25a72fb749cf064dfe07edd1e5bd98e8e`), which supplies the intended
  same-cell graph/additive-cap seam.

The question is purely mathematical:

> Once the source has proved `q_H(d) <= Delta`, what is the sharp envelope-only
> condition on the available headroom `beta-target` and the nominal metric energy
> `q_H(v_ref)` that guarantees the exact total target, without choosing a Young
> parameter and without taking a square root?

## 1. Exact lambda-free theorem

Let `H` be symmetric positive semidefinite and write

`q_H(u) = u^T H u`,  `<u,v>_H = u^T H v`.

Fix `v,d`, a nonnegative port cap `Delta`, and scalars `beta,target`. Define

```
L := q_H(v)
A := beta - target
C := A - L - Delta.
```

Assume

```
q_H(d) <= Delta,
0 <= C,
4 * L * Delta <= C^2.
```

Then

```
target <= beta - q_H(v+d).
```

Equivalently, a future weighted consumer can use the two exact polynomial gates

```
0 <= beta-target-q_H(v)-Delta,
4*q_H(v)*Delta <= (beta-target-q_H(v)-Delta)^2,
```

plus `H >= 0` and `q_H(d)<=Delta`. There is no inverse, matrix square root,
`lambda`, division, or irrational arithmetic in the trusted condition.

### Proof

Set `R=q_H(d)` and `s=<v,d>_H`. PSD Cauchy-Schwarz gives

`s^2 <= L R <= L Delta`.

Also

`q_H(v+d)=L+R+2s`.

If `s<=0`, then `q_H(v+d)<=L+Delta<=A` because `C>=0`.
If `s>0`, then

`4s^2 <= 4LDelta <= C^2`.

Since both `2s` and `C` are nonnegative, this implies `2s<=C`. Hence again

`q_H(v+d) <= L+Delta+C = A`.

This is exactly the desired target inequality.

For formalization, PSD Cauchy can itself be kept inverse-free as the Gram minor

`0 <= q_H(v)*q_H(d)-<v,d>_H^2`.

No positive definiteness is required; semidefinite `H` is enough.

## 2. Explicit strict reserve is also lambda-free

If a caller wants an **explicit output reserve** `tau>=0`, do not try to infer it
from a numerical distance of `lambda` from the optimizer. Instead define

`C_tau := beta-target-tau-L-Delta`.

The same proof gives

```
0 <= C_tau,
4*L*Delta <= C_tau^2
--------------------------------
target + tau <= beta - q_H(v+d).
```

Thus a rational source/checker can maximize or search `tau` directly while keeping
all trusted arithmetic polynomial. This is the clean quantitative replacement for
"choose a slightly safer lambda".

## 3. Relation to the existing finite-`lambda` Schur numerator

The current generic consumer uses

`N(lambda)=(lambda-1)*(A-lambda*Delta)-lambda*L`, with `lambda>1`.

Put `theta=lambda-1>0`. Then exactly

`N = -Delta*theta^2 + C*theta - L`.

Therefore, when `L>0` and `Delta>0`, there exists a real finite `lambda>1` with
`N>=0` **iff**

```
C > 0,
C^2 >= 4*L*Delta.
```

Because `L*Delta>0`, the lambda-free gate `C>=0` plus the discriminant inequality
already forces `C>0`. So in the genuine interior (`L,Delta>0`) the new gate is
exactly the existential closure of the old Young parameter, not a looser estimate.

However the old finite-`lambda` interface has two real endpoint holes:

### Zero port radius

Take `L=1, Delta=0, A=1`. The exact port condition forces `d` to have zero
`H`-seminorm, so `q_H(v+d)=L=1`; the target is valid at equality. The new gate has
`C=0` and passes.

But for every finite `lambda>1`,

`N=(lambda-1)*1-lambda*1=-1`.

This is precisely the boundary already exhibited by
`zero_radius_boundary_not_finite_witness` in the current Lean sidecar.

### Zero nominal radius

Take `L=0, Delta=1, A=1`. Again the exact robust target is valid at equality,
and the new gate passes with `C=0`. But

`N=(lambda-1)*(1-lambda)=-(lambda-1)^2<0`

for every `lambda>1`.

So the lambda-free theorem is a **strict completion** of the current finite-Young
consumer on degenerate but mathematically legitimate boundaries.

## 4. Sharpness and a fixed-lambda false rejection

The gate is information-theoretically sharp if the only port information is the
PSD metric cap. In one Euclidean dimension (`H=1`), take `v=sqrt(L)` and
`d=sqrt(Delta)` with the same sign. Then

`q_H(v+d)=L+Delta+2*sqrt(L Delta)`.

Thus no universal envelope theorem can replace the headroom threshold by anything
smaller without using extra signed/correlation information.

An exact rational regression shows why a fixed `lambda` can waste reserve:

```
L=4, Delta=1, A=9, H=1, v=2, d=1.
```

The exact total is `q(v+d)=9`, so the target holds at equality. The lambda-free
cleared gate is

`C=9-4-1=4`, `C^2=16=4*4*1`, hence PASS.

The commonly convenient choice `lambda=2` gives

`N=(2-1)*(9-2)-2*4 = -1`, hence rejects the same valid boundary. The optimal
finite Young witness is `lambda=3`, where `N=0`.

Therefore a fixed global `lambda` is a policy restriction, not an intrinsic Schur
limit. A checker should distinguish `FAIL_FIXED_LAMBDA` from failure of the
lambda-free discriminant gate.

## 5. Sharp boundary: additive forcing versus homogeneous headroom

This also resolves the open conceptual boundary between a genuinely additive port
and a homogeneous gain budget.

Let `x>=0` be a scalar energy proxy. Suppose the only same-cell envelopes are

```
q_H(v) <= kappa*x,
Delta <= rho*x + B,
beta-target >= a0 + eta*x,
```

with `kappa,rho,B>=0`. Define

```
c0 := a0-B,
c1 := eta-kappa-rho,
Cbar(x) := c0 + c1*x.
```

A fully rational sufficient gate for every fixed `x` is

```
0 <= Cbar(x),
4*kappa*x*(rho*x+B) <= Cbar(x)^2.
```

Indeed the actual `C=A-L-Delta` is at least `Cbar`, while
`L*Delta <= kappa*x*(rho*x+B)`.

### Purely homogeneous headroom cannot absorb a positive additive floor at the origin

If `a0=0` and `B>0`, then at `x=0` one has `Cbar(0)=-B<0`. Hence **no theorem based
only on these envelopes can uniformly absorb the additive port on a domain
containing the origin**. This is not a checker artifact: the scalar model
`H=1, v=0, d=sqrt(B), beta-target=0` satisfies the envelopes and violates the target.

The repair choices are mathematically distinct:

1. prove the actual additive floor vanishes (`B=0` or a stronger state-dependent cap);
2. provide genuine additive headroom `a0>0`;
3. exclude the low-energy region with a proved reachable/domain lower bound;
4. exploit additional signed correlation between `v` and `d` instead of the
   worst-case metric envelope.

One may not relabel a positive constant `B` as a homogeneous gain coefficient.

### Equality `a0=B` is still generally not enough near the origin

Assume `B>0` and `kappa>0`, and consider the envelope-saturating aligned scalar
case. If `a0=B`, then

`Cbar(x)=c1*x`,

while the squared cross requirement contains

`4*kappa*x*(rho*x+B)=4*kappa*B*x+O(x^2)`.

The left square is `O(x^2)` but the required cross budget is `O(x)`. Therefore,
for every finite `c1`, the robust envelope gate fails for all sufficiently small
positive `x`. So a uniform neighborhood of the origin needs **strict additive
headroom beyond the additive port floor** whenever both the nominal radius turns
on linearly (`kappa>0`) and `B>0`.

This is a useful obstruction: merely matching the constant terms `a0=B` closes the
single point `x=0` but not a whole low-energy tube.

### Homogeneous special case

If `B=0` and `a0=0`, then for every `x>0` the lambda-free condition reduces exactly
to

```
eta-kappa-rho >= 0,
(eta-kappa-rho)^2 >= 4*kappa*rho.
```

This is the square-root-free form of the sharp gain threshold
`eta >= (sqrt(kappa)+sqrt(rho))^2`.

Thus the additive case is not obtained by silently reusing the homogeneous gain
criterion; the constant floor changes the low-energy scaling order.

## 6. Exact interval checker for affine energy envelopes

For an intended energy interval `0<=x<=X`, the previous affine-envelope gate can
be checked without sampling. Let

```
p0 = c0^2,
p1 = 2*c0*c1 - 4*kappa*B,
p2 = c1^2 - 4*kappa*rho,
P(x)=p0+p1*x+p2*x^2.
```

Uniform closure is reduced to

`Cbar(x)>=0` and `P(x)>=0` on `[0,X]`.

The linear condition is exactly the two endpoint checks

`c0>=0`, `c0+c1*X>=0`.

For the quadratic, an exact rational checker can use the following complete case
split:

- if `p2<=0`, the minimum on the interval is at an endpoint; check `P(0)>=0`
  and `P(X)>=0`;
- if `p2>0` and `p1>=0`, the vertex lies at/before zero; `P(0)>=0` suffices;
- if `p2>0` and `p1+2*p2*X<=0`, the vertex lies at/after `X`; check `P(X)>=0`;
- otherwise the vertex is strictly inside; check the cleared minimum condition
  `4*p2*p0 >= p1^2`.

No division or floating vertex computation is needed. This is a direct candidate
for a small Lean/rational checker leaf once actual `(kappa,rho,B,a0,eta,X)` are
source-bound.

## 7. Formalization targets

Small theorem statements sufficient for a future Lean sidecar:

1. `psd_cauchy_sq`:
   `H PSD -> <u,v>_H^2 <= q_H(u)*q_H(v)`.
2. `weighted_combined_of_discriminant_budget`:
   the theorem of Section 1.
3. `weighted_combined_with_reserve_of_discriminant_budget`:
   the `tau` version of Section 2.
4. `schur_numerator_theta_identity`:
   `N(1+theta) = -Delta*theta^2 + C*theta - L`.
5. `zero_port_endpoint_lambda_free` and `zero_nominal_endpoint_lambda_free`.
6. `homogeneous_additive_floor_obstruction` for the scalar counterexample.
7. `affine_energy_envelope_discriminant` and the interval quadratic checker.

These should remain source-independent math. The actual K7/graph packet must still
prove the same-cell `H`, `d`, `Delta`, `v_ref`, `beta`, and `target` identities.

## 8. Integration recommendation and remaining boundary

If the K7 route eventually proves

`q_H(d)<=Delta`

in the actual same-cell graph, the shortest allocation seam is now:

```
L = q_H(v_ref)
C = beta-target-L-Delta
C >= 0
C^2 >= 4*L*Delta
-----------------------------
target <= beta-q_H(v_ref+d)
```

This removes both the metric square-root adapter and the auxiliary Young parameter
from the final trusted arithmetic. The existing fixed-`lambda` theorem remains a
valid sufficient leaf and can be retained for compatibility, but failure of a
chosen `lambda` is not a mathematical failure if this discriminant gate passes.

If source information contains a proved signed/correlation bound on
`<v_ref,d>_H`, a still sharper correlation-aware branch can beat the worst-case
`4LDelta` gate. That is a separate child; the present result is sharp for the
uncorrelated envelope class.

Current status remains `pending`: no actual source packet, no K7 witness, no
runtime/coverage evidence, no Lean/kernel receipt, and no registry/admission change.
