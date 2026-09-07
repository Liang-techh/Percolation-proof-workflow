---
kind: review_result
review_id: review-T-P5-009-liuguanyi-20260907T0005
task_id: T-P5-009
source_agent: 柳冠一
claimed_at: 2026-09-06T23:58:00-06:00
created_at: 2026-09-07T00:05:00-06:00
inspected_commit: cc5453e57763284991645c0a19832ad6c50d3b98
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_affine_envelope_boundary_and_replace_relative_interface
---

# T-P5-009 — exact interface boundary for affine FD envelopes and velocity-relative decay

## Scope

The current FD fallback interface is componentwise

```text
|e_i| <= slope_i * cap + offset_i.
```

`T-P5-005` already observed that the positive offsets in channels 1--4 prevent
one from simply reading this as `|e_i| <= rho_i |v_i|`. This review sharpens
that observation into an exact interface theorem: **what extra state contract is
sufficient, what is logically necessary if one insists on using only the affine
envelope, and what replacement interface is appropriate near the equilibrium.**

Inspected objects:

- `examples/routeb_dh_power_binding/FDForceBudget.lean`
  - blob `4e3a3ae56b5ec2708d0deeec2de786d0a0218e36`;
  - `envelope cap i = slope i * cap + offset i`.
- `agent_review_inbox/review-T-P5-005-kuangmanmozun-20260906T2307.md`
  - blob `65a1e212244e615568a07169889591ed2cb68c4f`;
  - supplies the desired componentwise/weighted relative-decay target and the
    positive-offset counterexample.
- `agent_review_inbox/review-T-P5-008-honglianmozun-20260906T2348.md`
  - current version reviewed at this pass;
  - shows that the deployed structure should ultimately remove the mass
    regularizer and gravity FD term into storage and treat the C mismatch at
    the power level, so the affine FD envelope is best viewed as a fallback
    enclosure rather than the preferred strict-decay interface.

No true-DH source binding, provenance, receipt, compilation, or admission claim
is made here.

## 1. Sharp scalar theorem: when an affine envelope alone can imply a relative bound

Fix nonnegative scalars

```text
s >= 0, b >= 0, C >= 0, rho >= 0.
```

Consider the abstract implication

```text
0 <= cap,
cap <= C * |v|,
|e| <= s * cap + b
--------------------------
|e| <= rho * |v|.                                  (A)
```

If (A) is required to hold for **every** real `v,e` and every admissible `cap`,
then the following condition is necessary and sufficient:

```text
b = 0  and  s*C <= rho.                             (B)
```

### Sufficiency

If `b=0`, then

```text
|e| <= s*cap
     <= s*C*|v|
     <= rho*|v|.
```

### Necessity of `b=0`

Set

```text
v = 0,
cap = 0,
e = b.
```

The envelope premise is satisfied because `|e|=b`. The conclusion forces

```text
b <= rho*0 = 0.
```

Together with `b>=0`, this gives `b=0`.

### Necessity of `s*C <= rho`

After `b=0`, choose

```text
v = 1,
cap = C,
e = s*C.
```

All premises are saturated, so the desired conclusion gives

```text
s*C <= rho.
```

Thus (B) is an exact iff boundary, not merely a convenient sufficient
condition.

### Important logical boundary

This theorem is about what follows from the **envelope interface alone**. A
positive `offset` does **not** prove that the physical error is nonzero at the
equilibrium. It proves that the current coarse enclosure permits such an error,
so no downstream theorem may infer a velocity-relative estimate without an
additional centered/source-specific premise.

## 2. Application to the repository's six FD envelopes

The exact offsets are

```text
i=0: 0
i=1: 68343 / 800000000000000
i=2: 21909 / 1000000000000000
i=3: 6867  / 8000000000000000
i=4: 6867  / 4000000000000000
i=5: 0.
```

Therefore:

