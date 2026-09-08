---
kind: review_result
review_id: review-T-P5-051-honglianmozun-20260907T2250
task_id: T-P5-051
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: 2026-09-07T22:48:00-06:00
created_at: 2026-09-07T22:50:00-06:00
claim_commit: b1f87192867020d53d09e9c3b6fdcb95b6560dd1
inspected_commit: 31b10141eecd81514a5dff12499de4cd6435ae59
continuation_of:
  - T-P5-044
  - T-P5-048
  - T-P5-050
related_tasks:
  - T-P5-040
  - T-P5-044
  - T-P5-048
  - T-P5-050
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_a_complete_2x2_symmetric_affine-energy_dispatcher_above_the_existing_PD_and_singular_PSD_children; preserve_the_non-PSD_and_kernel-incompatibility_obstructions_as_fail-closed_branches; do_not_force_the_PD_ratio_gate_onto_the_singular_boundary
---

# T-P5-051 — complete 2x2 symmetric affine-energy classifier

## 0. Scope and result

This child completes the mathematical classification behind the signed/correlated residual route started in T-P5-044 and continued through the singular boundary in T-P5-048/T-P5-050.

Let

```text
H = [[p,q],[q,s]]
Q(x,y) = p*x^2 + 2*q*x*y + s*y^2
B(x,y) = b4*x + b5*y
J(x,y) = -Q(x,y) - B(x,y).
```

Define the exact invariants

```text
Delta := p*s - q^2
tau   := p+s
k4    := s*b4 - q*b5
k5    := p*b5 - q*b4
N     := s*b4^2 - 2*q*b4*b5 + p*b5^2
B2    := b4^2+b5^2.
```

Then the following is a complete classification.

```text
There exists a finite C such that J(x,y) <= C for all real x,y

iff

H is positive semidefinite and b annihilates ker(H).
```

For a real symmetric 2x2 matrix this becomes the completely algebraic dispatcher

```text
(A) Delta > 0, p >= 0, s >= 0;                         [positive definite]

or

(B) Delta = 0, p >= 0, s >= 0, tau > 0,
    k4 = 0, k5 = 0;                                    [nonzero rank one]

or

(C) p = q = s = 0 and b4 = b5 = 0.                    [zero matrix]
```

The sharp completion cost is respectively

```text
(A) Csharp = N/(4*Delta),
(B) Csharp = B2/(4*tau),
(C) Csharp = 0.
```

If none of these branches holds, `J` is unbounded above along an explicit rational/polynomially-defined ray.

This closes an important logical gap: the positive-definite gate from T-P5-044 and the singular PSD gate from T-P5-050 are not merely sufficient local recipes. Together, with the non-PSD witnesses below, they form the exact global two-channel affine-energy classifier.

No source binding, Float64 semantics, ODE continuation, coverage, registry admission, provenance, or receipt is claimed here.

---

## 1. Positive-definite branch

Assume

```text
p >= 0,
s >= 0,
Delta > 0.
```

Then necessarily `p>0` and `s>0`, so `H` is positive definite.

Let

```text
z4 := 2*(p*x+q*y)+b4,
z5 := 2*(q*x+s*y)+b5.
```

The exact adjugate completion identity is

```text
z^T adj(H) z = 4*Delta*(Q+B) + N.                      (1.1)
```

Moreover

```text
p * (z^T adj(H) z)
  = (p*z5-q*z4)^2 + Delta*z4^2 >= 0.                  (1.2)
```

Therefore

```text
-Q-B <= N/(4*Delta).                                   (1.3)
```

The bound is sharp. At

```text
u* = -(adj(H)*b)/(2*Delta)
```

one has `2Hu*+b=0`, so equality holds in (1.1).

Thus the positive-definite branch needs no Young loss: its exact additive price is `N/(4Delta)`.

---

## 2. Nonzero singular PSD branch

Assume

```text
p >= 0,
s >= 0,
Delta = 0,
tau > 0.
```

