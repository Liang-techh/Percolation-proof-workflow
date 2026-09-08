# Single-shift review after PATHDOMAINPROJECTION repair

Status: **OPEN_UNCOMPILED / pending**. This is a bounded static review plus
one independent 47-line typed arithmetic/path consumer. No Lean/Lake or
regression ran. Existing modules, registry/state and old receipts were not
modified. Read-only shell access to local source files was not a compiler run.

## Finding: B is still consumed once mathematically

The repaired `projected_shift_cap_transfer_attempt` preserves its statement:
source<=cap, shifted target=source+B, and cap+B<=bar. Its body adds only

```lean
have hBudget' : B + cap ≤ bar := by simpa [add_comm] using hBudget
```

This is an order normalization of the same sum, not a second addition of B.
`repaired_budget_equivalent_attempt` expresses exactly that equivalence.

The current aligned consumer still has this chain:

| Step | Bound/value supplied | Count of shift B |
| --- | --- | --- |
| INITIALPATHCAPS initial plus integrated growth | source(path(t))<=a+beta | 0 |
| ACTUALSTORAGEALIGN value identity | target=source+B | 1 |
| ConsumerPremises.shiftedBudget | (a+beta)+B<=bar | 1 |
| Repaired budget normalization | B+(a+beta)<=bar | Same single B |

The consumer does not add a second B to a or beta. This audit checks the
typed meaning of those fields, not whether the caller's numeric a/beta
already contains a shift under a different storage label. Such an input
would still need the proper same-storage normalization review.

## Minimal independent composition

`single_shift_step_attempt` uses only s<=a+beta, g=s+B and
(a+beta)+B<=bar, then proves g<=bar using linear arithmetic. It avoids
dependence on the elaboration order of `add_le_add_right` and `.trans`.

`single_shift_path_consumer_attempt` additionally requires the full-state
domain projection, whole-path membership, and the shifted value identity
on projected configurations in Q. It applies the scalar step at each t in
[0,1]. For the existing aligned consumer, instantiate F=source(model),
G=target(model), project=Prod.fst and B=ACTUALSTORAGEALIGN.shiftB. Its source
cap is the output of INITIALPATHCAPS; its value identity is the output of
ACTUALSTORAGEALIGN. None of these actual instances is asserted here.

The new leaf imports only Mathlib. It neither imports nor certifies the
pending repaired dependency chain. It supplies no new initial bound,
integrated growth, Alignment, path inclusion, source semantics or ODE proof.

## Exact double-charge counterexample

Set B=4079979/400000, source s=0, target g=B, source cap=0 and target bar=B.
Then g=s+B, s<=cap, cap+B<=bar and g<=bar all hold exactly. But g+B<=bar
is false because B>0. `saturated_single_shift_counterexample_attempt`
encodes this saturated valid budget. Double counting therefore imposes an
unnecessary stronger condition that can falsely reject a valid cap; it does
not repair missing source/path hypotheses or justify a stronger acceptance.

## Repair/receipt boundary and remaining elaboration risk

The inspected focused receipt
`agent_review_inbox/review-T-P4-033-O1-body6-slice-lean-receipt-codex-20260908T052153.md`
records a **pre-repair** PATHDOMAINPROJECTION elaboration failure:
cap+B was supplied where that application expected B+cap. It also records
INITIALPATHCAPS dependency blockage, not successful elaboration of that file.
No successful post-repair receipt was established by this review.

The repaired PATHDOMAINPROJECTION source now has a different hash from the
pre-repair snapshot. The old aligned-consumer review's dependency hash
therefore does not pin the current repaired source; the current hash below
is the one inspected here. This review does not rewrite the old receipts.

One additional **static risk**, not a newly observed compiler error, remains:
ACTUALSTORAGEALIGN.aligned_path_cap_transfer_attempt contains the same
`(add_le_add_right ... B).trans hBudget` spelling as the failed pattern.
The current aligned consumer calls the earlier shifted-value lemma rather
than that helper, but its whole imported module must still elaborate.
The future focused check must inspect that site as well. A linear-arithmetic
finish after the value rewrite is an available bounded repair if required;
no existing source was edited in this review.

## Inspected hashes

| File under `examples/routeb_b45_source_comparator_lean` | SHA-256 |
| --- | --- |
| `NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.lean` (repaired) | `557a732c06cf774e49e75a811e1a01c910617ec011e0f84e5de72f0919a16f5b` |
| `NEW_BODY6_SLICE_INITIALPATHCAPS20260907.lean` | `5cad04f2e8b0af13c8d8a099455812fe1f6d17a66a0d567be5b85963252d224f` |
| `NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907.lean` | `f8da2e44f9afc4c80fc14e81a1c59626d5af98071300a009aecd33463d3bef56` |
| `NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.lean` | `f698d8c56c83005df0e0a907452ae7a6f083eb3736e6df60db4d0190084367dd` |
| `NEW_BODY6_SLICE_ONESHIFTREPAIR20260908.lean` | `a468140373c9fe43b52a3b3e0e15a5a773a437b44361c6b1898ba93af312649b` |

Focused failure-receipt SHA-256:
`59a88b4d7abce373d93aa08891679cf223c2724d785b26480f6acc691f211858`.
All conclusions about current source shape are static. No kernel/axiom
receipt or actual candidate instantiation was produced. Keep both the new
leaf and the reviewed composition **OPEN_UNCOMPILED / pending**.
