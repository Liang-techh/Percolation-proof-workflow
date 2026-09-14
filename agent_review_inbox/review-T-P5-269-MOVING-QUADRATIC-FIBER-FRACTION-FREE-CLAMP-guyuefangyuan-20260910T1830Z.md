---
kind: review_result
review_id: review-T-P5-269-moving-quadratic-fiber-fraction-free-clamp-guyuefangyuan-20260910T1830Z
task_id: T-P5-269-MOVING-QUADRATIC-FIBER-FRACTION-FREE-CLAMP
reviewer: 古月方源
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T18:30:00Z
claim_commit: 2328b6777061082a68f3bad542415074d009fe45
inspected_commit: 94199e51011d429f9f76b5259ac22871626da073
upstream_commits:
  - bcebee5554c3a98dbe3a716407a21586f6367839  # T-P5-268 concave quadratic parameter clamp
  - 3f2f9004e7fe2c1a0f3fc315f59d33a2ed4dbde5  # T-P5-267 parametric radial box certificate
  - d062e528bc248cd24f09973dcde7cfcf7c00ffae  # T-P5-266 zero-margin radial Sturm certificate
  - 913ed31d66c77016e82fe2371d3734b033e76e5f  # T-P5-265 rational Bernstein radial interval certificate
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add_rational_moving_fiber_clamp; add_fraction_free_scaled_slack_identities; add_denominator_orientation_gate; add_endpoint_collision_dispatch; add_exact_reserve_shift; preserve_algebraic_branch_selector_boundary
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: exact symbolic expansion of fraction-free moving-endpoint identities; ordered-field clamp derivation; exact rational counterexamples; no provenance/receipt/admission audit and no Lean/kernel run
exit_code: not_applicable
---

# T-P5-269 — Rational moving quadratic fiber: exact fraction-free clamp

## 0. Verdict

**CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding.**

T-P5-268 closes the fixed interval

`A(q,s)=A0(q)+A1(q)s-A2(q)s^2`, `s in [a,b]`,

but explicitly leaves the source-faithful moving fiber

`s in [a(q),b(q)]`

open. This child proves that **rational moving endpoints do not create a genuinely bivariate optimization problem**. After orienting their denominators on a radial sign cell, every clamp predicate and every branch reserve is again the sign of a single polynomial in `q`.

More strongly, there are denominator-cleared LEFT and RIGHT interval certificates written directly in scaled endpoint slacks. They avoid division by `a(q)`, `b(q)`, or `b(q)-a(q)` and therefore fit the exact-rational / Sturm / Bernstein route already developed in T-P5-265/266.

The exact boundary is also identified. General algebraic endpoint functions still admit the pointwise clamp, but **cannot in general be reduced to signs of rational polynomials merely by taking a resultant/norm**. A branch selector (Thom encoding / algebraic root isolation) is then essential.

No deployed P5 endpoint packet, source equality proving the moving fiber, same-key `q/s`, state realizability, coverage, Float64 semantics, Lean/kernel proof, independent verification, admission, registry mutation, or parent closure is claimed.

---

## 1. Rational moving-fiber setup

Let

`I=[0,R]`, `R>0`,

and let

`A0,A1,A2 in Q[q]`.

Set

`C(q):=K-A0(q)`,

`p(q,s):=K-A(q,s)=C(q)-A1(q)s+A2(q)s^2`.

Write the moving endpoints in reduced rational form

`a(q)=Na(q)/Da(q)`,

`b(q)=Nb(q)/Db(q)`,

with `Na,Da,Nb,Db in Q[q]` and `gcd(Na,Da)=gcd(Nb,Db)=1`.

The main theorem is pointwise on a connected radial cell `J subset I` on which the denominators have been oriented so that

**(1.1)** `Da(q)>0`, `Db(q)>0`.

Define the fraction-free width numerator

**(1.2)** `L(q):=Nb(q)Da(q)-Na(q)Db(q)`.

Then

`b-a = L/(Da Db)`.

Hence `L>0` is exactly the nondegenerate endpoint-order condition `a<b` on that cell.

Define the denominator-cleared clamp derivatives

**(1.3)** `Ga:=Da A1-2Na A2`,

**(1.4)** `Gb:=Db A1-2Nb A2`.

