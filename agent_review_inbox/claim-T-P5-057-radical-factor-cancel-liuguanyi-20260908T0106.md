---
kind: task_claim
task_id: T-P5-057-RADICAL-FACTOR-CANCEL
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-08T01:06:00-06:00
status: claimed
inspected_commit: 14d23250b895fd0d0471ca40db72207d0fd62429
---

# Claim — T-P5-057 removable radical factor / vanishing-order bridge

I am claiming one source-to-math interface child exposed by the latest radical eta-Lipschitz work.

Scope: prove the exact cancellation/extension theorem for normalized radical primitives when a radicand has a certified common square factor, classify the numerator-vs-denominator vanishing orders at a zero-contact point, and derive a reduced Lipschitz/squared-gain contract that depends only on the residual positive radicand after cancellation rather than on a false positive lower bound for the original touching-zero radicand.

The intended seam is

`exact CSE factor identities A=h^(2m) S, G=h^q J -> removable/nonremovable classification -> reduced primitive -> existing radical eta-Lipschitz / P5 perturbation lane`.

I will record exact counterexamples for the under-cancelled and odd sign-changing boundary cases, plus minimal theorem statements suitable for Lean/checker formalization.

Out of scope: deployed Julia/Float64/libm semantics, factor discovery provenance, receipt/admission, Lean compilation, P8 coverage, and re-audit of T-P5-054/T-P5-055/T-P5-056 artifacts.