---
kind: review_result
task_id: T-P4-036.2
source_agent: Codex
created_at: 2026-09-07
integration_status: pending
---

# Single-leaf receipt-to-Lean adapter

## Scope

This review handles one leaf only: `p3_candidate.cell_id = "1"` from
`artifacts/routeb_agent_p3_coverage_next_20260906T091543Z/
p3_coverage_bridge_audit.json`. The input artifact describes itself as a
read-only replay/candidate record; this adapter does not promote it to global
coverage or a deployed evaluator receipt.

The generator parses each recorded decimal/rational string with Python
`Fraction`, then emits exact `ℚ` literals. The Lean side checks the typed leaf
id and coordinate order and casts the exact endpoints into the existing
`RectBox13`/`InRectBox` interface.

Input receipt SHA-256:

```text
87CF832BF5D9D266A532EEA4DC54B9365FF9E4A5E709031907C8E9A97BDDC7D6
```

The selected q2 endpoints, after exact parsing, are:

```text
lo = -7742688036293973 / 100000000000000000
hi = -6742688036293973 / 100000000000000000
```

Lean proves `-3/20 ≤ lo` and `hi ≤ 3/20` by `norm_num`; no Float64 value is
introduced by this adapter.

## Typed adapter target

The generated source defines:

```lean
inductive ReceiptCoord
  | q1 | q2 | q3 | q4 | q5 | q6
  | dq1 | dq2 | dq3 | dq4 | dq5 | dq6 | w

structure ReceiptLeaf13 where
  leafId : Nat
  coordinateOrder : Fin 13 → ReceiptCoord
  lo : (Fin 13 → ℚ)
  hi : (Fin 13 → ℚ)
  ordered : ∀ i, lo i ≤ hi i
```

For the single record, Lean checks:

```lean
receipt_leaf1_id : receiptLeaf1.leafId = 1
receipt_leaf1_coordinate_order :
  receiptLeaf1.coordinateOrder = canonicalOrder
receipt_leaf1_q2_lower :
  -(3 / 20 : ℝ) ≤ (receiptLeaf1.lo q2Index : ℝ)
receipt_leaf1_q2_upper :
  (receiptLeaf1.hi q2Index : ℝ) ≤ (3 / 20 : ℝ)
```

The final typed target is:

```lean
theorem receipt_leaf1_theta2_exact_real_interval {x : State13}
    (hx : InRectBox (receiptLeaf1.toRectBox) x) :
    theta2 (x q2Index) + Real.pi / 2 = x q2Index ∧
    (-1 : ℝ) ≤ Real.sin (theta2 (x q2Index)) ∧
      Real.sin (theta2 (x q2Index)) ≤ -(791 / 800 : ℝ) ∧
    -(2409 / 16000 : ℝ) ≤ Real.cos (theta2 (x q2Index)) ∧
      Real.cos (theta2 (x q2Index)) ≤ 2409 / 16000
```

The only state premise is `hx : InRectBox ... x`; it is not manufactured by
the receipt parser. A future source-bound leaf witness must supply that
membership premise separately.

## Fresh pinned compile receipt

The generator is:

```text
scripts/routeb_theta2_receipt_to_lean.py
sha256 = 9675312237FEC4F69EE9B22D53E00B8ED9AFDD3F2C35AF445BD65D0E1ED52C39
```

The generated adapter and matching compiled artifact are:

```text
source:
  artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/mathlib/
  DownstreamTest/Theta2ReceiptAdapterGenerated.lean
source_sha256:
  5B9AD6A95D2F8C18C5F48A91AA6852724DA36C52060EDFCF3F95300431D56112
olean:
  artifacts/routeb_fd8_tensor_christoffel_enclosure_20260906/mathlib/.lake/
  build/lib/lean/DownstreamTest/Theta2ReceiptAdapterGenerated.olean
olean_sha256:
  DAE74AD000EC6153D7D03585A686C81915DC0506315AA33FF61A0A3EE996A3E9
toolchain:
  leanprover/lean4:v4.33.1
Lean:
  Lean (version 4.33.1, x86_64-w64-windows-gnu,
  commit 819816b2e0a3bf405af45ae5c7af2491d8f5bee6, Release)
command:
  lake env lean -o .lake/build/lib/lean/DownstreamTest/
    Theta2ReceiptAdapterGenerated.olean DownstreamTest/
    Theta2ReceiptAdapterGenerated.lean
exit_code: 0
```

The successful compile also printed:

```text
RouteBTheta2ReceiptAdapter.receipt_leaf1_theta2_exact_real_interval
  {x : State13} (hx : InRectBox receiptLeaf1.toRectBox x) :
  theta2 (x q2Index) + Real.pi / 2 = x q2Index ∧
    -1 ≤ Real.sin (theta2 (x q2Index)) ∧
      Real.sin (theta2 (x q2Index)) ≤ -(791 / 800) ∧
        -(2409 / 16000) ≤ Real.cos (theta2 (x q2Index)) ∧
          Real.cos (theta2 (x q2Index)) ≤ 2409 / 16000

'RouteBTheta2ReceiptAdapter.receipt_leaf1_theta2_exact_real_interval'
  depends on axioms: [propext, Classical.choice, Quot.sound]
```

The axiom list is a dependency report only. The theorem has no `sorry`, user
axiom, Float64, libm, finite-DH, or coverage-completeness premise.

## Exact remaining gap

This closes the typed implication for one parsed record, conditional on the
`InRectBox` witness. It does not prove that the candidate JSON is a certified
coverage leaf, does not validate sibling/parent partition relations, and does
not connect a runtime trajectory to `x`. The remaining receipt-to-Lean seam is
therefore exactly the external provenance/witness handoff:

```text
authoritative leaf JSON + source hash
  -> generated exact-ℚ ReceiptLeaf13 (done for leaf 1)
  -> RectBox13 endpoint cast (compiled)
  -> InRectBox witness for the actual x (OPEN)
  -> theta2_exact_real_interval (compiled)
```

No full-domain coverage or O2 closure is claimed.

## Status

```text
single_leaf_parse: COMPILED
leaf_id_binding: COMPILED
coordinate_order_binding: COMPILED
lo_hi_exact_rational_cast: COMPILED
q2_domain_transport: COMPILED
InRectBox_actual_witness: OPEN
coverage_completeness: OPEN
Float64_libm_DAG: OUT_OF_SCOPE
formal_certificate_allowed: false
registry_promoted: false
```