Because `Da,Db>0`,

`sign(Ga)=sign(A1-2aA2)`,

`sign(Gb)=sign(A1-2bA2)`.

Define the endpoint debit numerators

**(1.5)** `Ea:=Da^2 C-Na Da A1+Na^2 A2`,

**(1.6)** `Eb:=Db^2 C-Nb Db A1+Nb^2 A2`,

and the interior debit

**(1.7)** `F:=4A2 C-A1^2`.

Then

`p(q,a)=Ea/Da^2`,

`p(q,b)=Eb/Db^2`.

All quantities `L,Ga,Gb,Ea,Eb,F` lie in `Q[q]`.

---

## 2. Theorem A — exact moving clamp stays univariate

Assume on one radial point/cell

**(2.1)** `Da>0`, `Db>0`, `L>0`, `A2>=0`.

Then `A(q,s)<=K` for every `s in [a(q),b(q)]` is equivalent to the following deterministic branch test:

### LEFT

If

**(2.2)** `Ga<=0`,

then safety is exactly

**(2.3)** `Ea>=0`.

### RIGHT

If `Ga>0` and

**(2.4)** `Gb>=0`,

then safety is exactly

**(2.5)** `Eb>=0`.

### INTERIOR

If

**(2.6)** `Ga>0` and `Gb<0`,

then automatically `A2>0`, and safety is exactly

**(2.7)** `F>=0`.

### Proof

After division by the positive denominators,

`ga:=Ga/Da=A1-2aA2`,

`gb:=Gb/Db=A1-2bA2`.

Moreover

**(2.8)** `ga-gb=2(b-a)A2>=0`.

Thus the fixed-`q` function `p(s)=C-A1 s+A2 s^2` is convex, and its minimum on the moving interval is attained at the left endpoint, right endpoint, or unique stationary point according to exactly the three derivative-sign branches above. Endpoint debit signs are the signs of `Ea,Eb`, and the interior minimum is `F/(4A2)`. In the INTERIOR branch, `ga>0>gb` and (2.8) force `A2>0`, so no extra denominator-safety assumption is needed. QED.

The important point is not the optimizer itself but the algebraic type: **moving rational endpoints increase degree, but not variable dimension**.

---

## 3. Theorem B — denominator-cleared LEFT/RIGHT identities

The preceding argument can be made fully fraction-free, including the interval geometry.

For a state `s in [a,b]`, define the scaled nonnegative slacks

**(3.1)** `x:=Da s-Na = Da(s-a)>=0`,

**(3.2)** `y:=Nb-Db s = Db(b-s)>=0`.

Then the following polynomial identities hold exactly.

### LEFT identity

**(3.3)**

`L Da^2 p`

`= (-Ga) Da x y`

`  + L Ea`

`  + (L A2-Ga Db) x^2`.

Under `L>0`, `Da,Db>0`, `A2>=0`, `Ga<=0`, every coefficient on the right is nonnegative except only the explicit reserve term `Ea`. Therefore

`Ea>=0  ->  p>=0`

without dividing by `Da`, `Db`, or `L`.

### RIGHT identity

**(3.4)**

`L Db^2 p`

`= Gb Db x y`

`  + L Eb`

`  + (L A2+Gb Da) y^2`.

Under `Gb>=0`, all structural coefficients on the right are nonnegative, so

`Eb>=0  ->  p>=0`.

### INTERIOR identity

The fixed-interval identity survives unchanged:

**(3.5)**

`4A2 p=(2A2 s-A1)^2+F`.

Hence the moving-fiber clamp has a completely division-free certificate on every rational denominator/order cell.

The identities (3.3) and (3.4) were checked by exact symbolic expansion; they are plain commutative-ring identities and are suitable Lean leaves before any polynomial sign dispatcher is formalized.

---

## 4. Clamp gluing remains fraction-free

The endpoint/interior seam identities become

**(4.1)** `Da^2 F = 4A2 Ea-Ga^2`,

**(4.2)** `Db^2 F = 4A2 Eb-Gb^2`.

These follow by direct expansion. Consequently, at a branch switch `Ga=0` or `Gb=0`, the selected endpoint debit and interior debit agree after multiplication by a positive factor. No algebraic-root evaluation of a quotient is needed merely to glue the branches.

