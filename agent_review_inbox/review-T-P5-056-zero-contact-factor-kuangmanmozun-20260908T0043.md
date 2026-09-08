---
kind: review_result
review_id: review-T-P5-056-zero-contact-factor-kuangmanmozun-20260908T0043
task_id: T-P5-056
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: 2026-09-08T00:30:00-06:00
created_at: 2026-09-08T00:43:00-06:00
claim_commit: 4d945622138fe626c3e2b99f027c6004947d5a58
inspected_commit: c59525efbd1abfb49b5958eab9c0a27c013b30dd
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P5-052-guyuefangyuan-20260907T2334.md
  - agent_review_inbox/review-T-P5-054-correlated-matrix-perturbation-liuguanyi-20260908T0013.md
  - agent_review_inbox/review-T-P5-055-guyuefangyuan-20260908T0031.md
continuation_of:
  - T-P5-052
  - T-P5-055
related_tasks:
  - T-P5-053
  - T-P5-054
  - T-P5-050
  - T-P5-051
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add an exact rational zero-contact factor certificate for degree <= 3 branch-free remainders, so nonnegative determinant/trace polynomials touching zero at rational non-dyadic points can terminate without infinite dyadic subdivision; keep endpoint and interior zero semantics distinct and preserve negative-control tri-state
---

# T-P5-056 — exact zero-contact factor certificate for quadratic/cubic branch-free remainders

## 0. Bottleneck

`T-P5-052` gives exact quadratic/cubic Bernstein gates for the branch-free remainders `Rtr` and `Rdet`. `T-P5-055` strengthens this with a quantitative theorem: strict positivity implies finite dyadic Bernstein certification, but mere nonnegativity can stall forever. Its canonical obstruction is

```text
Z(t) = (t - 1/3)^2 >= 0,
```

whose unique dyadic cell containing `1/3` retains a negative interior Bernstein control at every dyadic depth.

This leaves one small but important mathematical gap: the checker needs an exact **zero-contact escape hatch** that certifies a nonnegative quadratic/cubic polynomial without requiring all Bernstein controls to become nonnegative.

For the affine one-cell P5 model this gap is unusually tractable because

```text
deg Rtr  <= 2,
deg Rdet <= 3.
```

The main result below is that interior zero contact for a rational polynomial of degree at most three always admits a tiny rational repeated-root/factor certificate. The trusted checker needs only ring identities and endpoint sign checks; polynomial gcd/root finding may remain outside the trusted core.

No source/Float64/FD/controller/P8/coverage/admission claim is made.

---

## 1. Interior nonnegative zeros must be multiple

Let `P` be a real polynomial and assume

```text
P(t) >= 0  for every t in [0,1].
```

If

```text
0 < r < 1,
P(r) = 0,
```

then `r` is a local minimum, hence

```text
P'(r) = 0.                                               (1.1)
```

Equivalently, a simple root in the open interval is incompatible with nonnegativity: if `P(r)=0` and `P'(r) != 0`, then `P` changes sign arbitrarily close to `r`.

This is the first fail-closed rule:

```text
interior zero + nonnegative claim
    -> repeated-root certificate is mandatory.
```

It must **not** be applied at `r=0` or `r=1`: one-sided nonnegativity permits a simple endpoint root, e.g. `P(t)=t` on `[0,1]`.

---

## 2. Quadratic zero-contact certificate

Let

```text
P(t) = a*t^2 + b*t + c.
```

Supply a rational candidate `r`. The following two coefficient equalities are division-free:

```text
b + 2*a*r = 0,                                          (2.1)
c - a*r^2 = 0.                                          (2.2)
```

They imply the exact ring identity

```text
P(t) = a*(t-r)^2.                                        (2.3)
```

Hence:

### T-P5-056-A — quadratic repeated-root PASS

If

```text
0 <= r <= 1,
a >= 0,
b + 2*a*r = 0,
c - a*r^2 = 0,
```

