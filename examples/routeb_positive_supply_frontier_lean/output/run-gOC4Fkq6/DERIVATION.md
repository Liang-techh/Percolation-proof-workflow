# Frontier derivation and closure boundary

## Exact theorem package

`Frontier.lean` proves five low-dependency facts:

- `terminalDen_pos_of_eta_zero`: if `A,D,rho>0`, `tau>=0`, and the projected
  defect is zero, the denominator is positive for `rho>0`.
- `terminalDen_pos_of_relative_eta`: if `0<=tau<=1` and
  `|eta|<=kappa*rho`, positivity follows from `kappa<A+D`.
- `b45_terminalDen_pos_of_relative_eta`: the concrete B45 constants give the
  exact threshold `36802229/24000000`.
- `equilibrium_floor_le_beta0`: a direct gate at `rho=0` with zero storage
  rate forces the equilibrium cost floor to be no larger than `beta0`.
- `equilibrium_floor_budget`: that floor can be charged to the finite beta0
  budget by exact linear arithmetic.

The relative theorem is the only division-compatible branch. The equilibrium
theorem is deliberately division-free, so it remains valid when an absolute
eta neighborhood makes the denominator nonpositive for sufficiently small
rho.

## Precise parent obligations

The sidecar closes no physical leaf by itself. To use branch A, the source
semantics must prove `etaU=0` at the equilibrium and must provide a direct
gate with `CR_eq <= beta0`. To use branch B, the source semantics must prove a
state-relative estimate for the projected defect; the existing Q projection
only supplies an absolute bound.

The minimum complete physical decomposition is therefore:

```text
EqZero := [etaU(0)=0, CR_eq=0]
          -> direct equilibrium gate with beta0 >= 0

EqFloor := [CR_eq <= beta_eq, beta_eq <= beta0]
           -> direct equilibrium gate and V0_cap + beta_eq + tail < 1

Rel := [rho>0, |etaU| <= kappa*rho, kappa < A+D]
       -> denominator-positive first-order gate

SmallRho := direct gate on 0 < rho <= rho_star
            -> no division near the absolute-eta singular regime
```

`SmallRho` still requires an exact source-cost enclosure. If neither `EqZero`
nor an affordable `EqFloor` is available, and only a nonzero absolute eta
bound is assumed, the current denominator route is impossible near `rho=0`.

## Minimal model choices

The least invasive repair is to add `etaU(0)=0` and a proved local estimate
`|etaU| <= kappa*rho` to the source contract. If that is false for the actual
implementation, retain absolute eta and add an explicit equilibrium supply
floor `beta_eq`; then use the direct gate for a small-rho cell and the relative
gate only outside it. Replacing the nominal PMI model is not required by this
algebraic obstruction; it is a separate B45-5 source-mismatch decision.
