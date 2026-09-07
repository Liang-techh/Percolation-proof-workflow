---
kind: review_result
review_id: review-T-P5-009-liuguanyi-20260907T0606
task_id: T-P5-009
source_agent: 柳冠一
claimed_at: 2026-09-07T06:06:15-06:00
created_at: 2026-09-07T06:06:15-06:00
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_affine_envelope_adapters_and_route_positive_offset_to_additive_budget
---

# T-P5-009 — exact adapters for affine FD envelopes

## Scope and inspected inputs

This review addresses only the mathematical interface requested by `T-P5-009`.
It does not change the current `FDForceBudget.envelope`, does not claim a
true-DH/source binding, and does not close P5/M4.

Inspected inputs:

- `examples/routeb_dh_power_binding/FDForceBudget.lean`, blob
  `4e3a3ae56b5ec2708d0deeec2de786d0a0218e36`;
- `review-T-P5-005-kuangmanmozun-20260906T2307.md`, blob
  `65a1e212244e615568a07169889591ed2cb68c4f`.

The current component envelope is exactly

```text
|e_i| <= s_i * cap + b_i,
```

where `s_i = slope i` and `b_i = offset i`.  Channels 1--4 have
`b_i>0`, while channels 0 and 5 have `b_i=0`.

The question is what additional state/equilibrium contract is mathematically
sufficient to turn this affine enclosure into a homogeneous relative bound,
and what cannot be obtained from the current interface alone.

## 1. The exact floor adapter

Consider one scalar channel.  Assume

```text
|e| <= s*cap + b,                 s,b >= 0,
cap <= K*|x|,                     K >= 0,
|x| >= nu > 0.
```

Then

```text
|e| <= (s*K + b/nu) |x|.                         (A)
```

Proof:

```text
|e| <= s*cap+b
    <= s*K*|x|+b
    <= s*K*|x|+(b/nu)|x|.
```

The division-free form is

```text
nu*|e| <= (s*K*nu+b)*|x|.                         (A0)
```

Consequently, if a downstream coefficient `rho` satisfies

```text
s*K*nu+b <= rho*nu,
```

then `|e|<=rho|x|`.

This coefficient is sharp from the stated abstract information alone: if the
envelope, `cap<=K|x|`, and the floor can all saturate at `|x|=nu`, no smaller
uniform coefficient can be certified.

### Consequence for P5

If `x=v_i`, an affine FD cap can be made velocity-relative on a punctured
domain only after supplying BOTH

```text
cap <= K_i |v_i|
and
|v_i| >= nu_i > 0                 (when b_i>0).
```

For channels 0 and 5, `b_i=0`, so the floor is unnecessary, but the
`cap <= K_i|v_i|` bridge is still necessary.

For channels 1--4, the current positive offsets force the extra floor in an
envelope-only conversion.  A fixed `nu_i>0` is incompatible with any
Lyapunov neighborhood that contains the equilibrium or contains states with
`v_i` arbitrarily close to zero.  Therefore the floor adapter is useful only
for annular/punctured domains, not for the usual equilibrium-containing strict
stability domain.

## 2. Equilibrium anchoring by itself is NOT enough

A common tempting repair is to add only

```text
e(0)=0.
```

That is still insufficient to infer any finite relative gain from the current
affine envelope when `b>0`.

Indeed, fix any `b>0` and define on a neighborhood of zero

```text
E(0) = 0,
E(x) = b/2      for x != 0.
```

With `cap=0`, this satisfies

```text
|E(x)| <= b <= s*cap+b
```

for every `x`, and it satisfies the exact equilibrium condition `E(0)=0`.
But for every finite `rho>=0`, choose a sufficiently small nonzero `x`; then

```text
|E(x)| = b/2 > rho*|x|.
```

For example, `x=b/(4*(rho+1))` works.  Hence the existing pointwise envelope
plus exact equilibrium vanishing does not imply a Lipschitz/relative estimate.
This is stronger than the earlier `e(0)!=0` witness: even after imposing
`e(0)=0`, a quantitative increment contract is still missing.

No continuity or smoothness of the lifted Float64/source error is present in
the current abstract interface, so such regularity cannot be silently assumed.

## 3. The correct equilibrium adapter is a CENTERED INCREMENT bound

Let `z_*` be the equilibrium and let `g(z)>=0` be the state gauge required by
the consumer, with `g(z_*)=0`.  If the source/checker proves

```text
e(z_*) = 0,
|e(z)-e(z_*)| <= L*g(z),                            (B)
```

then immediately

```text
|e(z)| <= L*g(z).                                   (Brel)
```

For componentwise P5, take `g(z)=|v_i|`.  For a weighted/full-state consumer,
`g` can instead be the appropriate typed energy norm.

This is the minimal honest kind of extra source/state contract for an
equilibrium-containing domain.  The constant `offset i` in the existing FD
envelope is not reinterpreted or deleted: rather, the new centered increment
statement is additional information about the ACTUAL error map.  The old
pointwise affine cap alone cannot prove (B).

A slightly more structured sufficient contract is

```text
cap(z) <= K*g(z),
e(z) = e_slope(z) + e_rem(z),
|e_slope(z)| <= s*cap(z),
e_rem(z_*) = 0,
|e_rem(z)-e_rem(z_*)| <= L_rem*g(z).
```

Then

```text
|e(z)| <= (s*K+L_rem) g(z).                         (C)
```

The decomposition itself must be source-bound; the numerical inequality
`|e|<=s*cap+b` does NOT construct it.