- channels `1,2,3,4`: **no finite `C` and `rho` can make the current affine
  envelope alone imply a global `|e_i| <= rho_i |v_i|` theorem**;
- channels `0,5`: the offset obstruction is absent, but one still needs the
  nontrivial state contract

```text
cap <= C_i * |v_i|.                                (C)
```

Without (C), even a zero-offset envelope cannot imply velocity-relative
scaling: take `v_i=0`, `cap>0`, and any allowed nonzero error.

If (C) is supplied, the sharp coefficient delivered by the envelope is

```text
rho_i = slope_i * C_i.
```

For strict componentwise damping retention `rho_i < d_i`, channels 0 and 5
would require respectively

```text
C_0 < (13/10) / slope_0
    = 195540800000000 / 257371
    ~= 7.5976236639e8,

C_5 < (1/2) / slope_5
    = 2417400000.
```

These are only algebraic interface thresholds; the repository currently does
not prove the componentwise cap contracts (C). In fact a common cap that also
measures configuration or other coordinates can remain positive when one
velocity component is zero, so (C) is generally much stronger than the
available domain information.

## 3. The exact away-from-equilibrium repair

A positive offset can be converted to a relative coefficient only on a region
bounded away from zero velocity.

Assume

```text
m > 0,
m <= |v|,
cap <= C*|v|,
|e| <= s*cap+b,
s,b,C >= 0.
```

Then the division-free sharp estimate is

```text
m*|e| <= (m*s*C + b)*|v|.                           (D)
```

Indeed,

```text
m*|e|
 <= m*s*cap + m*b
 <= m*s*C*|v| + b*|v|
 = (m*s*C+b)*|v|.
```

Since `m>0`, this is equivalent to

```text
|e| <= (s*C + b/m) * |v|.                           (E)
```

The coefficient is sharp under the supplied information: equality is attained
when `|v|=m`, `cap=C|v|`, and the error saturates the affine envelope.

This repair is useful for an annulus/first-exit argument, but it **cannot**
serve as a Lyapunov strict-decay theorem through the equilibrium because the
assumption `m<=|v|` explicitly removes `v=0` and a whole neighborhood of it.

## 4. Minimal equilibrium-compatible repair: replace the constant offset by a centered remainder

To obtain a theorem valid at `v=0`, the extra contract must force every
remaining error allowance to vanish there. A minimal abstract interface is

```text
|e| <= s*cap + zeta,
cap <= C*|v|,
zeta <= beta*|v|,
s,C,beta,zeta >= 0.
```

Then

```text
|e| <= (s*C + beta) * |v|.                          (F)
```

Equivalently, one may expose an actual decomposition

```text
e = e_cap + e_centered,
|e_cap|      <= s*cap,
|e_centered| <= beta*|v|,
cap          <= C*|v|,
```

and obtain the same result by the triangle inequality.

This is the mathematically correct role for an equilibrium/source theorem: it
must replace the numerical constant `offset_i` by a state-dependent centered
remainder, or prove that the corresponding physical term is removed elsewhere
(e.g. by storage renormalization).

A particularly reusable source-to-math contract is the centered Lipschitz form

```text
e(x_eq) = 0,
|e(x)-e(x_eq)| <= L * R(x),
```

which immediately yields

```text
|e(x)| <= L * R(x).                                (G)
```

If one insists on the componentwise target, one additionally needs
`R(x) <= K_i |v_i|`. That last step is usually the restrictive one.

## 5. Why a full-state or power-level interface is preferable

The current `cap` is not itself a velocity component. Therefore trying to prove
six separate contracts `cap <= C_i|v_i|` is structurally brittle: one component
`v_i` can vanish while other state coordinates remain nonzero.

The same algebra works with any nonnegative state size `R(x)`:

```text
cap <= C*R(x),
zeta <= beta*R(x)
--------------------------
|e| <= (s*C+beta) R(x).                             (H)
```

