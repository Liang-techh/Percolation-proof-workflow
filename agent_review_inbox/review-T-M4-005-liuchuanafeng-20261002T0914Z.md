---
kind: review_result
review_id: review-T-M4-005-liuchuanafeng-20261002T0914Z
source_agent: 流川枫
created_at: 2026-10-02T09:14:00Z
inspected_commit: c3bd185adef26b9eb4358848d6a39b87e568fa64
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/review-T-M4-003-kuangmanmozun-20260906T2258.md
  - agent_review_inbox/review-T-M4-004-liuchuanafeng-20261002T0814Z.md
  - examples/routeb_terminal_qpoly_comparator_lean/F4DirectQpolyComparator.lean
  - examples/routeb_terminal_qpoly_comparator_lean/README.md
  - examples/routeb_terminal_qpoly_comparator_lean/lean-toolchain
  - examples/routeb_terminal_qpoly_comparator_lean/verify.sh
  - examples/routeb_m4_cross_branch_budget_lean/CrossBranchBudget.lean
task_id: T-M4-005
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# T-M4-005 admission probe: eta=81/160 terminal arithmetic corollary

## Question

Does commit `c3bd185adef26b9eb4358848d6a39b87e568fa64` already contain a pinned Lean sidecar of the exact rational specialization `eta=81/160`, `D<=1401/625`, with current `L,g` kept as typed hypotheses, an exact positive terminal margin, and no hidden Float64 step?

## Decision

**No. Keep `admission_label: pending`.** The required corollary sidecar is absent. Offline exact rational arithmetic agrees with the parent review's claimed margins, but that check is not a Lean receipt, not a compile, and not an admission event.

This is not `rejected`: the scalar implication was not disproved. It is not `compiled_candidate`: no `eta81` file was compiled and `verify.sh` was not run. It is not `verified` and not architecture-only: the statement is a concrete arithmetic child of `T-M4-003`, but the theorem artifact does not exist.

## Evidence inspected (read-only)

1. **Queue contract is still open and previously unclaimed.**
   `task_queue.md` lists `T-M4-005` with status `open`, historical owner `臭屁猪`, sources `review-T-M4-003-kuangmanmozun-20260906T2258.md` and `examples/routeb_terminal_qpoly_comparator_lean/`. Tree lookup at this commit found no prior `claim-T-M4-005*` or `review-T-M4-005*`. Sibling `T-M4-004` already records that the generic weighted split is also absent; this leaf does not reopen that task.

2. **Existing comparator is the `eta=1/2` leaf, not the corollary.**
   `F4DirectQpolyComparator.lean` (blob `2d89190182dd7a4a795f8c8e1e930f9f46686bf2`) defines `qpoly`, exact `L`, exact `g`, and `D_gate = 4483/2000`, and proves `terminal_qpoly_lt_twelve` only under `Q <= (3/2)*L + 3*g*D` and `D <= D_gate`. There is no `eta`, no `81/160`, and no `1401/625`. No `sorry` or `admit` appears. `#print axioms` is a source directive, not a captured axiom list from this pass. `lean-toolchain` is `leanprover/lean4:v4.29.0-rc1`. `verify.sh` was not executed.

3. **Cross-branch budget directory is a different child.**
   `examples/routeb_m4_cross_branch_budget_lean/CrossBranchBudget.lean` (blob `3d45fe486c0b0181b2abd7d9b084641215e59114`) belongs to the `T-M4-007` arithmetic interface. It is not consumed here and is not treated as the eta81 terminal corollary.

4. **Parent margins rechecked offline with exact rationals, not Lean.**
   Using the in-file `L` and `g`, `eta=81/160`, and no Float64 step:

   ```text
   D_gate = 4483/2000
   1401/625 - D_gate = 1/10000
   12 - [(1+eta)*L + (1+1/eta)*g*D_gate]
     = 562809780911078327482773299144592251
       / 1612800000000000000000000000000000000000
     > 0
   12 - [(1+eta)*L + (1+1/eta)*g*(1401/625)]
     = 11386738131946758247425634286621983
       / 67200000000000000000000000000000000000
     > 0
   ```

   Both fractions match `review-T-M4-003-kuangmanmozun-20260906T2258.md`. This confirms the arithmetic claim in that review. It does not discharge the weighted-split hypothesis `Q(x+r) <= (1+eta)*Q(x) + (1+1/eta)*Q(r)`, and it does not create physical `L` or `g`.

## Compile obstruction

There is no file to pin. A future Lean slot must add a sidecar whose statement is exactly:

```text
theorem terminal_qpoly_lt_twelve_eta81_160
    (hlin : qpoly x <= L)
    (hres : qpoly r <= g*D)
    (hD : D <= 1401/625)
    (hsplit : qpoly (x+r) <= (1+81/160)*qpoly x + (1+160/81)*qpoly r) :
    qpoly (x+r) < 12
```

with `L` and `g` the existing typed constants, `D_gate` left at `4483/2000`, pinned toolchain, exit code, `#print axioms`, and placeholder scan. Until that file exists, the obstruction is missing artifact, not a failed compile.

## Assumptions still required

- the generic weighted split from `T-M4-004`, still absent;
- hypotheses `Q(x_lin) <= L` and `Q(r) <= g*D` as premises, not proved bounds;
- no identification of these scalars with deployed DH variables;
- no change to authoritative `D_gate`.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-M4-005` open.
- Requested action: do not register `D<=1401/625` as the M4 gate; do not edit registry, `state.json`, or formal certificates.
- Next formalization owner should add the corollary only after, or strictly hypothesizing, the generic split, then return a pinned receipt.

## Forbidden-boundary compliance

- Did not replace `D_gate=4483/2000`.
- Did not create physical `L`/`g` bounds.
- Did not close M4, P8, residual absorption, or flowpipe coverage from this arithmetic child.
- Did not edit registry, state, or formal proofs.
