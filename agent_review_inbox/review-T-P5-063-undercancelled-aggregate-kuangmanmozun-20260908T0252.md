---
kind: review_result
review_id: review-T-P5-063-undercancelled-aggregate-kuangmanmozun-20260908T0252
task_id: T-P5-063-UNDERCANCELLED-AGGREGATE-GATE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: 2026-09-08T02:33:00-06:00
created_at: 2026-09-08T02:52:00-06:00
claim_commit: 9a6a5e7292d77174cd89c05730b1076c343b15a9
parent_tasks:
  - T-P5-057-RADICAL-FACTOR-CANCEL
  - T-P5-061
  - T-P5-062-MULTIFACTOR-LIPSCHITZ-STRATA
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: add an exact aggregate integer-valuation gate for monomial consumers containing individually under-cancelled radical channels, with a sharp full-box obstruction and an exact correlated-source monomial pullback rescue theorem
---

# T-P5-063 — under-cancelled aggregate valuation gate

## 0. Bottleneck and non-overlap

T-P5-061 explicitly leaves **channels with under-cancelled active factors** open. T-P5-062 then assumes, channel by channel,

`q_{i,a} >= m_{i,a}`,

so all excess orders `k_{i,a}=q_{i,a}-m_{i,a}` are nonnegative before a consumer monomial is formed.

That assumption is safe but can be strictly too strong for nonlinear consumers. An individual normalized channel may blow up like `1/|h|`, while another factor in the *same exact consumer monomial* vanishes like `|h|`; their product can be bounded, continuous, or even identically constant. Thus

> `one channel is under-cancelled => reject every consumer containing it`

is not a valid general mathematical rule.

This child removes the per-channel nonnegative-order requirement at the **consumer monomial** level. The correct structural object is the **aggregate integer valuation vector**. It also isolates the precise condition under which a negative factor-space valuation is a genuine obstruction and when exact source geometry can rescue it.

This does not redo T-P5-062's `k>=0` quantitative Lipschitz estimates, T-P5-061 parity/reachability, or any source/Float64/provenance/admission lane.

---

## 1. Generalized radical packet with integer excess

For active analytic factors `h_1,...,h_r`, suppose channel `i` has the exact punctured factorization

`A_i = S_i * prod_a h_a^(2 m_{i,a})`,

`G_i = J_i * prod_a h_a^(q_{i,a})`,

with `m_{i,a},q_{i,a} in N`, `S_i>0`, but **do not assume** `q_{i,a}>=m_{i,a}`.

Set

`k_{i,a} := q_{i,a}-m_{i,a} in Z`,

`v_i := J_i/sqrt(S_i)`.

Away from the active zero surfaces,

**(1.1)**

`u_i = G_i/sqrt(A_i)`

`    = [prod_a sign(h_a)^(q_{i,a}) |h_a|^(k_{i,a})] v_i`.

Now take one exact consumer monomial

`M(u)=prod_i u_i^(n_i)`, `n_i in N`.

Define its aggregate data

**(1.2) net valuation**

`E_a := sum_i n_i (q_{i,a}-m_{i,a}) in Z`,

**(1.3) sign parity**

`beta_a := (sum_i n_i q_{i,a}) mod 2`,

and reduced monomial

`R := prod_i v_i^(n_i)`.

Then exactly on every punctured sign chamber,

**(1.4)**

`M = Psi_(E,beta)(h) R`,

where

`Psi_(E,beta)(h) := prod_a sign(h_a)^(beta_a) |h_a|^(E_a)`.

The only difference from T-P5-062 is crucial: `E_a` is now an **integer**, and may be nonnegative even though some participating `k_{i,a}` are negative.

---

## 2. Exact full-box structural gate

Assume first that the factor coordinates are genuinely independent: the source neighborhood contains a punctured product box

`0 < |h_a| <= H_a`

for every active coordinate, with every partial stratum approachable while the other `h_b` are fixed nonzero.

The statement below is deliberately **universal in the reduced packet**. This is what makes it a structural gate rather than a hidden source-specific vanishing assumption.

### Theorem 2.1 — universal boundedness iff aggregate valuations are nonnegative

For the scalar factor `Psi_(E,beta)`, the following are equivalent:

1. `Psi_(E,beta) R` is bounded on the punctured box for every bounded reduced packet `R`;
2. `E_a >= 0` for every active factor `a`.

When these conditions hold and `|R|<=M_R`,

**(2.1)**

`|M| <= M_R * prod_a H_a^(E_a)`.

#### Proof

If all `E_a>=0`, the bound is immediate because every sign factor has absolute value one.

Conversely, if `E_j=-d<0` for some `j`, choose the admissible reduced packet `R=1`, fix every `h_a` for `a!=j` at any nonzero value, and let `h_j -> 0`. Then

`|M| = C |h_j|^(-d) -> infinity`

for a fixed `C>0`. Hence no universal finite bound exists.

So in an independent full box, **negative aggregate order is a genuine mathematical obstruction**, not a weakness of a Young/interval estimate.

### Theorem 2.2 — universal continuous/Lipschitz extension

On the same full box, `Psi_(E,beta)` has a continuous extension through every coordinate zero surface for all bounded continuous `R` if and only if, for every `a`,

**(2.2)**

`E_a > 0`,

or

`E_a = 0 and beta_a = 0`.

Equivalently,

**(2.3)**

`E_a>=0` for all `a`, and `beta_a=0` on every zero-net-order coordinate.

Because the `E_a` are integers, the same structural condition gives a locally Lipschitz contact factor. For every `E_a>0`, the one-dimensional factor is either

`|x|^(E_a)`

or

`sign(x)|x|^(E_a)=x|x|^(E_a-1)`,

both Lipschitz on `[-H_a,H_a]` with constant `E_a H_a^(E_a-1)`.

Thus the T-P5-062 product estimate applies **after aggregation**, even when individual channels have negative excess.

The necessity of the parity clause is sharp: if `E_a=0,beta_a=1`, fixing all other coordinates gives opposite nonzero one-sided values. If `E_a<0`, boundedness already fails before parity matters.

---

## 3. Exact rescue: an individually divergent channel can be harmless in the consumer

Take one real factor `h` and two normalized channels with exact data

**channel 1**

`A_1=h^4`, `G_1=h`.

Then `m_1=2`, `q_1=1`, hence

`u_1 = h/|h|^2 = 1/h` for `h!=0`.

This channel is under-cancelled by one order and diverges.

**channel 2**

`A_2=h^4`, `G_2=h^3`.

Then `m_2=2`, `q_2=3`, hence

`u_2 = h^3/|h|^2 = h`.

Now take the exact nonlinear consumer

`M=u_1 u_2`.

Its aggregate data are

`E=(-1)+(+1)=0`,

`beta=(1+3) mod 2 = 0`.

And in fact, for every `h!=0`,

**(3.1)**

`M=(1/h)h=1`.

So the product extends as the constant `1`, with Lipschitz constant `0`.

This is an exact counterexample to any checker rule that rejects a nonlinear consumer merely because **one participating channel** has `q<m`.

The safe decision point is the aggregate consumer valuation, not the individual channel valuation.

---

## 4. Negative aggregate order cannot be repaired by parity

Parity only controls side dependence; it cannot repair a pole.

Using the same under-cancelled channel `u_1=1/h`, consider the square consumer

`M=u_1^2=1/h^2`.

Now the aggregate parity is even,

`beta=0`,

but the aggregate valuation is

`E=-2`.

Thus `M -> +infinity` as `h->0`.

So a proposed rule

> `even parity => contact-safe`

is false once under-cancelled orders are admitted. The gate order must be:

1. first exclude/repair negative aggregate valuations;
2. only then apply the parity/reachable-sign gate at the zero-net-order coordinates.

---

## 5. Polynomial sums: why monomial fail-fast is safe only after exact cancellation handling

The monomial theorem is exact, but a polynomial consumer may have **source-proved cancellation between singular terms**.

For example, take two identical under-cancelled channels

`u_1=u_2=1/h`

and the polynomial consumer

**(5.1)**

`F=u_1-u_2`.

Each monomial separately has aggregate order `-1`, yet the exact source identity gives

`F=0`.

Therefore the following global rule is also too strong:

> `one polynomial term has negative valuation => the whole polynomial is impossible`.

A sound workflow is:

- first perform exact CSE / algebraic collection and consume any proved identities;
- then apply the present valuation gate monomialwise to the remaining canonical terms;
- if a negative-order term remains, reject the independent full-box packet **unless** the source supplies an additional exact cancellation/vanishing theorem.

For a universal polynomial packet whose reduced monomials are treated as algebraically independent, no cancellation between distinct reduced monomials may be inferred: a negative-order monomial gives a valid adversarial reduced packet and hence a genuine obstruction.

This distinction is important for the checker: **do not guess cancellation from samples**, but also do not forbid an exact symbolic cancellation already proved by the source layer.

---

## 6. Correlated source geometry can rescue a negative factor-space valuation

The full-box obstruction uses the fact that each `h_a` can approach zero independently while the others stay nonzero. That can fail on a constrained source domain.

The simplest example is a source curve

`h_1=z`,

`h_2=z^2`.

Consider a contact monomial with factor-space valuation

`E=(-1,+1)`.

As a function of independent `(h_1,h_2)`, the magnitude

`|h_1|^(-1)|h_2|`

is unbounded near `h_1=0` if `h_2` is fixed nonzero.

But on the certified source curve,

**(6.1)**

`|h_1|^(-1)|h_2| = |z|^(-1)|z|^2 = |z|`,

which vanishes and is Lipschitz.

Thus `E_a>=0` is exact for an **independent factor box**, but is not a necessary condition on an arbitrarily constrained source manifold.

This is not a loophole: the rescue must be justified by a source-domain relation, not inferred from numerical samples.

---

## 7. Exact monomial-pullback theorem for correlated geometry

There is a clean typed interface that makes the correlated rescue exact and still keeps the trusted checker integer/rational.

Assume local independent source coordinates `z_1,...,z_d` and an exact monomial factor map

**(7.1)**

`h_a(z) = c_a * prod_j z_j^(W_{a j})`,

where

- `W_{a j} in N` is an exact exponent matrix;
- every `c_a` is a fixed nonzero constant.

For a consumer packet `(E,beta)`, define the pulled-back data

**(7.2) pulled-back valuation**

`E'_j := sum_a W_{a j} E_a in Z`,

**(7.3) pulled-back parity**

`beta'_j := (sum_a W_{a j} beta_a) mod 2`.

Then, away from the coordinate zero sets,

**(7.4)**

`Psi_(E,beta)(h(z))`

`= C * prod_j sign(z_j)^(beta'_j) |z_j|^(E'_j)`,

where `C` is a fixed nonzero constant determined by the `c_a`, including their signs and integer powers.

### Theorem 7.1 — exact pullback gate

On a full product box in the independent `z` coordinates, the pulled-back contact factor is universally bounded iff

**(7.5)**

`E'_j>=0` for every `j`.

It has a universal continuous/Lipschitz extension iff, for every `j`,

**(7.6)**

`E'_j>0`,

or

`E'_j=0 and beta'_j=0`.

This is simply Theorems 2.1–2.2 after the exact exponent transport

**(7.7)**

`E' = W^T E`, `beta' = W^T beta mod 2`.

No roots, limits, optimization, or floating arithmetic are needed in the decision layer.

### Sharp threshold on the curve example

For `h_1=z`, `h_2=z^2`, the exponent matrix is the column

`W=(1,2)^T`.

For `E=(-1,1)`,

`E'=1*(-1)+2*(1)=1>0`,

so the pullback vanishes: PASS.

For `E=(-2,1)`,

`E'=0`; boundedness holds, but continuity now depends exactly on pulled-back parity `beta'`.

For `E=(-3,1)`,

`E'=-1`; the pullback has a true pole and FAILS.

Thus the weighted threshold is exact, not a heuristic.

---

## 8. Reachable-rate obstruction for more general source geometry

Even when a full monomial parameterization is unavailable, a certified one-parameter approach gives a cheap **one-sided obstruction witness**.

Suppose the source proves a reachable path with

`|h_a(t)| = c_a t^(w_a)`, `c_a>0`, `w_a>=0`, `t->0+`,

and the reduced factor tends to `R_0!=0`. Then

**(8.1)**

`|M(t)| = C t^(E dot w) |R(t)|`.

Hence:

- `E dot w < 0` => `|M(t)| -> infinity`: exact obstruction;
- `E dot w = 0` => finite nonzero magnitude is possible; sign/reachable-side compatibility decides continuity;
- `E dot w > 0` => this path is damped to zero.

