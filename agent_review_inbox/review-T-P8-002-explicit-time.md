---
kind: review_result
task_id: T-P8-002
source_agent: Codex
created_at: 2026-09-06T22:00:00-06:00
integration_status: pending
---

# T-P8-002 — explicit-time 13-state parent option

## Scope and decision boundary

This is a read-only comparison of the existing 14-state ramp parent and the
smallest semantically faithful explicit-time 13-state alternative.  No source,
persistent Route-B state, registry, receipt, or admission flag was modified.
No long simulation was run.

The recommendation must preserve the original Route-B quantifiers: the full
12-dimensional initial mechanical set, every ramp coefficient `c` satisfying
`c^2 ≤ 3`, horizon `[0,1]`, and the same terminal physical outputs.  A parent
that removes `c` from the quantifier or silently changes `w` is not equivalent.

## Inspected evidence

| artifact | SHA-256 | relevant evidence |
|---|---|---|
| `docs/routeb-p8-next-concrete-child.md` | `9EF74058FB6711946A253A9DED55EB6CE91DDA01059A78999B413FF98E57AB0E` | existing contract decision and `c=1` incompatibility witness |
| `docs/routeb-p8-flowpipe-binding-next.md` | `47681DFC4DE2153B34AD8B2269FF747583D09E3FADDACA50FDA27D94BC43A6AB` | source lines, coordinate map, flowpipe obligations |
| `examples/routeb_p8_picard_step_lean/RouteBP8PicardStep.lean` | `99D309B1D07439DFB7DE1088D6A2E34F7DCA664EFE72857F94ECE5F28A635741` | `State14`, `FullX0`, `InitialBox`, `RampRhsPremise`, Picard decomposition |
| `examples/routeb_p8_contract_adapter/P8ContractAdapter.lean` | `DC4BF1C7C0B1EE428EE3BF146E90801E08A2199FB931789699FE8073A82AB7F9` | exact negative `zeroTailLift_not_ramp`; conditional `timeLift_rampPremise` |
| external `robot_final/cross_validation/routeB_reachability_full_dh_probe.jl` | recorded in prior P8 audit | `u[1:6]`, `u[7:12]`, `u[13]`; `du[13]=z0`; `dim:13` |
| external `robot_final/routeB_export_traj.jl` | recorded in prior P8 audit | discrete `dt=0.005`; computes `wv=cw*tk`, does not expose a 14-state ODE |

The current 13-state probe therefore represents a constant-`w` state, not the
nonzero ramp family.  The exporter’s formula `w(t)=c*t` is evidence for a
time-dependent input convention only; it is not an ODE source binding.

## Existing 14-state parent

The current parent uses

```text
State14 = Fin 14 → ℝ = (q₁,…,q₆,dq₁,…,dq₆,w,c)
FullX0(z) := mechanicalEnergy(z) ≤ 9/400 ∧ w=0 ∧ c²≤3
RampRhsPremise(F) := ∀ z, F(z)[w] = z[c] ∧ F(z)[c] = 0
```

Its terminal/flowpipe interfaces are consequently predicates over a 14-state
trajectory.  This is the cleanest statement for the original ramp-input
problem if a genuine deployed 14-state RHS can be supplied and source-bound.

The natural zero-tail lift of the deployed 13-state source is impossible:
at the legal initial state `q=dq=w=0,c=1`, `FullX0` holds but the lift gives
`w'=0`, while `RampRhsPremise` requires `w'=1`.  This is a closed negative
contract fact, not an interval or numerical failure.

## Minimal explicit-time 13-state signature

Use a 13-state mechanical-plus-input state

```text
State13 := Fin 13 → ℝ = (q₁,…,q₆,dq₁,…,dq₆,w)
TimeRhs13 := ℝ → State13 → State13
```

The smallest parent contract that retains the original ramp family is:

```text
ExplicitInitial13(x,c) :=
  mechanicalEnergy13(x) ≤ 9/400 ∧ x[w] = 0 ∧ c² ≤ 3

ExplicitSolution13(F,x₀,c,y) :=
  y(0)=x₀ ∧
  (∀ t∈[0,1], y'(t)=F(t,y(t))) ∧
  (∀ t∈[0,1], y(t)[w] = c*t)

ExplicitRhsBinding(F13, source) :=
  ∀ t x, F13(t,x) = source_rhs13(x,t,c)
```

For an implementation that keeps `c` outside the state but makes it explicit
in the vector field, the least ambiguous signature is instead:

```text
F13 : ℝ → ℝ → State13 → State13
-- arguments are (t,c,x), with F13 t c x[w] = c
```

Then the core theorem should be parameterized by the same `c`:

```text
theorem explicit_time_flowpipe
  (F13 : ℝ → ℝ → State13 → State13)
  (x₀ : State13) (c : ℝ)
  (hinit : mechanicalEnergy13 x₀ ≤ 9/400 ∧ x₀[w] = 0 ∧ c^2 ≤ 3)
  (hbinding : ∀ t x, F13 t c x = ...)
  (hregular : ...)
  (hbox : ... outward enclosure on every time cell) :
  ∃ y, solution13 F13 c x₀ y ∧
    ∀ t ∈ Set.Icc 0 1, y t ∈ certifiedTube13 t
```

