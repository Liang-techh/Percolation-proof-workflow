# T-P5-063 — Undercancelled aggregate contact-order Lean sidecar

Agent/source_agent: **巨阳仙尊** (Lean formalization), consuming the mathematics in `agent_review_inbox/review-T-P5-063-undercancelled-aggregate-kuangmanmozun-20260908T0252.md` from **狂蛮魔尊**.

This sidecar formalizes the source-independent algebraic/contact-order layer behind the rule “aggregate first, then decide whether the contact is safe.”  It deliberately does **not** prove any deployed P5/P8 source binding or final closure.

## Trusted statements

`P5UndercancelledAggregate.lean` provides:

- `net_order_nonnegative_iff` / `net_order_negative_iff`: integer net order is reduced to the natural exponent comparison.
- `aggregate_integer_excess_identity`: for `B ≤ A` and `x ≠ 0`, `x^A/x^B = x^(A-B)`.
- `aggregate_contact_safe_of_net_nonnegative`: a nonnegative aggregate net order admits the explicit continuous extension `x ↦ x^(A-B)`.
- `zero_net_order_finite_scale` and `positive_net_order_zero_extension`: exact finite/vanishing boundary cases.
- `negative_net_order_reciprocal_form` and `negative_net_order_unbounded`: a negative net order leaves a positive reciprocal power and is unbounded along positive points approaching contact.
- `undercancelled_product_exact_rescue`, `zero_net_order_exact_example`, `negative_net_order_exact_example`: exact regressions distinguishing positive/zero/negative aggregate excess.
- `monomial_pullback_exponent_transport`: `(lambda*y^p)^M = lambda^M*y^(p*M)` for the monomial pullback layer.
- `additive_cancellation_bounded_iff`: for the exact principal model `a/x+b/x`, boundedness is equivalent to `a+b=0`.
- `exact_vanishing_atom_rescue`: exact algebraic rescue corresponding to `mu=kappa^2`, hence `mu^2/kappa=kappa^3` away from the contact.

The additive theorem uses **global boundedness of the exact principal pair**.  For a pure `1/x` principal model this is equivalent to boundedness in any punctured neighbourhood of zero; it is not a claim about arbitrary lower-order remainders.

## Interface boundary

This sidecar does not formalize:

- the finite-order asymptotic expansion `p_i=a_i xi^{m_i}+O(xi^{m_i+1})` or exact leading-coefficient product/quotient;
- algebraic dependence or GCD cancellation between non-monomial factors;
- additive cancellation beyond the exact two-term principal model;
- actual deployed `Rtr/Rdet` / P5 coefficient or P8 trajectory/source binding;
- Float64, finite-difference, controller, solve semantics, or same-domain ODE coverage;
- P5/P8/M4 final closure, registry admission, provenance, receipts, or independent verification.

Thus a compile-clean result is only a `compiled_candidate`.  It must remain **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**.

## Portable verification

The sidecar is pinned to the repository’s Lean 4.32 local-FKG environment and is intended to be run by `.github/workflows/lean-agent-sidecars.yml`:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_undercancelled_aggregate_lean/verify.sh
```

`verify.sh` resolves `lake`/`lean` from `PATH`, checks the pinned local `lake-manifest.json`, compiles with `-DwarningAsError=true`, scans for `sorry`/`admit`, and audits all public theorem `#print axioms` reports for `sorryAx`.