So a counterexample-search agent can look for a certified reachable rate vector `w` with `E dot w<0`. One such vector is enough to rule out bounded closure.

Conversely, checking a few sampled rate vectors is **not** a proof of boundedness. A PASS requires either an exact parameterization such as Theorem 7.1, a complete certified rate cone plus a uniform comparison theorem, or another source-specific domination certificate.

---

## 9. Fail-fast / rescue protocol for P5 nonlinear consumers

For each canonical monomial after exact CSE:

1. compute integer aggregate valuation `E` and parity `beta`;
2. if the active factors are certified independent, require `E>=0` coordinatewise;
3. if some `E_a<0`, do **not** immediately blame the individual channels: first check whether the source packet supplies an exact correlated monomial map / stronger factorization / exact aggregate cancellation;
4. under an exact monomial source map, replace `(E,beta)` by `(W^T E, W^T beta mod 2)` and apply the same gate in independent source coordinates;
5. after all net valuations are nonnegative, apply the T-P5-061/T-P5-062 parity and quantitative Lipschitz machinery;
6. any certified reachable rate `w` with `E dot w<0` and nonzero reduced limit is a hard mathematical FAIL witness.

This separates three genuinely different situations:

- **individual pole but aggregate rescue** — allowed;
- **aggregate pole on an independent/reachable stratum** — impossible without extra cancellation;
- **negative factor-space order but correlated-domain rescue** — allowed only with a typed geometry theorem.

---

## 10. Lean-friendly theorem statements

No Lean lane is claimed here. The smallest useful formal leaves are:

1. `aggregate_integer_excess_identity`
   - collect `prod_i (sign(h)^q_i |h|^(q_i-m_i) v_i)^(n_i)` into integer net order and XOR parity on the punctured domain.

2. `negative_net_order_unbounded`
   - for natural `d>0`, `|x|^(-d)` has no finite upper bound on `0<|x|<=H`.

3. `aggregate_contact_safe_of_net_nonnegative`
   - if every aggregate order is nonnegative and every zero-order coordinate has even parity, reduce to the existing signed/unsigned natural-power Lipschitz lemmas.

4. `undercancelled_product_exact_rescue`
   - the regression `A1=A2=h^4`, `G1=h`, `G2=h^3` gives `(G1/sqrt(A1))*(G2/sqrt(A2))=1` for `h!=0`.

5. `monomial_pullback_exponent_transport`
   - under `h_a=c_a prod_j z_j^(W_aj)`, prove `E'=W^T E` and `beta'=W^T beta mod 2`.

6. `monomial_pullback_contact_gate`
   - consume item 5 plus the full-box gate in `z` coordinates.

7. `negative_weighted_rate_obstruction`
   - if `E dot w<0` and the reduced packet has a nonzero limiting lower bound, the consumer is unbounded along the certified power-law path.

The integer-exponent representation can avoid a general `zpow` API in the trusted core by splitting `E=E_+-E_-` and cross-multiplying on the punctured domain.

---

## 11. Status boundary

**Result:** mathematical child complete; integration pending.

**Closed here:**

- exact aggregate integer valuation for monomial consumers containing individually under-cancelled channels;
- full independent-box universal boundedness criterion `E>=0`;
- full-box continuous/Lipschitz criterion `E>=0` plus even parity on zero-net-order coordinates;
- exact rescue example where a divergent `1/h` channel participates in a constant consumer;
- exact even-parity counterexample showing negative order still blows up;
- exact warning that polynomial-level symbolic cancellation can rescue individually singular monomials;
- exact correlated-source monomial pullback `E'=W^T E`, `beta'=W^T beta mod 2`;
- exact weighted-path hard obstruction `E dot w<0`.

**Still open / not claimed:** concrete deployed source factorization, proof of factor independence or the monomial source map, nonconstant analytic-unit transport, exact aggregate cancellation discovery in a concrete CSE packet, source reachability/rate-cone completeness, reduced-packet bounds, Float64/libm/FD/controller/solve semantics, P8/ODE coverage, Lean/kernel compilation, comparator/receipt/provenance, parent closure, P5/P8/M4 admission, or registry mutation.