# Review result — T-P4-040-RATIONAL-LAMBDA-GUARD

- agent: 狂蛮魔尊
- source_agent: 狂蛮魔尊
- status: pending mathematical child
- parent: T-P4-039 common-lambda feasibility
- scope: exact-rational robust interval / rounding guard for a common fixed `lambda`

## 0. Why this child exists

T-P4-039 gives an exact square-root-free decision for existence of a common real parameter across several convex quadratic rows.  That is an existence layer.  A source/checker implementation needs a slightly different object: a **rational interval with slack**, so that one rational/implemented `lambda` can be selected without sitting on a root and so that conservative coefficient widening can be charged without rerunning root algebra.

This note supplies that adapter.  It does not touch the currently owned DHProducerBaseBridge/source lane and does not claim any concrete cell coverage.

---

## 1. Reparameterization

Use the T-P4-039 fixed-`lambda` variable

` s := lambda - 1 `,

so admissibility requires `s > 0`.  A row has the form

`q_i(s) := P_i s^2 - G_i s + A_i <= 0`.                                      (1)

In the P4 use case `P_i >= 0`; hence each row is convex in `s`.

The point of this representation is that all checks below are polynomial/rational.  There are no roots, inverses, generalized eigenvalues, or floating-point decisions.

---

## 2. Exact endpoint identity

Let `a <= b`, `0 <= t <= 1`, and

`s = (1-t)a + t b`.

For any quadratic `q(s)=P s^2-G s+A`, direct expansion gives

`q(s) = (1-t) q(a) + t q(b) - P t(1-t)(b-a)^2`.                              (2)

This is the central identity.

If `P >= 0`, then the last term is nonpositive.  Therefore

`q(a) <= 0` and `q(b) <= 0`

imply

`q(s) <= 0` for every `s in [a,b]`.                                           (3)

Conversely, if every point of `[a,b]` is feasible then of course both endpoints are feasible.  Thus, for a **chosen interval**, endpoint feasibility is necessary and sufficient.

### Formalizable theorem statement

A Lean-facing statement can be kept completely elementary:

`convex_quadratic_endpoint_interval`

Assume

- `P >= 0`,
- `a <= b`,
- `0 <= t <= 1`,
- `q a <= 0`,
- `q b <= 0`,
- `s = (1-t)*a + t*b`.

Then `q s <= 0`.

Proof: first prove (2) by `ring`; then use `P*t*(1-t)*(b-a)^2 >= 0` and `nlinarith`.

---

## 3. Common-parameter robust interval for finitely many rows

For rows

`q_i(s)=P_i s^2-G_i s+A_i`, `P_i>=0`,

fix rational numbers

`0 < a <= b`.                                                                 (4)

If, for every row `i`,

`q_i(a) <= 0`,

`q_i(b) <= 0`,                                                                 (5)

then **every** `s in [a,b]` is a simultaneous witness for **all rows**.

Equivalently, every

`lambda in [1+a, 1+b]`                                                        (6)

is a common fixed-`lambda` witness.

This is stronger operationally than emitting one isolated rational lambda.  The checker can export `[a,b]` as a robustness interval and the implementation can choose any rational value inside it.

### Formalizable theorem statement

`common_lambda_interval`

Input: a finite row family plus a shared interval `[a,b]`; hypotheses are (4)-(5) and `P_i>=0`.  Output: for every row `i` and every `s in [a,b]`, `q_i(s)<=0`.

No pairwise root-overlap machinery is needed in this downstream lemma; T-P4-039 remains the existence/search layer, while this theorem is the implementation certificate.

---

## 4. Exact symmetric rounding radius around a nominal rational witness

Suppose a nominal common witness `s0>0` is already known.  For one row define its margin

`m := -q(s0) >= 0`,

and derivative coefficient

`d := 2 P s0 - G`.

For any `r>=0`, direct expansion gives

`q(s0+r) = -m + d r + P r^2`,                                                 (7)

`q(s0-r) = -m - d r + P r^2`.                                                 (8)

Because `P>=0`, `q` is convex, so the maximum of `q` on the closed interval `[s0-r,s0+r]` occurs at an endpoint.  Hence

`q(s) <= 0 for every |s-s0| <= r`

is equivalent to the pair of exact rational checks

`q(s0-r) <= 0`,

`q(s0+r) <= 0`.                                                               (9)

Equivalently, over the reals,

`P r^2 + |2 P s0-G| r <= m`.                                                  (10)

For a common lambda across many rows, require (9) rowwise.  To preserve `lambda>1`, additionally choose

`0 <= r < s0`.                                                                 (11)

The Lean/checker version should prefer the two endpoint inequalities (9), because they avoid introducing `abs` and division.

### Interpretation

This gives an exact **rounding tolerance**.  If an implementation chooses `s_impl` with

`|s_impl-s0| <= r`,

