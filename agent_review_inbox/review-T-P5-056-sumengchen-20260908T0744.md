---
kind: review_result
review_id: review-T-P5-056-sumengchen-20260908T0744
task_id: T-P5-056
agent: 苏梦辰
source_agent: 苏梦辰
created_at: 2026-09-08T01:44:00-06:00
inspected_math_review: review-T-P5-056-honglianmozun-20260908T0100
inspected_math_commit: 14d23250b895fd0d0471ca40db72207d0fd62429
formal_commit: 2697257fba48093af4dfb19f63c92278a3acb306
admission_label: compiled_candidate
integration_status: pending
requested_action: 待封不觉独立验证 / 待梁智炜最终整合
---

# T-P5-056 — radical eta-Lipschitz polynomial core Lean review

本轮优先处理前一轮 sidecar 的真实 GitHub Actions 状态，不重新做大规模数学探索。数学输入来自红莲魔尊 `T-P5-056` 的 exact radical eta-Lipschitz bridge；形式化只核化其适合 P5 squared-residual consumer 的 source-independent polynomial/root-packet 核心，不声称 source CSE、Float64、libm、ODE coverage 或 admission 已解决。

## 1. Sidecar / pinned environment

- sidecar: `examples/routeb_p5_radical_eta_lipschitz_lean/`
- Lean: `examples/routeb_p5_radical_eta_lipschitz_lean/P5RadicalEtaLipschitz.lean`
- source blob at inspected commit: `0fbe06ab58addebdddf90d462dab6826ca05a1bd`
- README: `examples/routeb_p5_radical_eta_lipschitz_lean/README.md`
- verifier: `examples/routeb_p5_radical_eta_lipschitz_lean/verify.sh`
- sidecar `lean-toolchain`: `leanprover/lean4:v4.32.0`
- verifier uses `lake` / `lean` from `PATH` and is registered with `CI_PORTABLE=1`; it consumes the repository-pinned `examples/local_fkg/lake-manifest.json` dependency environment rather than a hard-coded machine path.

## 2. Minimal theorem decomposition actually kernel-checked

Nine exported theorems are present:

1. `root_product_margin`: from nonnegative root packets `m ≤ r²`, `m ≤ s²`, derive `m ≤ r*s`.
2. `sqrt_two_point_sq_from_roots`: radical-free two-point square-root charge `4*m*(r-s)² ≤ (A-B)²` under exact root identities.
3. `inverse_root_charge_from_relation`: transport the root-difference charge through the exact reciprocal packet `r*s*h = s-r`, yielding `4*m³*h² ≤ DA²*deta²`.
4. `numerator_over_root_charge`: division-free numerator/root charge.
5. `bias_inverse_root_charge`: multiply reciprocal-root charge by a bounded numerator amplitude.
6. `weighted_two_term_square_identity`: exact denominator-free Young identity.
7. `weighted_two_term_square_bound`: the corresponding two-term square inequality.
8. `normalized_radical_sq_from_atomic_charges`: fused checker-friendly squared normalized-radical certificate.
9. `normalized_radical_sq_from_root_packet`: end-to-end root-packet consumer combining all previous atomic obligations.

The principal exported consumer is intentionally stated without source evaluator semantics. In plain algebraic form it proves that, from a nonnegative radicand margin packet, exact root/reciprocal identities, source variation charges for `A` and `G`, and `uDiff = a+b`, one obtains

`4*theta*m^3*uDiff^2 <= (1+theta)*(4*theta*m^2*DG^2 + MG^2*DA^2)*deta^2`.

This is the radical-free squared bridge requested by the math review, with hypotheses made explicit and no hidden MVT/FTC or monotonicity assumption.

## 3. Real CI repair loop

The pre-fix sidecar hit a Lean 4.32 `warningAsError` blocker from an unused hypothesis. Commit `2697257fba48093af4dfb19f63c92278a3acb306` removes that unused formal parameter without weakening the mathematical conclusions.

The subsequent real GitHub Actions run is:

- workflow: `Lean agent sidecars`
- run: `34199121964`
- job: `101973606256`
- runner environment: Lean `4.32.0`, Lake `5.0.0-src+8c9756b`

For this sidecar the log explicitly reports:

- `AXIOM_AUDIT=PASS`
- `P5_RADICAL_ETA_LIPSCHITZ_FOCUSED_CHECK=PASS`
- `SIDECAR_RESULT=PASS path=examples/routeb_p5_radical_eta_lipschitz_lean/verify.sh`

Thus the T-P5-056 focused compile is green in the actual portable workflow.

The aggregate `portable-sidecars` job remains red because of unrelated pre-existing sidecars (including FLT path resolution, M4 cross-branch, old P5 componentwise/direct-two-channel/parameter-tube/weighted-dual, P7 tail-Schur and old P8 ramp reconstruction). 本轮没有越权修改这些工件。

## 4. Axiom state

All nine exported T-P5-056 theorems print only the ordinary mathlib axioms

`[propext, Classical.choice, Quot.sound]`.

No exported theorem contains `sorryAx` in the passing run.

## 5. Dependencies and still-open formal interfaces

The Lean core now expects the source/checker layer to bind the abstract packet to the real CSE nodes. The remaining obligations are intentionally left open:

- `ROOT_PACKET_SOURCE_BINDING=OPEN`
- `RADICAND_MARGIN_SOURCE_BINDING=OPEN`
- `ETA_VARIATION_SOURCE_BINDING=OPEN`
- `FLOAT64_LIBM_SEMANTICS=OPEN`
- `P8_ODE_COVERAGE=OPEN`

In particular, this result does not prove that the deployed source evaluates the exact cancelled/rationalized expression, does not certify Float64/libm outward rounding, and does not establish same-domain trajectory coverage.

## 6. Status

`compiled_candidate` only. No registry/admission/global-status mutation is requested or implied.

**待封不觉独立验证 / 待梁智炜最终整合。**