then

```text
P(t) >= 0  for every t in [0,1].                         (2.4)
```

If `0<r<1` and `P` is not identically zero, the condition `a>=0` is also necessary for nonnegativity.

For the `T-P5-055` obstruction

```text
Z(t)=t^2-(2/3)t+1/9,
r=1/3,
a=1,
```

both (2.1) and (2.2) vanish exactly. Thus the polynomial that defeats every pure dyadic all-controls test receives an immediate exact PASS from four rational checks.

A discriminant version is equivalent when `a>0`:

```text
b^2 - 4*a*c = 0,
-2*a <= b <= 0
```

puts the double root `r=-b/(2a)` in `[0,1]`. The witness form (2.1)-(2.2) is preferable for Lean/checker use because it avoids division and square roots.

---

## 3. Cubic interior zero-contact factorization

Let

```text
P(t) = a*t^3 + b*t^2 + c*t + d.
```

Suppose a candidate `r` satisfies the division-free coefficient conditions

```text
c + 3*a*r^2 + 2*b*r = 0,                                (3.1)
d - 2*a*r^3 - b*r^2 = 0.                                (3.2)
```

Then direct expansion gives

```text
P(t)
 = (t-r)^2 * L(t),                                       (3.3)

L(t)
 = a*t + (b + 2*a*r).                                    (3.4)
```

Conditions (3.1)-(3.2) are exactly what follows from `P(r)=0` and `P'(r)=0`; conversely they directly certify the factor identity without asking the trusted checker to manipulate derivatives or divide by a leading coefficient.

Define the two rational endpoint values

```text
L0 := L(0) = b + 2*a*r,
L1 := L(1) = a + b + 2*a*r.                              (3.5)
```

For `0<=t<=1`,

```text
L(t) = (1-t)*L0 + t*L1.                                  (3.6)
```

Therefore:

### T-P5-056-B — cubic repeated-root PASS

If

```text
0 <= r <= 1,
(3.1), (3.2),
L0 >= 0,
L1 >= 0,
```

then

```text
P(t) >= 0  for every t in [0,1].                         (3.7)
```

For an **interior** contact `0<r<1`, this endpoint test on `L` is not merely sufficient. Under the factor identity (3.3),

```text
P >= 0 on [0,1]
    iff
L >= 0 on [0,1]
    iff
L0>=0 and L1>=0.                                         (3.8)
```

The reason is that `(t-r)^2>0` away from the single point `r`, so the sign of `P` there is exactly the sign of the affine factor `L`; continuity fills the contact point.

Thus the cubic zero-contact branch has an exact rational necessary-and-sufficient gate once `r` is supplied.

---

## 4. Why the repeated root is rational for degree <= 3 rational data

The factor witness above is not assuming a miraculous rational root that need not exist. For rational coefficients and degree at most three, any interior zero of a nonnegative polynomial is rational.

### Quadratic

For `a != 0`, `P'(r)=0` gives

```text
2*a*r = -b,
```

so `r in Q`. If `a=0`, a nonzero linear polynomial cannot have an interior nonnegative zero; the zero polynomial is trivial.

### Cubic

Let `a != 0` and define

```text
Delta0 := b^2 - 3*a*c.                                   (4.1)
```

An interior nonnegative zero is repeated. A triple interior root would make a nonzero cubic proportional to `(t-r)^3`, which changes sign across `r`; hence the nonnegative case cannot be triple. Therefore the repeated root is the ordinary double root of a cubic.

For a double but nontriple root, exact coefficient algebra gives

```text
2*Delta0*r = 9*a*d - b*c.                                (4.2)
```

Moreover `Delta0 != 0` (indeed for `a(t-r)^2(t-s)`, `Delta0=a^2(r-s)^2>0`). Hence

```text
r = (9*a*d-b*c)/(2*Delta0) in Q.                         (4.3)
```