Then `H` is nonzero rank-one PSD.

The exact compatibility vector is

```text
adj(H)*b = (k4,k5).
```

### 2.1 Compatible bias

If

```text
k4=0,
k5=0,
```

then `b in Range(H)` and the trace completion identity from the singular branch becomes

```text
[2*(p*x+q*y)+b4]^2 + [2*(q*x+s*y)+b5]^2
  = 4*tau*(Q+B) + B2.                                  (2.1)
```

Hence

```text
-Q-B <= B2/(4*tau).                                    (2.2)
```

This is sharp. Compatibility gives `H*b=tau*b`; therefore at

```text
u* = -b/(2*tau)
```

the two squares in (2.1) vanish.

### 2.2 Incompatible bias

If `(k4,k5)!=(0,0)`, then under `Delta=0`

```text
H*(k4,k5)^T = 0.                                       (2.3)
```

Also

```text
b4*k4+b5*k5 = N,

k4^2+k5^2 = tau*N.                                     (2.4)
```

Since `tau>0` and `(k4,k5)!=(0,0)`, (2.4) implies `N>0`.

Take

```text
u_t = -t*(k4,k5),   t>0.
```

Then

```text
Q(u_t)=0,
B(u_t)=-t*N,
J(u_t)=t*N -> +infinity.                               (2.5)
```

So a nonzero kernel component of the bias cannot be repaired by any finite additive constant.

---

## 3. Zero-matrix branch

Assume `H=0`, i.e.

```text
p=q=s=0.
```

Then

```text
J(x,y) = -b4*x-b5*y.
```

If `b=0`, `J=0` identically and the sharp charge is `0`.

If `b!=0`, set

```text
u_t = -t*b,  t>0.
```

Then

```text
J(u_t) = t*(b4^2+b5^2) -> +infinity.                   (3.1)
```

Thus the fully degenerate endpoint is finite iff the affine bias vanishes exactly.

---

## 4. Every non-PSD matrix is an exact obstruction

The previous children concentrated on PSD effective dissipation. For the actual signed residual route one also needs the converse: if the source Jacobian makes `H=A+Sym(K)` non-PSD, then no global additive bias charge can rescue the quadratic energy ledger.

Indeed, if there exists a vector `v` with `v^T H v<0`, then for `u=t v`,

```text
J(tv) = -t^2*(v^T H v) - t*(b^T v) -> +infinity
```

as `|t|->infinity`, because the positive quadratic term dominates the linear term.

For 2x2 symmetric `H`, explicit witnesses can be chosen branchwise.

### 4.1 Negative first diagonal

If

```text
p<0,
```

choose `v=(1,0)`. Then `Q(v)=p<0`.

### 4.2 Negative second diagonal

If

```text
s<0,
```

choose `v=(0,1)`. Then `Q(v)=s<0`.

### 4.3 Nonnegative diagonals but negative determinant

Assume

```text
p>=0,
s>=0,
Delta<0.
```

If `p>0`, choose

```text
v=(q,-p).
```

Then

```text
Q(v)=p*Delta<0.                                        (4.1)
```

If `p=0`, then `Delta=-q^2<0`, so `q!=0`. Choose

```text
v=(s+1,-2*q).
```

A direct expansion gives

```text
Q(v) = -4*q^2 < 0.                                     (4.2)
```

Therefore every failure of the elementary PSD conditions has an explicit negative-energy direction and hence an unbounded `J` ray.

This is a useful fail-closed structural boundary: an additive residual budget controls linear forcing only after the effective quadratic dissipation matrix has been shown PSD. A negative quadratic direction cannot be patched by a larger constant `B`.

---

## 5. Complete first-exit dispatcher for the current P5 Pareto ledger

For the current P5 family

```text
c(r) = (109-r)/200,
0 <= r <= 1,
V* = 1/4,
```

suppose the energy inequality has reached

```text
V' <= -c(r)*V + J(u).
```

Because `c(r)>0` on `[0,1]`, the exact strict inward condition at `V=1/4` is branchwise:

### Positive-definite branch

```text
p>=0,
s>=0,
Delta>0,
200*N < (109-r)*Delta.                                 (5.1)
```

### Nonzero rank-one branch

```text
p>=0,
s>=0,
Delta=0,
tau>0,
k4=0,
k5=0,
200*B2 < (109-r)*tau.                                  (5.2)
```

### Zero branch

```text
p=q=s=0,
b4=b5=0.                                               (5.3)
```

Then `J=0`, so the boundary is strictly inward automatically because `c(r)>0` and `V*=1/4>0`.

Every other branch is not merely uncertified: the separated global affine-completion mechanism is mathematically impossible because `J` is unbounded above.

### Important singular-boundary warning

Do **not** reuse the PD inequality (5.1) by setting `Delta=0`.

On the compatible rank-one boundary one also has `N=0`, so (5.1) degenerates to

```text
0 < 0,
```

which is false and would create a checker false negative. The correct continuous boundary limit is the trace charge (5.2), not the determinant ratio.

---

## 6. Complete parameter-tube dispatcher

If the incremental affine bias has the form

```text
b = g * dc
```

and the parameter tube is the existing

```text
Vd = dc^2/12,
```

then the same exact classification gives the inward gate:

### Positive definite

Let

```text
Ng := s*g4^2 - 2*q*g4*g5 + p*g5^2.
```

Require

```text
600*Ng < (109-r)*Delta.                                (6.1)
```

### Nonzero rank one

Require compatibility

```text
s*g4-q*g5 = 0,
p*g5-q*g4 = 0
```

and

```text
600*(g4^2+g5^2) < (109-r)*tau.                         (6.2)
```

### Zero branch

Only `g=0` admits an `O(dc^2)` global tube through this mechanism.

Again, if `H` is non-PSD or a singular PSD `H` has an incompatible `g`, the global quadratic tube mechanism fails by an explicit ray; no scalar additive constant proportional to `dc^2` can fix the missing curvature/kernel compatibility.

---

## 7. Structural interpretation

The signed/correlated residual route now has a complete two-channel energy fingerprint.

Given

```text
l(u) = K*u + b,
H = A + Sym(K),
```

only `Sym(K)` enters the quadratic power, because `u^T Skew(K) u=0`.

The remaining closure is exactly:

```text
1. H must be PSD;
2. if H is singular, b must lie in Range(H);
3. the additive price is the sharp quadratic completion on Range(H).
```

So the correct source-side object is not an entrywise absolute Jacobian bound. It is the signed symmetric effective dissipation matrix plus the projection of the affine remainder onto its kernel/range decomposition.

This yields a much sharper decision tree than independent scalar Young bounds and now includes exact failure certificates for every forbidden branch.

---

## 8. Suggested theorem statements

A future Lean/math sidecar can stay entirely elementary and branchwise. Suggested statements:

```text
pd_affine_completion_sharp
rank_one_affine_completion_sharp
rank_one_bias_incompatible_unbounded
zero_matrix_bias_unbounded
nonpsd_negative_direction_p
nonpsd_negative_direction_s
nonpsd_negative_determinant_p_pos
nonpsd_negative_determinant_p_zero
complete_two_channel_affine_energy_dispatcher
complete_two_channel_first_exit_dispatcher
complete_two_channel_parameter_tube_dispatcher
```

The polynomial identities needed for the proof are already division-free except for the final human-readable sharp constants. Checker-facing gates (5.1), (5.2), (6.1), and (6.2) are division-free.

---

## 9. Boundaries / not claimed

- No claim that deployed `forceError`, FD, controller, or source Jacobian satisfies any `K,b,H` contract.
- No claim that `H` is PSD on the physical coverage domain.
- No Float64/source reification.
- No ODE continuation or flowpipe coverage.
- No provenance/receipt/admission update.
- No duplication of the active T-P5-050 singular-PSD Lean formalization lane.

Admission remains `pending mathematical child`.