This matters for a Sturm sign atlas: open sign cells can be handled by rational sample points, while branch-root points close by continuity and (4.1)-(4.2).

---

## 5. Exact reserve transport

Let `eta in Q`, `eta>=0`, and seek the stronger statement

`p(q,s)>=eta`

throughout the moving fiber.

Define

**(5.1)** `Ea_eta:=Ea-eta Da^2`,

**(5.2)** `Eb_eta:=Eb-eta Db^2`,

**(5.3)** `F_eta:=F-4eta A2`.

Then Theorem A remains exact after replacing `Ea,Eb,F` by `Ea_eta,Eb_eta,F_eta`.

The fraction-free identities are literally (3.3)-(3.5) with `p` replaced by `p-eta` and the corresponding reserve polynomial replaced as above. The gluing identities become

**(5.4)** `Da^2 F_eta=4A2 Ea_eta-Ga^2`,

**(5.5)** `Db^2 F_eta=4A2 Eb_eta-Gb^2`.

Thus source-dependent endpoint motion consumes no mysterious extra slack: its effect is already encoded exactly in the endpoint numerator polynomials.

---

## 6. Endpoint collision is a separate exact branch, not a failure

T-P5-268 assumes a fixed positive width. A moving fiber can collapse.

If

**(6.1)** `L(q)=0`,

then `a(q)=b(q)` and the physical fiber at that `q` is a singleton. Safety is simply

**(6.2)** `Ea>=0`

(or equivalently `Eb>=0`). Indeed

**(6.3)** `Db^2 Ea = Da^2 Eb`

when `L=0`.

For reserve `eta`, replace `Ea,Eb` by `Ea_eta,Eb_eta`.

Therefore the correct radial dispatcher is:

`L>0 -> moving clamp`,

`L=0 -> singleton endpoint evaluation`,

`L<0 -> endpoint-order semantics must be resolved`.

If `a,b` are typed as lower/upper endpoints, `L<0` is a source-geometry inconsistency / lane-not-applicable event, not a physical Lyapunov FAIL. If the source explicitly declares them only as an unordered endpoint pair, the checker may swap them on a sign cell after recording that semantic rule.

When an isolated `L=0` point is the limit of valid positive-width cells, the minimum debit is continuous in `q`, so a PASS with reserve on the neighboring cells extends to the collision point. If `L` is identically zero on a cell, use the singleton branch directly.

---

## 7. Denominator orientation is a theorem gate

A rational endpoint denominator cannot be silently cleared with unknown sign.

After gcd cancellation, partition `I` at real roots of `Da Db`. On each zero-free connected cell the sign of each denominator is constant. Multiply numerator and denominator by `-1` when necessary so that (1.1) holds.

If a reduced denominator has a genuine root inside the declared source cell, the endpoint is undefined there. The moving-rational-fiber theorem is then not applicable across that root unless the source provides a removable-cancellation identity or splits/excludes the singular point.

### Counterexample: unsigned denominator clearing can produce a false PASS

Take

`q in [0,1/2]`,

`a(q)=1/(q-1)`, `b(q)=0`,

`A(q,s)=s`, `K=-1/2`.

The true interval is `[a(q),0]`, and the true maximum is `A(q,0)=0>-1/2`, so safety FAILS everywhere.

Here `A2=0`, `A1=1`, hence the true left derivative is `ga=1>0`; the RIGHT endpoint must be checked. But if one naively forms `Ga=(q-1)A1<0` and forgets that `Da=q-1<0`, one incorrectly selects LEFT. At the left endpoint

`p(a)=-1/2-1/(q-1)>0`,

so this mistake yields a false PASS.

Normalize instead to

`a=(-1)/(1-q)` with `Da=1-q>0`.

Then `Ga=1-q>0`, RIGHT is selected, and `p(b)=-1/2<0` correctly rejects safety.

This is a mathematical soundness gate, not bookkeeping.

---

## 8. Exact one-dimensional dispatcher

For rational endpoints the full moving-fiber problem can be decided by a one-dimensional sign atlas in `q`.

On each denominator-oriented cell:

1. certify `L>=0` and `A2>=0`;
2. partition open nondegenerate cells by roots of `Ga Gb`;
3. use LEFT / RIGHT / INTERIOR according to the sign pair;
4. certify the corresponding `Ea_eta`, `Eb_eta`, or `F_eta` nonnegative;
5. handle `L=0` by the singleton rule;
6. glue branch roots by (5.4)-(5.5) and continuity.

Every object involved is in `Q[q]`. Therefore:

- T-P5-265 gives a finite Bernstein certificate whenever the desired reserve is strict;
- T-P5-266 gives a complete exact zero-margin Sturm/multiplicity decision for each univariate rational polynomial;
- no tensor-product Bernstein box in `(q,s)` is required for this structured lane.

Degree growth is explicit. If `deg` denotes polynomial degree, then for example

`deg Ga <= max(deg Da+deg A1, deg Na+deg A2)`,

`deg Ea <= max(2deg Da+deg C, deg Na+deg Da+deg A1, 2deg Na+deg A2)`,

and similarly for `Gb,Eb`; while

`deg L <= max(deg Nb+deg Da, deg Na+deg Db)`,

`deg F <= max(deg A2+deg C, 2deg A1)`.

So moving rational geometry may raise the Sturm degree substantially, but it does not raise the semialgebraic dimension.

---

## 9. Source fidelity can strictly improve the answer over a fixed outer box

A fixed outer parameter box is sound for PASS but can create a spurious FAIL.

Take

`q in [0,1]`,

`A(q,s)=s-q`, `K=0`,

with the true moving fiber

`s in [0,q]`.

Then

`max_{0<=s<=q} A(q,s)=0`

for every `q`, so the true moving-fiber gate is exactly safe.

If one replaces the source by the fixed outer box `s in [0,1]`, then at `(q,s)=(0,1)` one gets

`A(0,1)=1>0`.

Thus the fixed box declares a counterexample that is impossible under the real source relation. T-P5-269 removes precisely this avoidable loss when the endpoint functions are available.

At `q=0` the true fiber collapses to the singleton `{0}`, demonstrating why the collision branch in Section 6 is not optional.

---

## 10. General algebraic endpoints: pointwise clamp survives, pure Q[q] elimination does not

Suppose instead that an endpoint is a selected real algebraic branch `z=a(q)` satisfying

`P_a(q,z)=0`.

The pointwise quadratic clamp is still exact. The endpoint derivative and debit are

`g_a=A1-2zA2`,

`e_a=C-zA1+z^2 A2`.

Candidate `q` values where their signs can change are contained in resultant zero sets such as

`Res_z(P_a, A1-2zA2)=0`,

`Res_z(P_a, C-zA1+z^2A2-eta)=0`.

However, **the sign of a resultant/norm does not determine the sign on the selected physical algebraic branch**. Conjugate roots are multiplied together.

A constant exact regression makes this unavoidable. Let the physical branch be

`z=sqrt(2)`, `P(z)=z^2-2`.

For `H(z)=z-3`,

`H(sqrt(2))<0`,

but

`Res_z(z^2-2,z-3)=7>0`.

Thus replacing the selected-branch sign by a resultant sign would reverse the answer.

The correct general algebraic dispatcher must carry a branch selector, e.g. an isolating interval / Thom encoding, and use subresultant or algebraic-number sign evaluation on each radial cell. This is still essentially one-dimensional in the base variable `q`, but it is **not** the same pure `Q[q]` fraction-free packet proved for rational endpoints.

Special algebraic endpoints can still collapse back to `Q[q]` when a sign-preserving elimination identity is proved with all side conditions. Blind squaring or taking norms is not such a proof.

---

## 11. Theorem-level structural fingerprint

The reusable fingerprint is

`quadratic nuisance parameter + moving rational source fiber`

`-> reduce endpoint fractions`

`-> split/orient denominator signs`

`-> L=Nb*Da-Na*Db`

`-> L>0: nondegenerate moving interval`

`-> Ga=Da*A1-2*Na*A2, Gb=Db*A1-2*Nb*A2`

`-> Ea=Da^2*C-Na*Da*A1+Na^2*A2`

`-> Eb=Db^2*C-Nb*Db*A1+Nb^2*A2`

`-> LEFT: Ga<=0 and Ea>=0`

`-> RIGHT: Ga>0, Gb>=0 and Eb>=0`