So an untrusted generator can recover the candidate root using exact rational arithmetic; the trusted proof path still only needs to verify (3.1)-(3.2), the interval membership, and `L0,L1>=0`.

This is useful architecture: **root discovery is not a trusted operation**. A CAS/gcd routine may propose `r`; the proof checker verifies a tiny rational certificate.

---

## 5. Endpoint zero branch must remain separate

Interior and boundary zero contacts are mathematically different.

The rule

```text
P(r)=0 and P>=0 -> P'(r)=0
```

is valid only for `0<r<1`.

At an endpoint,

```text
P(t)=t
```

is nonnegative on `[0,1]`, has `P(0)=0`, but `P'(0)=1`.

Therefore a checker that requires a square factor for **every** zero would falsely reject valid boundary cells.

The exact endpoint adapter is simpler. If `P(0)=0`, supply a lower-degree polynomial `Q` with exact identity

```text
P(t)=t*Q(t).                                              (5.1)
```

Since `t>=0` on `[0,1]`, any certificate `Q>=0` implies `P>=0`. Similarly, at the right endpoint supply

```text
P(t)=(1-t)*Q(t).                                         (5.2)
```

For degree at most three, `Q` has degree at most two, so the endpoint branch reduces to the already tiny quadratic Bernstein/factor gate.

This branch also handles polynomials such as `t*(1-t)` without pretending either endpoint root has even multiplicity.

---

## 6. Simple-root negative control: a zero is not enough

A future checker must not infer nonnegativity merely because it found an exact rational root and can split there.

Take

```text
W(t) = (t-1/3)*(t-2/3).
```

Then

```text
W(0)=W(1)=2/9 > 0,
```

but

```text
W(1/2) = -1/36 < 0.                                     (6.1)
```

Both interior roots are simple. Splitting at `1/3` or `2/3` does not create a nonnegative certificate across the full parent; the quotient changes sign.

Therefore the sound zero-contact protocol is:

```text
interior root:
    verify repeated-root/factor identity + factor sign;
endpoint root:
    verify one-sided endpoint factor identity + quotient sign;
otherwise:
    remain SUBDIVIDE/UNDECIDED unless an exact negative point is found.
```

This is a genuine mathematical distinction, not a provenance/admission convention.

---

## 7. Complete low-degree escape from the dyadic zero-contact stall

Combine `T-P5-055` with the present factor branch for a rational polynomial `P` of degree at most three on `[0,1]`.

There are only three mathematical cases.

### Case 1 — strict positivity

If

```text
P(t)>0 for every t in [0,1],
```

`T-P5-055` gives a finite dyadic depth at which every Bernstein control on every child is positive.

### Case 2 — nonnegative with zero contact

If `P>=0` and has a zero:

- an interior zero is repeated by Section 1 and rational by Section 4; degree `<=3` therefore yields the exact square-times-linear certificate of Sections 2-3;
- an endpoint zero is rational trivially and reduces by (5.1) or (5.2) to degree `<=2`.

Thus every nonnegative rational degree-`<=3` polynomial has a finite exact certificate using

```text
Bernstein strict-positive cells
    + repeated-root factor cells
    + endpoint-factor cells.
```

### Case 3 — negativity somewhere

If `P(t0)<0` at some real point, continuity gives an open negative interval. Dyadic rationals are dense, so some exact dyadic rational `q` satisfies

```text
P(q)<0.
```

Hence exhaustive dyadic refinement/evaluation eventually yields a genuine rational counterexample.

### T-P5-056-C — certificate-level completeness statement

For rational `P` with `deg P<=3`, the combination

```text
exact Bernstein subdivision
+ exact rational point evaluation
+ exact repeated-root/endpoint factor certificates
```

is complete for deciding `P>=0` on `[0,1]` at the mathematical certificate level.

The trusted verifier does **not** need a trusted polynomial root solver or gcd implementation. Root/factor discovery can be an untrusted search phase because every successful branch reduces to a ring identity plus ordered rational inequalities.