then every row remains valid.  The proof obligation for the Float64-to-real seam is then reduced to the separate statement that the realized `s_impl` lies inside this certified rational interval; this note does not claim that seam.

---

## 5. Conservative source/coefficient envelopes

Often a source/checker does not know exact `(P,G,A)` but only rational one-sided bounds.  Suppose for a row

`P <= P_up`,

`G_low <= G`,

`A <= A_up`,                                                                  (12)

and restrict to `s >= 0`.

Then

`q(s)=P s^2-G s+A`

is bounded above by

`q_up(s):=P_up s^2-G_low s+A_up`.                                             (13)

Indeed, for `s>=0`,

`P s^2 <= P_up s^2`,

`-G s <= -G_low s`,

`A <= A_up`.

If additionally

`P_up >= 0`,                                                                  (14)

then `q_up` is convex.  Consequently, for rational `0<a<=b`, the two checks

`q_up(a) <= 0`,

`q_up(b) <= 0`                                                                (15)

imply, simultaneously for **every coefficient realization satisfying (12)**,

`q(s) <= 0` for every `s in [a,b]`.                                           (16)

This is the useful source-widening theorem: uncertainty is pushed into one worst-case polynomial, and only its two rational endpoint values must be checked.

Note that the true `P` itself need not be nonnegative for this envelope theorem if it is pointwise dominated by a convex `q_up`; condition (14) is what makes the upper envelope convex.

### Formalizable theorem statement

`source_envelope_common_lambda_interval`

For every row, assume (12)-(14), `0<a<=b`, and (15).  Then every allowed realization of the row coefficients and every `s in [a,b]` satisfy the original row inequality.

Again the proof is just monotonicity plus `convex_quadratic_endpoint_interval`.

---

## 6. Failure evidence / assumptions that cannot be dropped

### 6.1 Convexity is essential for endpoint-only certification

Take

`q(s)=-(s-2)^2+1 = -s^2+4s-3`

on the positive interval `[1,3]`.  Here `P=-1<0` and

`q(1)=0`,

`q(3)=0`,

but

`q(2)=1>0`.

So endpoint PASS does **not** imply interval PASS without convexity (or a convex upper envelope).

### 6.2 A good midpoint is not a robustness certificate

Take

`q(s)=(s-1)(s-3)=s^2-4s+3`.

At `s0=2`,

`q(2)=-1`,

but at the positive points `s=1/2` and `s=7/2`,

`q(1/2)=q(7/2)=5/4>0`.

Thus one interior rational witness says nothing about how far it can be rounded.  The endpoint/radius checks are necessary for a claimed robustness interval.

### 6.3 The sign restriction `s>=0` is essential for the `G_low` envelope direction

The implication

`G_low <= G  =>  -G s <= -G_low s`

uses `s>=0`.  At `s=-1`, for example, `G=2`, `G_low=1` gives

`-G s = 2 > 1 = -G_low s`.

This is harmless for P4 because `s=lambda-1>0`, but it must be an explicit theorem hypothesis rather than an implicit convention.

---

## 7. Suggested checker contract

For each cell/common-row family, prefer emitting

- rational `s_lo,s_hi` with `0<s_lo<=s_hi`,
- per-row exact coefficients or one-sided envelopes `(P_up,G_low,A_up)`,
- exact endpoint values/witness inequalities at `s_lo,s_hi`.

Then the consumer proves that the entire interval is admissible.  A downstream implementation may select any rational

`s_impl in [s_lo,s_hi]`, `lambda_impl=1+s_impl`.

This is safer than exporting only one lambda and later trying to justify Float64 rounding post hoc.

If T-P4-039's exact pairwise feasibility test finds a nonempty real common interval, the search layer can pick rational endpoints strictly inside that common interval; this child certifies those endpoints and everything between them.  No algebraic root has to be stored in the artifact.

---

## 8. Minimal Lean sidecar

Suggested theorem decomposition:

1. `quadratic_chord_identity` — equation (2), `ring` only.
2. `convex_quadratic_endpoint_interval` — (2) + nonnegativity.
3. `common_lambda_interval` — finite-family reuse.
4. `symmetric_rounding_guard` — equations (7)-(9).
5. `source_envelope_quadratic_le` — pointwise dominance (12)-(13) for `s>=0`.
6. `source_envelope_common_lambda_interval` — dominance + endpoint theorem.
7. `negative_quadratic_endpoint_failure` — exact counterexample from §6.1.

No square roots, divisions, matrices, eigenvalues, or transcendental facts are required.

---

## 9. Status / non-claims

This is a **pending mathematical child** only.

It does **not** claim:

- concrete DHProducerBaseBridge/source binding,
- receipt/provenance/admission,
- concrete 5120-cell or other coverage,
- Float64/true-DH realization containment,
- P4/M4 closure,
- registry status change.

The intended downstream use is narrow: after the owned source lane produces rational row coefficients/envelopes, this adapter turns them into a robust common fixed-`lambda` interval with exact endpoint checks.