`-> INTERIOR: Ga>0>Gb and F=4*A2*C-A1^2>=0`

`-> one-dimensional Sturm/Bernstein atlas in q`

`-> L=0: singleton endpoint evaluation`

`-> algebraic endpoint: require explicit branch selector; resultant alone is insufficient`.

---

## 12. Minimal Lean theorem statements

The recommended first formalization is pointwise over a linear ordered field; polynomial/Sturm integration should come later.

### Leaf 1 — rational endpoint sign transport

Assume `Da>0`. For `a=Na/Da`,

`sign(A1-2*a*A2)=sign(Da*A1-2*Na*A2)`.

Likewise for `b`.

### Leaf 2 — moving LEFT ring identity

With

`L=Nb*Da-Na*Db`,

`x=Da*s-Na`, `y=Nb-Db*s`,

`Ea=Da^2*C-Na*Da*A1+Na^2*A2`,

`Ga=Da*A1-2*Na*A2`,

prove

`L*Da^2*p = (-Ga)*Da*x*y + L*Ea + (L*A2-Ga*Db)*x^2`.

This is `ring` / `ring_nf` only.

### Leaf 3 — moving RIGHT ring identity

Prove

`L*Db^2*p = Gb*Db*x*y + L*Eb + (L*A2+Gb*Da)*y^2`.

### Leaf 4 — moving clamp LEFT/RIGHT soundness

From positivity of `Da,Db,L`, nonnegativity of `A2,x,y`, the branch derivative sign, and the endpoint reserve, conclude `p>=0` using Leaf 2 or 3.

### Leaf 5 — interior completed square

`4*A2*p=(2*A2*s-A1)^2+F`.

### Leaf 6 — branch gluing

`Da^2*F=4*A2*Ea-Ga^2`,

`Db^2*F=4*A2*Eb-Gb^2`.

### Leaf 7 — reserve shift

Replace `p` by `p-eta`, `Ea` by `Ea-eta*Da^2`, `Eb` by `Eb-eta*Db^2`, and `F` by `F-4*eta*A2` in Leaves 2-6.

### Leaf 8 — singleton fiber

Under `Da,Db>0` and `L=0`, prove `a=b` and

`Db^2*Ea=Da^2*Eb`.

These leaves avoid rational-function normalization inside the final inequality proof: all difficult divisions are isolated in the endpoint interpretation layer.

---

## 13. Remaining obligations and fail-closed semantics

Still open:

1. actual P5 source identity producing rational/algebraic `a(q),b(q)`;
2. proof that these functions describe the true same-key parameter fiber rather than an outer/inner surrogate;
3. denominator reduction and sign/orientation on the actual radial cell;
4. endpoint-order semantics, including whether label swapping is authorized;
5. actual `A2>=0` and branch polynomial extraction;
6. same-key `q`, metric, chart and source parameter binding;
7. state/source realization of any candidate violation;
8. cell/trajectory/flowed-sheet/FD-halo/reference-halo coverage;
9. Float64/libm/interval semantics;
10. Lean/kernel formalization;
11. independent verification by 封不觉;
12. admission, registry mutation, or P5 parent closure.

A failed denominator/order/source-binding gate is **MOVING_FIBER_LANE_NOT_APPLICABLE**, not physical FAIL. A negative branch reserve is a mathematical counterexample for the declared moving fiber; it upgrades to a physical/source FAIL only when the source fiber and state realization are proved.

---

## 14. Requested next step

The source-facing next step should first inspect the actual P5 coefficient packet.

- If the real endpoints are rational functions, bind their exact `Na/Da,Nb/Db` to the same source key and run the present univariate dispatcher directly. This is preferable to another generic bivariate relaxation.
- If the real endpoints are algebraic, the next independent mathematical child should be an **algebraic moving-fiber branch-selector theorem**: selected-root / Thom-encoding transport for `Ga,Ea` signs, with resultant/subresultant breakpoints but without replacing selected-branch signs by norms.
- If the source only provides a coupled relation `P(q,s)>=0` rather than endpoint functions, that is a genuinely different semialgebraic-fiber problem and should not be hidden behind fictitious `a(q),b(q)`.

This preserves the exact one-dimensional path whenever the source geometry truly permits it, and records the precise point where stronger real-algebraic machinery becomes necessary.