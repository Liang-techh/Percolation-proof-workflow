---
kind: review_result
review_id: review-T-P5-064-ANALYTIC-UNIT-PULLBACK-ADMISSION-liuchuanafeng-20261010T0218Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-10T02:18:00Z
inspected_commit: 83b41ebd7d597af4abe6d088925d95c892ba8942
parent_tree: 53a7156fa52b07ae6cf6a963e0d9cc34ed80808d
claim_id: claim-T-P5-064-ANALYTIC-UNIT-PULLBACK-ADMISSION-liuchuanafeng-20261010T0215Z
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/claim-T-P5-064-ANALYTIC-UNIT-PULLBACK-ADMISSION-liuchuanafeng-20261010T0215Z.md
  - agent_review_inbox/claim-T-P5-064-analytic-unit-pullback-liuguanyi-20260908T0305.md
  - agent_review_inbox/review-T-P5-064-analytic-unit-pullback-liuguanyi-20260908T0321.md
  - agent_review_inbox/review-T-P5-063-UNDERCANCELLED-AGGREGATE-ADMISSION-liuchuanafeng-20261010T0116Z.md
task_id: T-P5-064
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
proposed_integration_target: documentation
requested_action: harvest_pending_admission_audit_do_not_promote_analytic_unit_pullback_bridge
---

# T-P5-064 admission audit: analytic-unit pullback bridge stays pending

## Question

At the inspected tree `83b41ebd7d597af4abe6d088925d95c892ba8942` (parent `53a7156fa52b07ae6cf6a963e0d9cc34ed80808d`), does the published T-P5-064 analytic-unit pullback note already supply a deployed source factorization into explicit nonvanishing units `u_a` and exponent matrix `W`, certified rational margins `m_a/M_a/L_a`, reduced-packet bounds `M_R/L_R`, a proof of factor independence, a reachable rate cone, an actual P5 residual margin, Float64/libm semantics, same-key cell coverage, ODE continuation, a fresh pinned Lean receipt, or registry admission?

May the unit-transport identity `E' = W^T E`, `beta' = W^T beta mod 2`, the structural gate survival under positive lower bound `b_U > 0`, the exact rational unit budgets, or the hidden-zero obstruction be promoted?

## Decision

**No admission upgrade. Keep `admission_label: pending`.**

柳冠一 states a source-independent child that extends the pure-monomial transport of T-P5-063 to the normal-crossing form `h_a(z) = u_a(z) * prod_j z_j^(W_aj)` under an explicit nonvanishing-unit contract `0 < m_a <= sigma_a u_a(z) <= M_a` and Lipschitz bound. The variable unit becomes a multiplicative reduced factor `U_E` that does not alter the pulled-back valuation or parity. Structural boundedness and contact regularity gates survive provided `b_U > 0`. Exact rational amplitude and Lipschitz budgets are derived for integer powers. A sharp obstruction shows that pointwise nonzero on the punctured set is insufficient (hidden zeros must be promoted). Approximate factorization with remainders is excluded.

This is not `rejected`: the published identities match an independent replay of the transport, the example, and the obstruction. It is not `architecture_only`: the review states exact ordered-field surfaces under named hypotheses. It is not `compiled_candidate`: no Lean sidecar or pinned receipt is attached to this leaf. A source-independent algebraic/valuation bridge is not source binding and is not registry admission.

Prior authorship is preserved. This file does not overwrite 柳冠一. The same-agent claim at `2026-10-10T02:15:00Z` is consumed; no second claim is added.

Roster text still lists 流川枫 as unavailable for new dispatch. This audit does not rewrite that roster or prior authorship. Harvest may still mark the file `rejected_retired_agent`; that marker must not be read as a mathematical rejection of the bridge.

## Evidence

1. **Queue does not close the parent.** `task_queue.md` has no T-P5-064 closure. The 2026-09-14 release still says a source-independent lemma cannot enter the verified registry. The neighbouring T-P5-063 admission audit already left the aggregate lane pending.
2. **Math review is conditional.** `review-T-P5-064-analytic-unit-pullback-liuguanyi-20260908T0321.md` states the packet (1.1)-(1.4), Theorems 2.1-3.2 on transport and gate survival, Lemmas/Theorems 4-6 on rational budgets, the worked example (7), the hidden-zero obstruction (8), sign and exactness boundaries (9-10), and Lean-friendly leaves (12). Its `admission_label` is `pending`. The claim excludes source binding, Float64, coverage, and admission.
3. **No fresh Lean receipt.** Section 12 proposes statements only. This pass did not execute Lean, did not create a sidecar, and did not re-run a workflow checker.
4. **Local replay of the published example and obstruction only.**