The omitted regularity/enclosure premises are deliberate: they must be
instantiated by actual source semantics and outward intervals, not inferred
from an endpoint payload.  The theorem must not quantify over only `c=0`.

## Initial-domain impact

The mechanical initial ball is unchanged: keep the same `9/400` energy bound
on `(q,dq)` and `w(0)=0`.  The scalar condition `c²≤3` must remain a parameter
condition in the parent, even though `c` is not a state coordinate.  Therefore
the 13-state initial domain is a dependent family `X₀(c)`, not the projection
of the old `FullX0` with `c` discarded.

The old `fullX0_subset_initialBox` can be reused only after a new projection
lemma is proved, for example:

```text
FullX0(z) → ExplicitInitial13(forgetTail z, z[c])
```

and conversely, for semantic equivalence of quantified families:

```text
ExplicitInitial13(x,c) → FullX0(rampLift x c 0).
```

The converse is important: without it, a 13-state parent could accidentally
weaken or enlarge the original initial set.

## Terminal-transfer impact

If the terminal statement mentions only `(q₄,q₅,dq₄,dq₅)` and the mechanical
energy/residual outputs, transfer is structurally a projection and can reuse
the existing terminal comparator after proving the trajectory relation
`w(t)=c*t`.

If the terminal statement contains `w`, use the explicit relation theorem
`y(t)[w]=c*t` to rewrite it.  If it contains `c`, `c` must remain an external
parameter in the terminal predicate:

```text
Terminal13(y,c) := Terminal14 (fun t => appendRamp (y t) c t)
```

The transfer theorem must prove both directions needed by the original
quantifier, not merely equality at `t=1`:

```text
terminal14 (appendRamp (y 1) c 1)
  ↔ terminal13 (y 1) c
```

An endpoint equality alone does not establish the flowpipe/domain condition;
the tube must still cover every `t ∈ [0,1]`, and domain continuation must be
proved in the selected 13-state semantics.

## Comparison and recommendation

| option | semantic status | proof cost | recommendation |
|---|---|---:|---|
| Keep 14-state ramp parent and bind a genuine 14-state source | exactly matches the existing theorem and original ramp semantics | lower downstream cost, higher immediate source-contract cost | preferred if source can be repaired without changing deployed dynamics |
| Add explicit-time 13-state parent with `c` as external parameter | equivalent only with `X₀(c)`, `w=c*t`, source binding, and terminal equivalence lemmas | moderate; requires a parallel 13-state flowpipe chain | recommended fallback for the currently deployed 13-state code |
| Natural zero-tail 13→14 lift | contradicts legal `c≠0` initial states | invalid | reject |
| Treat exporter `w=c*t` as 13-state ODE proof | discrete empirical convention only | invalid | reject |

Recommendation: do not silently replace the existing parent. Add the explicit
time parent as a named alternative contract, then bind the current source to
it only if the source is made parameter-aware (`c` must affect the RHS, at
least through `w(t)=c*t`). Preserve the existing 14-state parent as the
preferred target for the original theorem, because it keeps `c` in the state
and makes ramp invariants and terminal transfer direct. If the deployed source
cannot be changed, the explicit-time parent is the only semantically coherent
fallback, but it remains a new theorem family and cannot inherit the current
14-state flowpipe result by definitional equality.

## Smallest next child theorem chain

```text
P8_EXPLICIT_INITIAL_EQUIVALENCE
  → P8_EXPLICIT_RAMP_RELATION (w(t)=c*t)
  → P8_EXPLICIT_SOURCE_BINDING
  → P8_EXPLICIT_RHS_INTERVAL_CONTAINMENT
  → P8_EXPLICIT_LOCAL_FLOWPIPE
  → P8_EXPLICIT_CONTINUATION_TO_T1
  → P8_EXPLICIT_TERMINAL_TRANSFER
```

The first executable child is `P8_EXPLICIT_INITIAL_EQUIVALENCE`; it is pure
exact-real adapter logic and does not require simulation. It must be followed
by a source-semantic binding child. The existing `timeLift_rampPremise` is
reusable only as a conditional interface theorem; it does not discharge either
binding child.

## Unresolved items and admission boundary

- The current Julia probe has no `c` input and writes `du[13]=z0`; exact
  source-to-`F13(t,c,x)` binding is therefore open.
- The current exporter uses a discrete `dt=0.005` trajectory and is not a
  continuous-time proof.
- No outward interval enclosure, solution existence, continuation, full
  `[0,1]` coverage, or terminal transfer has been established for either
  contract.
- The 14-state parent’s conditional Lean scaffold and the explicit-time
  signature are not registry entries.
- `formal_certificate_allowed` must remain `false`; registry remains unchanged.

Integration status is `pending` and this memo is evidence for scheduling only.