## 4. Exact classification of the current six-channel FD interface

The offsets in the current checked file are

```text
b_0 = 0
b_1 = 68343 / 800000000000000
b_2 = 21909 / 1000000000000000
b_3 = 6867  / 8000000000000000
b_4 = 6867  / 4000000000000000
b_5 = 0.
```

Therefore:

1. Channels 0 and 5 can become componentwise relative from the existing
   envelope if one additionally proves `cap<=K_i|v_i|`; their legal gain is
   `rho_i=s_i*K_i`.
2. Channels 1--4 cannot become uniformly velocity-relative on any domain with
   `|v_i| -> 0` from the existing affine envelope alone.
3. On a punctured domain with `|v_i|>=nu_i>0`, the legal envelope-only gain is
   exactly `rho_i=s_i*K_i+b_i/nu_i`.
4. On an equilibrium-containing domain, the useful replacement contract is a
   centered increment estimate for the actual FD/source error, not an
   equilibrium value alone.

There is a second independent compatibility issue: even when `b_i=0`, the
current theorem does not state that `cap` is controlled by `|v_i|`.  Thus zero
offset is necessary but not by itself sufficient for the componentwise P5
relative premise.

## 5. Weighted-dual fallback that does NOT need a velocity floor

The positive offsets need not be discarded.  They can be routed honestly to
the additive finite-horizon/weighted-dual consumer rather than forced into a
homogeneous relative gain.

Let the positive damping coefficients be `d_i` and define

```text
Dual(e) := sum_i e_i^2/d_i,
S := sum_i s_i^2/d_i,
B := sum_i b_i^2/d_i.
```

From the current component envelope and `(a+b)^2 <= 2a^2+2b^2`,

```text
Dual(e) <= 2*S*cap^2 + 2*B.                         (D)
```

For the exact current repository coefficients,

```text
S = 98881705013075533
    / 15933555824784998400000000000000000,

B = 90362741420079
    / 12646400000000000000000000000000000.
```

If a separate same-domain state bridge supplies

```text
cap^2 <= K^2 * A(v),
A(v) := sum_i d_i*v_i^2,
```

then

```text
Dual(e) <= (2*S*K^2) A(v) + 2*B.                    (E)
```

This is a legal mixed relative-plus-additive SQUARED charge.  It does not
pretend that the actual error has been decomposed into two vectors.  The
constant `2B` can be sent to the additive finite-horizon route developed in the
P5 weighted-dual/barrier work, while the first term is a relative damping
charge.  If a pure strict-decay theorem is required, the additive term must
still be eliminated by a stronger centered source contract; (E) does not do
that.

The identity also explains the existing `polynomialBudget`: its constant term
is exactly `B/2` because that file charges `sum envelope_i^2/(2d_i)`.

## 6. Minimal theorem statements suggested for Lean

```lean
-- Envelope-only adapter on a punctured domain; division-free premise.
theorem affine_envelope_relative_of_floor
    (s b cap K nu x e rho : ℝ)
    (hs : 0 <= s) (hb : 0 <= b) (hK : 0 <= K) (hnu : 0 < nu)
    (henv : |e| <= s*cap+b)
    (hcap : cap <= K*|x|)
    (hfloor : nu <= |x|)
    (hbudget : s*K*nu+b <= rho*nu) :
    |e| <= rho*|x|
```

```lean
-- Equilibrium-containing adapter: source increment, not static offset.
theorem centered_increment_relative
    (err : X -> ℝ) (z z0 : X) (g : X -> ℝ) (L : ℝ)
    (h0 : err z0 = 0)
    (hinc : |err z - err z0| <= L*g z) :
    |err z| <= L*g z
```

```lean
-- Current affine envelope can be retained as mixed weighted-dual charge.
theorem affine_box_to_weighted_dual_mixed
    (d s b e : Fin 6 -> ℝ) (cap : ℝ)
    (hd : forall i, 0 < d i)
    (hs : forall i, 0 <= s i)
    (hb : forall i, 0 <= b i)
    (hcap : 0 <= cap)
    (he : forall i, |e i| <= s i*cap+b i) :
    (sum i, e i^2/d i)
      <= 2*(sum i, s i^2/d i)*cap^2 + 2*(sum i, b i^2/d i)
```

A small explicit counterexample theorem should also be retained to prevent a
future adapter from accidentally assuming that `err z0=0` implies a relative
bound under the affine cap.

## 7. Recommended integration boundary

The current `FDForceBudget.envelope` should NOT be changed to hide its positive
offsets.  Instead downstream source adapters should choose one of three typed
routes explicitly:

```text
zero-offset + cap/state compatibility
    -> homogeneous relative bound;

positive offset + state floor
    -> punctured-domain relative bound;

centered source increment OR weighted-dual additive route
    -> equilibrium-containing analysis.
```

For the current P5 Lyapunov direction, the third route is the natural one.
A velocity floor would excise the equilibrium and therefore cannot support the
intended local strict-decay statement.

## Open boundary

Still not proved here:

- any deployed/source theorem `cap<=K|v_i|` or `cap^2<=K^2 A(v)`;
- any centered increment/Lipschitz property of the actual Float64 FD error;
- true-DH/source binding of the current numeric envelope;
- same-domain P8 coverage;
- P5/M4 admission.

Status remains `pending`.  Formalization should preserve these boundaries and
final validation/integration remains with 封不觉 / 梁智炜 respectively.