```text
example: h1=(2+z)z, h2=(3-z)z^2 on |z|<=1/2
E=(-1,1), W=(1,2) → E'=1, beta'=1
U=(3-z)/(2+z), 1<=U<=7/3, Lip(U)<=20/9
full Lip <=31/9 with R=1.
hidden-zero: u(z)=z, W=0, E=-1 → Psi=1/|z| unbounded.
```

These checks do not instantiate a source remainder. `u_a`, `W`, `m_a`, `M_a`, `L_a`, `H_j`, `M_R`, `L_R` remain hypotheses. Absolute-value and sign figures are regressions, not deployed residuals.

## Receipt

```text
command: local numeric replay only; repo checker not run
exit_code: 0 for the local replay; not a workflow checker
axiom_print: not executed this pass
placeholder_scan: not a kernel scan this pass
math_review_blob: b9d659a557e5bf7ff00427e0b85ce08254a37c34
math_claim_blob: 10663f3eb27a796cbc4628457e2b9ad5b2dd22eb
fresh_lean_receipt: not exhibited
unit_transport_identity: E'=W^T E preserved
hidden_zero_unbounded: true for E=-1, W=0
rational_unit_budgets: exact for integer powers
deployed_factorization: not exhibited
unit_margin_packet: not exhibited
reduced_monomial_bounds: not exhibited
factor_independence: not exhibited
reachable_rate_cone: not exhibited
actual_P5_residual_margin: not exhibited
float64_libm_outward_rounding: not exhibited
same_key_cell: not exhibited
ode_continuation: not exhibited
```

## Obstruction

```text
identity_surface: a supplied exact factorization plus certified nonvanishing unit margins classifies whole-cell boundedness/continuity after transport; the bridge is not a source theorem
coefficient_surface: u_a, W, m_a, M_a, L_a, H_j, M_R, L_R are hypotheses; absolute-value and sign figures are regressions, not source witnesses
lower_margin_gap: pointwise nonzero is insufficient; a positive rational lower bound is required for necessity of the gate
hidden_zero_gap: zeros or sign changes inside a purported unit must be promoted into the explicit exponent packet
approximate_factor_gap: additive remainders can alter zeros and therefore valuation/parity; numerical closeness is not a certificate
formal_gap: no pinned Lean receipt exists for the unit-monomial identity, the integer-power bounds, the product envelope, the gate survival, or the hidden-zero counterexample
binding_gap: no same-key CSE identity producing the unit factorization or the margins is bound
execution_gap: a removable mathematical extension does not prove the deployed evaluator avoids IEEE 0/0 on the zero surfaces
coverage_gap: a finite abstract cell does not place an absolute cell in a source domain
calculus_gap: valuation identities are not a checker certificate; FTOC, first-exit, and ODE continuation are not proved
obstruction_scope: missing source factorizations with explicit units and W, certified rational margins, reduced bounds, independence, residual margins, Float64 semantics, box trajectory, flowpipe, gate binding, and a fresh pinned receipt remain failure boundaries
missing_for_parent_close:
  one same-key exact factorization exhibiting the unit form for the relevant factors
  certified rational m_a/M_a/L_a and box radii H_j
  certified reduced-packet bounds M_R/L_R
  either the structural gate after transport, or a separate exact cancellation theorem
  a uniform residual margin if the Lipschitz constant is used in a first-exit argument
  an execution adapter showing the cancelled formula, or an exclusion of the zero surfaces
  a first-exit / ODE existence-continuation theorem on the actual pair
  an independent pinned Lean receipt after source binding
forbidden_this_pass:
  registry edit
  state edit
  formal proof edit
  recompile
  sidecar creation
  promotion of the analytic-unit pullback theorem, the budget identities, or the neighbouring aggregate lane
```

## Admission

`admission_label: pending`. Integration status remains pending. `formal_certificate_allowed: false`. `registry_promoted: false`.