This closes exactly the zero-contact hole left open by `T-P5-055` for the one-dimensional affine-cell P5 remainders.

---

## 8. Direct impact on the P5 branch-free packet

For an affine source cell, `T-P5-052` already establishes

```text
deg Rtr <= 2,
deg Rdet <= 3.
```

Therefore a fail-closed exact checker can now use the following order:

```text
1. Form signed correlated Rtr/Rdet first.
2. Try Bernstein nonnegative controls on the current cell.
3. If a remainder has a negative exact rational point, return obstruction.
4. If controls remain negative only because of zero contact:
   a. interior contact -> repeated-root factor certificate;
   b. endpoint contact -> endpoint factor reduction.
5. Otherwise subdivide.
```

The important point is that step 4 acts on the **complete correlated remainder** `Rdet`, not on separately intervalized pieces such as `4ps-sigma^2` and the bias quadratic. This preserves the cancellation discipline of `T-P5-054`.

For the near-singular perturbation lane of `T-P5-054`, the same rule applies after forming the certified actual lower polynomial/enclosure. A zero determinant reserve is not automatically failure; if the complete correlated lower remainder factors with a valid zero-contact certificate, the nonstrict branch-free majorant may still PASS exactly.

A downstream theorem demanding a **strict** energy reserve must keep the distinction: a zero-contact certificate proves nonnegativity, not a positive uniform margin. It cannot be silently promoted into the strict-decay lane.

---

## 9. Minimal Lean/checker theorem surface

The first formalization should stay small and division-free.

### Quadratic

```text
quadratic_double_root_factor
```

Premises:

```text
b + 2*a*r = 0
c - a*r^2 = 0
```

Conclusion:

```text
a*t^2+b*t+c = a*(t-r)^2.
```

Then

```text
quadratic_nonneg_of_double_root_factor
```

adds `0<=a` and returns global nonnegativity.

### Cubic

```text
cubic_double_root_factor
```

Premises (3.1)-(3.2), conclusion (3.3).

```text
affine_nonneg_on_unit_of_endpoints
```

Premises `0<=L0`, `0<=L1`, `0<=t<=1`, conclusion `0<=(1-t)L0+tL1`.

```text
cubic_nonneg_of_double_root_factor
```

combines the previous two.

### Endpoint adapter

```text
nonneg_of_left_endpoint_factor
nonneg_of_right_endpoint_factor
```

consume an exact factor identity and a lower-degree nonnegativity premise.

### Regressions

```text
one_third_square_zero_contact_pass
```

for `(t-1/3)^2`.

```text
simple_root_split_not_nonnegative
```

for `(t-1/3)(t-2/3)` with witness `t=1/2`.

```text
endpoint_simple_root_is_valid
```

for `P(t)=t`, preventing the interior repeated-root rule from being applied at a boundary.

The ring equalities should be `ring`-level; ordered conclusions should need only square nonnegativity and `nlinarith`/linear convexity.

The rational-root existence theorem of Section 4 is useful documentation and completeness mathematics, but it need not be in the first trusted execution sidecar.

---

## 10. Boundaries / non-claims

This child does **not** prove:

- that deployed P5 source quantities are affine/polynomial on a real cell;
- any nominal-to-actual source enclosure from `T-P5-054`;
- Float64, libm, finite-difference, controller or solve soundness;
- same-key physical cell identity;
- P8/ODE/trajectory coverage;
- strict positive determinant/trace reserve at a zero-contact cell;
- Lean compilation, axioms, independent verification, comparator/admission or registry promotion.

Admission remains `pending mathematical child`.

The new mathematical conclusion is narrower and useful: **for rational degree <= 3 remainders, zero contact is not a reason to subdivide forever. Interior contact has a finite exact repeated-root factor certificate; endpoint contact has a separate one-sided factor certificate.** This is the correct branch-aware closure complement to `T-P5-055` strict-positive Bernstein completeness.