For the P5 energy lane, the most natural choices are a weighted velocity norm,
an energy/sublevel radius, or a direct power theorem.

This matches the new `T-P5-008` structure:

- the `10^-6 I` mass term should be absorbed into kinetic storage rather than
  forced through an affine residual envelope;
- the frozen-potential gravity FD discrepancy is a candidate conservative
  storage correction after its source binding;
- the C-FD mismatch power is cubic in velocity and should be bounded directly
  by a damping power inequality such as

```text
|<e_C,v>| <= kappa_C * A(v),
```

not by six componentwise affine force envelopes.

Thus `FDForceBudget.envelope` remains a valid fallback for ultimate-bound / gross
error accounting, but it is not the right interface for proving local strict
decay.

## 6. Lean-friendly theorem decomposition

The highest-value source-independent formalization is the sharp iff.

```lean
def AffineEnvelopeImpliesRelative
    (s b C rho : ℝ) : Prop :=
  ∀ (v cap e : ℝ),
    0 ≤ cap ->
    cap ≤ C * |v| ->
    |e| ≤ s * cap + b ->
    |e| ≤ rho * |v|

theorem affine_envelope_relative_iff
    (s b C rho : ℝ)
    (hs : 0 ≤ s) (hb : 0 ≤ b) (hC : 0 ≤ C) (hrho : 0 ≤ rho) :
    AffineEnvelopeImpliesRelative s b C rho
      <-> (b = 0 ∧ s*C ≤ rho)
```

The away-from-zero theorem should be kept division-free:

```lean
theorem affine_envelope_relative_away_from_zero
    (s b C m v cap e : ℝ)
    (hs : 0 ≤ s) (hb : 0 ≤ b) (hC : 0 ≤ C)
    (hm : 0 < m) (hvm : m ≤ |v|)
    (hcap : cap ≤ C*|v|) (he : |e| ≤ s*cap+b) :
    m*|e| ≤ (m*s*C+b)*|v|
```

And the equilibrium-compatible adapter is:

```lean
theorem centered_envelope_to_relative
    (s C beta v cap e zeta : ℝ)
    (hs : 0 ≤ s) (hC : 0 ≤ C) (hbeta : 0 ≤ beta)
    (hcap : cap ≤ C*|v|)
    (hzeta : zeta ≤ beta*|v|)
    (he : |e| ≤ s*cap+zeta) :
    |e| ≤ (s*C+beta)*|v|
```

A vector/full-state version should generalize `|v|` to a supplied nonnegative
radius rather than baking in `Fin 6` prematurely.

## 7. What this closes / what remains open

Mathematically closed here:

1. exact necessary-and-sufficient conditions for deriving a global relative
   bound from the affine envelope plus `cap <= C|v|`;
2. exact proof that positive offsets in channels 1--4 are an unavoidable
   logical obstruction **at the current interface level**;
3. exact sharp repair on regions `|v|>=m>0`;
4. the minimal equilibrium-compatible centered adapter needed to replace the
   constant offset.

Still open:

- a source theorem giving an equilibrium-centered FD error rather than the
  coarse global envelope;
- a realistic relation between the repository's `cap` and a weighted state or
  velocity norm on the same covered domain;
- the source bindings needed by `T-P5-008` to remove storage terms and quantify
  the C-FD cubic power;
- controller/runtime solve residual bounds;
- P5/M4 domain coverage and final admission.

## Recommended next action

Do **not** try to prove `offset_i <= beta_i |v_i|` for the positive constant
offsets. That is impossible on any domain containing `v_i=0`.

Instead, the physical/source lane should expose a centered error theorem for the
actual terms (or remove them into storage as in `T-P5-008`), and the formalization
lane can encode the three small interface lemmas above. If the only available
information remains the old affine envelope, use it for ultimate-bound/error
budgeting, not for strict relative decay.

No checker or Lean command was run in this mathematical pass; compilation and
independent validation remain separate lanes.
